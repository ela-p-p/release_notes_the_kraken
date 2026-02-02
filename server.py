import os
from base64 import b64encode
from typing import Any, Literal

import requests
from dotenv import load_dotenv  # type: ignore
from flask import Flask, Response, jsonify
from requests.auth import HTTPBasicAuth

load_dotenv()


app = Flask(__name__)


JIRA_BASE_URL: str = os.environ.get(
    "JIRA_BASE_URL", "https://your-domain.atlassian.net"
)
JIRA_API_EMAIL: str = os.environ.get(
    "JIRA_API_EMAIL", "your-email@example.com"
)  # noqa: E501
JIRA_API_TOKEN: str = os.environ.get("JIRA_API_TOKEN", "your-api-token")
PROJECT_KEY: str = os.environ.get("PROJECT_KEY", "SCRUM")

url: str = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
auth = HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN)
headers: dict[str, str] = {"Accept": "application/json"}


def get_jira_auth_headers() -> dict[str, str]:
    auth_str: str = f"{JIRA_API_EMAIL}:{JIRA_API_TOKEN}"
    b64_auth: str = b64encode(auth_str.encode()).decode()
    return {
        "Authorization": f"Basic {b64_auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


@app.route("/")
def home() -> str:
    return "AI release notes is running."


@app.route("/api/jira/field", methods=["GET"])
def jira_field() -> tuple[Response, Literal[200]] | tuple[Response, int]:
    url = f"{JIRA_BASE_URL}/rest/api/3/field"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
    )
    print(response.json())
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return (
            jsonify({"status": "error", "details": response.text}),
            response.status_code,
        )


@app.route("/api/jira/project_keys", methods=["GET"])
def jira_project_keys() -> (
    tuple[Response, Literal[200]] | tuple[Response, int]
):  # noqa: E501
    url: str = f"{JIRA_BASE_URL}/rest/api/3/project/search"
    headers: dict[str, str] = get_jira_auth_headers()
    response: requests.Response = requests.get(url, headers=headers)
    if response.ok:
        projects = response.json().get("values", [])
        project_keys: list[Any] = [p.get("key") for p in projects]
        return jsonify({"status": "ok", "project_keys": project_keys}), 200
    else:
        return (
            jsonify({"status": "error", "details": response.text}),
            response.status_code,
        )


@app.route("/api/jira/issues", methods=["GET"])
def get_jira_issues() -> tuple[Response, Literal[200]] | tuple[Response, int]:
    url: str = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    # status,assignee,created,updated,description,
    query: dict[str, str] = {
        "jql": f"project = {PROJECT_KEY}",
        "fields": "key,summary,customfield_10000",
        "maxResults": "50",
    }
    print(
        f"Fetching issues for project {PROJECT_KEY} from Jira: {url} "
        f"with params: {query}"
    )
    response: requests.Response = requests.get(
        url,
        headers={"Accept": "application/json"},
        params=query,
        auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
    )
    if response.ok:
        data = response.json()
        return jsonify(data), 200
    else:
        return jsonify({"error": response.text}), response.status_code


@app.route("/api/jira/issueByKey/<issueIdOrKey>", methods=["GET"])
def jira_issueByKey(
    issueIdOrKey: str,
) -> tuple[Response, Literal[200]] | tuple[Response, int]:
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
    )
    print(response.json())
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return (
            jsonify({"status": "error", "details": response.text}),
            response.status_code,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
