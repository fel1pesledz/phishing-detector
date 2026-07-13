# Virus Checker Extension

A Google Chrome extension that checks files and URLs for viruses/malware before the user downloads a file or accesses a link, using the VirusTotal API.

## About the project

When a user attempts to download a file or navigate to a suspicious URL, the extension intercepts the action and sends the relevant information to the backend, which queries the [VirusTotal API](https://developers.virustotal.com/reference/overview) to determine whether the file/URL is malicious. The result is displayed to the user in real time, allowing them to decide whether to proceed.

## Project structure

```
.
├── backend
│   ├── app
│   │   ├── routes       # API endpoints (e.g. /check-url, /check-file)
│   │   └── services     # Integration logic with the external verification API
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests
├── extension
│   ├── background.js    # Listens for browser events (downloads, navigation)
│   ├── content.js       # Interacts with the page the user is visiting
│   ├── manifest.json    # Extension configuration
│   └── popup            # Extension UI (HTML/CSS/JS)
├── docker-compose.yml
└── README.md
```

## Tech stack

- **Backend:** Python (Flask/FastAPI)
- **Extension:** JavaScript (Manifest V3)
- **Infrastructure:** Docker / Docker Compose
- **External API:** [VirusTotal API](https://developers.virustotal.com/reference/overview)

## Getting started

### Backend

```bash
cd backend
docker build -t virus-checker-backend .
docker run -p 8000:8000 --env-file .env virus-checker-backend
```

Or, using Docker Compose:

```bash
docker-compose up --build
```

### Environment variables

Create a `.env` file inside `backend/` with:

```
VT_API_KEY=your_virustotal_api_key
```

> A free API key can be obtained by creating an account at [virustotal.com](https://www.virustotal.com/). Note the free tier's rate limits (e.g. 4 requests/minute).

### Extension

1. Go to `chrome://extensions` in Google Chrome.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select the `extension/` folder.
4. The extension will appear in the browser toolbar.

## How it works

1. The user attempts to download a file or access a URL.
2. `background.js`/`content.js` capture the event and send a request to the backend.
3. The backend queries the VirusTotal API (file upload or URL analysis).
4. The result is returned and displayed in the `popup` or as an alert on the page.

## Testing

```bash
cd backend
pytest
```

## Team

- [Add team member names]

## License

[Define license, e.g. MIT]
