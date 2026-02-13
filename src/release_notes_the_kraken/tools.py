import os
from base64 import b64encode
from typing import Any

import requests
from mcp.server import Server
from mcp.types import TextContent, Tool
from requests.auth import HTTPBasicAuth

# Configuration
JIRA_BASE_URL: str = os.environ.get("JIRA_BASE_URL", "https://your-domain.atlassian.net")
JIRA_API_EMAIL: str = os.environ.get("JIRA_API_EMAIL", "your-email@example.com")
JIRA_API_TOKEN: str = os.environ.get("JIRA_API_TOKEN", "your-api-token")
PROJECT_KEY: str = os.environ.get("PROJECT_KEY", "SCRUM")


def get_jira_auth_headers() -> dict[str, str]:
    auth_str: str = f"{JIRA_API_EMAIL}:{JIRA_API_TOKEN}"
    b64_auth: str = b64encode(auth_str.encode()).decode()
    return {
        "Authorization": f"Basic {b64_auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def register_tools(server: Server) -> None:
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available JIRA integration tools."""
        return [
            Tool(
                name="get_jira_fields",
                description="Get all available JIRA fields",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_project_keys",
                description="Get all JIRA project keys available in the workspace",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_jira_issues",
                description=(
                    "Get JIRA issues for a specific project. Returns up to 50 "
                    "issues with key, summary, and custom fields."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_key": {
                            "type": "string",
                            "description": (f"JIRA project key (default: {PROJECT_KEY})"),
                        },
                        "max_results": {
                            "type": "number",
                            "description": (
                                "Maximum number of results to return (default: 50)"
                            ),
                        },
                    },
                },
            ),
            Tool(
                name="get_issue_by_key",
                description=(
                    "Get detailed information about a specific JIRA issue "
                    "by its key or ID"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_key": {
                            "type": "string",
                            "description": "The JIRA issue key or ID (e.g., SCRUM-123)",
                        },
                    },
                    "required": ["issue_key"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Handle tool calls for JIRA integration."""

        if name == "get_jira_fields":
            url = f"{JIRA_BASE_URL}/rest/api/3/field"
            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
            )

            if response.ok:
                return [TextContent(type="text", text=str(response.json()))]
            else:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {response.status_code} - {response.text}",
                    )
                ]

        elif name == "get_project_keys":
            url = f"{JIRA_BASE_URL}/rest/api/3/project/search"
            headers = get_jira_auth_headers()
            response = requests.get(url, headers=headers)

            if response.ok:
                projects = response.json().get("values", [])
                project_keys = [p.get("key") for p in projects]
                return [
                    TextContent(
                        type="text",
                        text=f"Project keys: {', '.join(project_keys)}",
                    )
                ]
            else:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {response.status_code} - {response.text}",
                    )
                ]

        elif name == "get_jira_issues":
            project_key = arguments.get("project_key", PROJECT_KEY)
            max_results = arguments.get("max_results", 50)

            url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
            query = {
                "jql": f"project = {project_key}",
                "fields": "key,summary,customfield_10000",
                "maxResults": str(max_results),
            }

            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                params=query,
                auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
            )

            if response.ok:
                data = response.json()
                return [TextContent(type="text", text=str(data))]
            else:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {response.status_code} - {response.text}",
                    )
                ]

        elif name == "get_issue_by_key":
            issue_key = arguments.get("issue_key")
            if not issue_key:
                return [TextContent(type="text", text="Error: issue_key is required")]

            url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                auth=HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_TOKEN),
            )

            if response.ok:
                return [TextContent(type="text", text=str(response.json()))]
            else:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: {response.status_code} - {response.text}",
                    )
                ]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
