#!/usr/bin/env python3
"""Pulse Messenger — hardened dependency-free Python server."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from threading import Lock
from datetime import datetime, timezone
from collections import defaultdict, deque
import json, time, uuid, os, logging
VERSION="0.2.0"; ROOT=Path(__file__).resolve().parent; DATA=ROOT/"messages.json"; LOCK=Lock(); CLIENTS,HISTORY={},{}; RATE=defaultdict(deque)
logging.basicConfig(level=os.environ.get("LOG_LEVEL","INFO"),format="%(asctime)s %(levelname)s %(message)s")
try: HISTORY=json.loads(DATA.read_text("utf-8"))
except Exception: HISTORY={}
def now(): return datetime.now(timezone.utc).isoformat()
def clean(value,limit=1000): return str(value or "").strip()[:limit]
def save():
    tmp=DATA.with_suffix(".tmp"); tmp.write_text(json.dumps(HISTORY,indent=2),"utf-8"); tmp.replace(DATA)
def room_clients(room): return [c for c in CLIENTS.values() if c["room"]==room]
def emit(room,event,exclude=None):
    for cid,c in CLIENTS.items():
        if c["room"]==room and cid!=exclude: c["queue"].append(event)
def update_users(room): emit(room,{"type":"users","users":[c["name"] for c in room_clients(room)]})
def update_typing(room): emit(room,{"type":"typing","users":[c["name"] for c in room_clients(room) if c["typing"]]})
def remove_client(cid):
    c=CLIENTS.pop(cid,None)
    if c: emit(c["room"],{"type":"system","text":f'{c["name"]} left the room'}); update_users(c["room"]); update_typing(c["room"])
def prune():
    cutoff=time.time()-45
    for cid in [x for x,c in CLIENTS.items() if c["seen"]<cutoff]: remove_client(cid)
def allowed(key,limit,window=10):
    q=RATE[key]; t=time.time()
    while q and q[0]<t-window: q.popleft()
    if len(q)>=limit: return False
    q.append(t); return True
class Handler(SimpleHTTPRequestHandler):
    server_version="Pulse/"+VERSION
    def translate_path(self,path): return str(ROOT/(urlparse(path).path.lstrip("/") or "index.html"))
    def log_message(self,fmt,*args): logging.info('%s %s',self.client_address[0],fmt%args)
    def end_headers(self):
        self.send_header("X-Content-Type-Options","nosniff"); self.send_header("X-Frame-Options","DENY"); self.send_header("Referrer-Policy","no-referrer"); self.send_header("Permissions-Policy","camera=(), microphone=(), geolocation=()"); self.send_header("Content-Security-Policy","default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"); super().end_headers()
    def json_out(self,obj,status=200):
        body=json.dumps(obj).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store"); self.end_headers(); self.wfile.write(body)
    def body(self):
        try:
            size=int(self.headers.get("Content-Length",0))
            if size>8192: return None
            return json.loads(self.rfile.read(size) or b"{}")
        except Exception: return None
    def do_GET(self):
        u=urlparse(self.path)
        if u.path in ("/health","/api/health"): return self.json_out({"status":"ok","version":VERSION,"time":now()})
        if u.path=="/api/version": return self.json_out({"name":"Pulse Messenger","version":VERSION})
        if u.path=="/api/poll":
            cid=parse_qs(u.query).get("client",[""])[0]
            with LOCK:
                prune(); c=CLIENTS.get(cid)
                if not c: return self.json_out({"error":"session expired"},410)
                c["seen"]=time.time(); events=c["queue"][:]; c["queue"].clear()
            return self.json_out({"events":events})
        super().do_GET()
    def do_POST(self):
        d=self.body()
        if d is None: return self.json_out({"error":"Invalid or oversized request"},400)
        ip=self.client_address[0]
        with LOCK:
            prune()
            if self.path=="/api/join":
                if not allowed((ip,"join"),8,60): return self.json_out({"error":"Too many join attempts. Try again shortly."},429)
                name=clean(d.get("name"),24); room=clean(d.get("room"),24).lower(); room="".join(x if x.isalnum() or x in "_-" else "-" for x in room)
                if not name or not room: return self.json_out({"error":"Name and room are required"},400)
                used=[c["name"] for c in room_clients(room)]; base=name; n=2
                while name in used: name=f"{base} {n}"; n+=1
                cid=uuid.uuid4().hex; CLIENTS[cid]={"name":name,"room":room,"typing":False,"queue":[],"seen":time.time()}; emit(room,{"type":"system","text":f"{name} joined the room"},cid); update_users(room); logging.info("join room=%s user=%s",room,name)
                return self.json_out({"client":cid,"name":name,"history":HISTORY.get(room,[])[-100:],"version":VERSION})
            cid=clean(d.get("client"),64); c=CLIENTS.get(cid)
            if not c: return self.json_out({"error":"session expired"},410)
            c["seen"]=time.time()
            if self.path=="/api/message":
                if not allowed((cid,"message"),20,10): return self.json_out({"error":"You are sending messages too quickly."},429)
                text=clean(d.get("text"))
                if not text: return self.json_out({"error":"Message cannot be empty"},400)
                msg={"type":"message","id":uuid.uuid4().hex,"name":c["name"],"text":text,"timestamp":now()}; HISTORY.setdefault(c["room"],[]).append(msg); HISTORY[c["room"]]=HISTORY[c["room"]][-500:]; save(); emit(c["room"],msg); c["typing"]=False; update_typing(c["room"])
                return self.json_out({"ok":True,"message":msg})
            if self.path=="/api/typing": c["typing"]=bool(d.get("active")); update_typing(c["room"]); return self.json_out({"ok":True})
            if self.path=="/api/leave": remove_client(cid); return self.json_out({"ok":True})
        return self.json_out({"error":"Not found"},404)
if __name__=="__main__":
    port=int(os.environ.get("PORT","8000")); logging.info("Pulse %s running at http://localhost:%s",VERSION,port); ThreadingHTTPServer(("0.0.0.0",port),Handler).serve_forever()
