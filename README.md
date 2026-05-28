# Phishing Detector

A real-time phishing detection system combining machine learning, a REST API, and a Chrome Extension to identify malicious URLs and emails before they cause harm.


---

## Overview

Phishing Detector provides organizations and individuals with a layered defense against phishing attacks. It combines a machine learning model trained on known malicious patterns with real-time browser integration, giving users immediate feedback before interacting with suspicious content.

---

## Features

- **URL Scanner** — assigns a threat score from 0 to 100 based on domain reputation, redirects, and structural patterns
- **SSL Certificate Verification** — validates certificate authenticity and chain of trust
- **Fake Login Page Detection** — identifies credential-harvesting pages using visual and structural heuristics
- **Chrome Extension** — provides real-time alerts and inline threat indicators via Manifest v3
- **Email Phishing Detector** — AI-powered analysis of email headers, links, and body content
- **Analytics Dashboard** — visualizes threat trends, scan history, and detection metrics

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask, Scikit-learn |
| Frontend | React, Tailwind CSS |
| Extension | Chrome Manifest v3 |
| Database | MongoDB |
| Infrastructure | Docker |

---

## Project Structure

```
phishing-detector/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
│   ├── package.json
│   └── Dockerfile
├── extension/
│   ├── manifest.json
│   ├── background.js
│   └── popup/
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`.

### Chrome Extension

1. Open Chrome and navigate to `chrome://extensions`
2. Enable **Developer mode** in the top-right corner
3. Click **Load unpacked** and select the `extension/` directory
4. The extension icon will appear in the toolbar

### Docker (all services)

```bash
docker compose up --build
```

---

## Usage

**Scanning a URL**

Send a POST request to the API with the target URL:

```bash
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response**

```json
{
  "url": "https://example.com",
  "threat_score": 12,
  "ssl_valid": true,
  "is_phishing": false,
  "details": {
    "domain_age_days": 3420,
    "redirects": 0,
    "suspicious_keywords": []
  }
}
```

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

Please follow the existing code style and include tests for new functionality.

---

