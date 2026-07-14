import json, os, subprocess, time, unittest, urllib.request, urllib.error
PORT="8765"; BASE=f"http://127.0.0.1:{PORT}"
def request(path,data=None):
    kwargs={}
    if data is not None: kwargs={"data":json.dumps(data).encode(),"headers":{"Content-Type":"application/json"}}
    with urllib.request.urlopen(urllib.request.Request(BASE+path,**kwargs),timeout=5) as r: return r.status,json.load(r),dict(r.headers)
class PulseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc=subprocess.Popen(["python3","server.py"],env={**os.environ,"PORT":PORT},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(30):
            try: request("/health"); return
            except Exception: time.sleep(.1)
        raise RuntimeError("server failed to start")
    @classmethod
    def tearDownClass(cls): cls.proc.terminate(); cls.proc.wait(timeout=5)
    def test_health_and_security_headers(self):
        status,data,headers=request("/health"); self.assertEqual(status,200); self.assertEqual(data["status"],"ok"); self.assertEqual(headers["X-Content-Type-Options"],"nosniff")
    def test_two_users_exchange_message(self):
        _,a,_=request("/api/join",{"name":"Alice","room":"test-room"}); _,b,_=request("/api/join",{"name":"Bob","room":"test-room"}); _,sent,_=request("/api/message",{"client":a["client"],"text":"Hello Bob"}); self.assertTrue(sent["ok"]); self.assertIn("id",sent["message"]); _,polled,_=request("/api/poll?client="+b["client"]); self.assertTrue(any(e.get("text")=="Hello Bob" for e in polled["events"]))
    def test_empty_message_rejected(self):
        _,a,_=request("/api/join",{"name":"Charlie","room":"empty-test"})
        with self.assertRaises(urllib.error.HTTPError) as ctx: request("/api/message",{"client":a["client"],"text":"   "})
        self.assertEqual(ctx.exception.code,400)
if __name__=="__main__": unittest.main()
