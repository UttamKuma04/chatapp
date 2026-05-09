# Aglo Chat

Aglo Chat is a Django-based real-time chat application. It lets registered users log in, join named chat rooms, exchange messages over WebSockets, and start browser-based audio or video calls using WebRTC signaling through Django Channels.

## Features

- User registration and login with Django authentication.
- Named chat rooms that users can join from the main chat screen.
- Real-time chat messages delivered through WebSockets.
- Message history persisted in SQLite through the `ChatMessage` model.
- Audio and video call signaling through the same WebSocket room.
- Basic media upload endpoint and media file settings.
- Admin support for viewing and searching stored chat messages.

## Tech Stack

- Python with Django 5.2.6.
- Django Channels for ASGI and WebSocket handling.
- Daphne as the ASGI server.
- SQLite for local data storage.
- Browser WebRTC APIs for peer-to-peer audio and video calls.
- HTML, CSS, and vanilla JavaScript templates.

## Project Structure

```text
.
|-- README.md
|-- .gitignore
`-- aglo/
    |-- manage.py
    |-- requirements.txt
    |-- db.sqlite3
    |-- aglo/
    |   |-- settings.py
    |   |-- urls.py
    |   |-- asgi.py
    |   `-- wsgi.py
    |-- app/
    |   |-- consumers.py
    |   |-- models.py
    |   |-- routing.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    `-- templates/
        |-- base.html
        |-- login.html
        `-- register.html
```

## Requirements

- Python 3.10 or newer.
- A modern browser with WebSocket and WebRTC support.
- Camera and microphone permissions for audio or video calling.

Redis packages are listed in `requirements.txt`, but the current settings use Django Channels' in-memory channel layer. That is suitable for local development and single-process testing. Use Redis for multi-process or production deployments.

## Setup

From the repository root:

```powershell
cd aglo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
```

Create an admin user if you want to use the Django admin:

```powershell
python manage.py createsuperuser
```

## Configuration

The project reads these environment variables:

```text
DJANGO_SECRET_KEY=change-this-in-production
DJANGO_DEBUG=True
```

Important defaults in `aglo/aglo/settings.py`:

- `DEBUG` is disabled unless `DJANGO_DEBUG=True`.
- `ALLOWED_HOSTS` is currently set to allow all hosts.
- CSRF trusted origins include Render subdomains.
- SQLite is used as the default database.
- Uploaded media is stored under `aglo/media/`.

## Running Locally

Use Daphne so HTTP and WebSocket traffic are both served by the ASGI application:

```powershell
daphne -b 127.0.0.1 -p 8000 aglo.asgi:application
```

Then open:

```text
http://127.0.0.1:8000/
```

You can also run Django management commands from the `aglo/` directory:

```powershell
python manage.py check
python manage.py test
```

## Usage

1. Register a new account at `/register/`.
2. Log in at `/login/`.
3. Enter a room name on the chat screen.
4. Share the same room name with another logged-in user to chat together.
5. Use the Audio or Video controls in the room header to start a browser call.

Messages are stored with the room name, username, message body, and timestamp. When a user reconnects to a room, recent messages are loaded from the database.

## WebSocket Flow

- Browser clients connect to `ws://host/ws/chat/<room_name>/`.
- `app.routing` maps the WebSocket URL to `ChatConsumer`.
- `ChatConsumer` adds each client to a Channels group for the selected room.
- Chat messages are saved to the database and broadcast to the room.
- WebRTC signaling messages such as offers, answers, ICE candidates, and call events are relayed through the room group.

## Deployment Notes

- Set a strong `DJANGO_SECRET_KEY`.
- Set `DJANGO_DEBUG=False` for production.
- Replace `ALLOWED_HOSTS=["*"]` with explicit hostnames.
- Use Redis as the Channels layer for production or multiple worker processes.
- Serve static files and uploaded media with production-ready storage.
- Review the CSRF settings before deploying outside Render.

## Known Gaps

- `upload_file_view` exists, but the current chat template does not expose a file attachment control.
- The `0002` migration adds a file field to `ChatMessage`, while the current model only stores text messages.
- The test suite is still empty.
