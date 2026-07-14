# Pulse Messenger — Python Edition

A working real-time room messenger using only Python 3. No Node.js and no package installation.

## Start

### Windows
Double-click `start_windows.bat`, or open Command Prompt in this folder and run:

```bat
python server.py
```

### macOS / Linux
Open Terminal in this folder and run:

```bash
python3 server.py
```

Then open **http://localhost:8000**.

Keep the terminal window open while using the app. Open a second browser window and enter the same room to test real-time messaging.

## Phone or another computer
Connect both devices to the same Wi-Fi. On the server computer, find its local IP address and open:

```text
http://YOUR-COMPUTER-IP:8000
```

You may need to allow Python through the computer firewall.

## Features
- Real-time messages via efficient long polling
- Public rooms
- Online presence and typing indicators
- Message history saved in `messages.json`
- Responsive desktop/mobile design
- No third-party dependencies

## Production note
For a public internet deployment, add HTTPS, user authentication, rate limiting, moderation, and a production database.
