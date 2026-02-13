# AI Release Notes MCP Server

This project is an MCP (Model Context Protocol) server for building release notes by integrating with JIRA. It exposes JIRA API functionality as MCP tools that can be used by AI assistants like Claude.

## Features

- **get_jira_fields**: Get all available JIRA fields
- **get_project_keys**: Get all JIRA project keys in your workspace
- **get_jira_issues**: Get JIRA issues for a specific project
- **get_issue_by_key**: Get detailed information about a specific issue

## Setup

### Prerequisites

- Python 3.10+
- [uv package manager](https://github.com/astral-sh/uv)

### Installation

1. Install dependencies with uv:
   ```bash
   uv sync --extra dev
   ```

2. Create a `.env` file with your JIRA credentials:
   ```bash
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_API_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   PROJECT_KEY=SCRUM
   ```

### Running the Server

The MCP server runs via stdio and is meant to be configured in an MCP client like Claude Desktop.

#### Configure in Claude Desktop

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "release-notes": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/elizabethporter/coding/release_notes_the_kraken",
        "run",
        "python",
        "-m",
        "release_notes_the_kraken.server"
      ]
    }
  }
}
```

#### Run Locally

To run the server locally:
```bash
uv run python -m release_notes_the_kraken.server
```

## Development

Install pre-commit hooks:
```bash
uv tool install pre-commit
pre-commit install
```

## JIRA API Setup

To get your JIRA API token:
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token
4. Add it to your `.env` file