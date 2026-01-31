# Jira App Python Server

This project is a basic Python server scaffold for building a Jira app integration. It uses Flask to provide REST API endpoints and is ready to be extended for Jira API interactions.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python server.py
   ```
3. The server will be available at http://localhost:5000

## Endpoints
- `/` : Health check
- `/api/jira` : Receives Jira webhook POST requests

## Next Steps
- Add authentication for Jira API
- Implement Jira API request handling
- Extend endpoints as needed
