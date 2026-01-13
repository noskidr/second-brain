#!/usr/bin/env python3
"""ClickUp API client for Claude Code skill.

Provides a command-line interface to interact with ClickUp's API v2.

Usage:
    python clickup_api.py --action get-workspaces
    python clickup_api.py --action get-tasks --list-id "123456"
    python clickup_api.py --action create-task --list-id "123456" --name "New Task"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


BASE_URL = "https://api.clickup.com/api/v2"


def get_api_token() -> str:
    """Get ClickUp API token from environment or .env file."""
    token = os.environ.get("CLICKUP_API_TOKEN")
    if token:
        return token

    # Try loading from ~/.claude/.env
    env_file = Path.home() / ".claude" / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("CLICKUP_API_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    print("Error: CLICKUP_API_TOKEN not found in environment or ~/.claude/.env", file=sys.stderr)
    sys.exit(1)


def make_request(
    method: str,
    endpoint: str,
    data: dict[str, Any] | None = None,
    params: dict[str, str] | None = None
) -> dict[str, Any]:
    """Make HTTP request to ClickUp API."""
    token = get_api_token()

    # Build URL with query parameters
    url = f"{BASE_URL}{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v)
        if query:
            url = f"{url}?{query}"

    # Prepare request
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None

    request = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(request, timeout=30) as response:
            response_data = response.read().decode()
            if response_data:
                return json.loads(response_data)
            return {"status": "success"}
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if error_body:
            try:
                error_json = json.loads(error_body)
                print(f"Error details: {json.dumps(error_json, indent=2)}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"Error body: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


# =============================================================================
# API Functions
# =============================================================================

def get_workspaces() -> dict[str, Any]:
    """Get all authorized workspaces (teams)."""
    return make_request("GET", "/team")


def get_spaces(team_id: str) -> dict[str, Any]:
    """Get spaces in a workspace."""
    return make_request("GET", f"/team/{team_id}/space")


def get_folders(space_id: str) -> dict[str, Any]:
    """Get folders in a space."""
    return make_request("GET", f"/space/{space_id}/folder")


def get_lists(folder_id: str | None = None, space_id: str | None = None) -> dict[str, Any]:
    """Get lists in a folder or space (folderless lists)."""
    if folder_id:
        return make_request("GET", f"/folder/{folder_id}/list")
    elif space_id:
        return make_request("GET", f"/space/{space_id}/list")
    else:
        raise ValueError("Either folder_id or space_id required")


def get_tasks(
    list_id: str,
    archived: bool = False,
    page: int = 0,
    subtasks: bool = False,
    include_closed: bool = False
) -> dict[str, Any]:
    """Get tasks in a list."""
    params = {
        "archived": str(archived).lower(),
        "page": str(page),
        "subtasks": str(subtasks).lower(),
        "include_closed": str(include_closed).lower(),
    }
    return make_request("GET", f"/list/{list_id}/task", params=params)


def get_task(task_id: str) -> dict[str, Any]:
    """Get a single task by ID."""
    return make_request("GET", f"/task/{task_id}")


def create_task(
    list_id: str,
    name: str,
    description: str | None = None,
    status: str | None = None,
    priority: int | None = None,
    due_date: int | None = None,
    assignees: list[int] | None = None,
    tags: list[str] | None = None
) -> dict[str, Any]:
    """Create a new task."""
    data: dict[str, Any] = {"name": name}
    if description:
        data["description"] = description
    if status:
        data["status"] = status
    if priority is not None:
        data["priority"] = priority
    if due_date:
        data["due_date"] = due_date
    if assignees:
        data["assignees"] = assignees
    if tags:
        data["tags"] = tags

    return make_request("POST", f"/list/{list_id}/task", data=data)


def update_task(
    task_id: str,
    name: str | None = None,
    description: str | None = None,
    status: str | None = None,
    priority: int | None = None,
    due_date: int | None = None
) -> dict[str, Any]:
    """Update an existing task."""
    data: dict[str, Any] = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if status:
        data["status"] = status
    if priority is not None:
        data["priority"] = priority
    if due_date:
        data["due_date"] = due_date

    if not data:
        raise ValueError("At least one field to update is required")

    return make_request("PUT", f"/task/{task_id}", data=data)


def delete_task(task_id: str) -> dict[str, Any]:
    """Delete a task."""
    return make_request("DELETE", f"/task/{task_id}")


def get_time_entries(
    team_id: str,
    start_date: int | None = None,
    end_date: int | None = None,
    task_id: str | None = None
) -> dict[str, Any]:
    """Get time tracking entries."""
    params: dict[str, str] = {}
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)
    if task_id:
        params["task_id"] = task_id

    return make_request("GET", f"/team/{team_id}/time_entries", params=params)


def get_goals(team_id: str) -> dict[str, Any]:
    """Get goals in a workspace."""
    return make_request("GET", f"/team/{team_id}/goal")


def create_comment(task_id: str, comment_text: str) -> dict[str, Any]:
    """Create a comment on a task."""
    return make_request("POST", f"/task/{task_id}/comment", data={"comment_text": comment_text})


def get_comments(task_id: str) -> dict[str, Any]:
    """Get comments on a task."""
    return make_request("GET", f"/task/{task_id}/comment")


def get_custom_fields(list_id: str) -> dict[str, Any]:
    """Get custom fields for a list."""
    return make_request("GET", f"/list/{list_id}/field")


def get_webhooks(team_id: str) -> dict[str, Any]:
    """Get webhooks for a workspace."""
    return make_request("GET", f"/team/{team_id}/webhook")


def create_webhook(team_id: str, endpoint: str, events: list[str]) -> dict[str, Any]:
    """Create a webhook."""
    return make_request("POST", f"/team/{team_id}/webhook", data={
        "endpoint": endpoint,
        "events": events
    })


def delete_webhook(webhook_id: str) -> dict[str, Any]:
    """Delete a webhook."""
    return make_request("DELETE", f"/webhook/{webhook_id}")


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="ClickUp API client")
    parser.add_argument("--action", required=True, choices=[
        "get-workspaces", "get-spaces", "get-folders", "get-lists",
        "get-tasks", "get-task", "create-task", "update-task", "delete-task",
        "get-time-entries", "get-goals",
        "create-comment", "get-comments", "get-custom-fields",
        "get-webhooks", "create-webhook", "delete-webhook"
    ], help="API action to perform")

    # ID parameters
    parser.add_argument("--team-id", help="Workspace/Team ID")
    parser.add_argument("--space-id", help="Space ID")
    parser.add_argument("--folder-id", help="Folder ID")
    parser.add_argument("--list-id", help="List ID")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--webhook-id", help="Webhook ID")

    # Task fields
    parser.add_argument("--name", help="Task name")
    parser.add_argument("--description", help="Task description")
    parser.add_argument("--status", help="Task status")
    parser.add_argument("--priority", type=int, choices=[1, 2, 3, 4],
                        help="Priority: 1=Urgent, 2=High, 3=Normal, 4=Low")
    parser.add_argument("--due-date", type=int, help="Due date (Unix ms)")
    parser.add_argument("--assignees", help="Comma-separated user IDs")
    parser.add_argument("--tags", help="Comma-separated tags")

    # Time entries
    parser.add_argument("--start-date", type=int, help="Start date (Unix ms)")
    parser.add_argument("--end-date", type=int, help="End date (Unix ms)")

    # Comments
    parser.add_argument("--comment", help="Comment text")

    # Webhooks
    parser.add_argument("--endpoint", help="Webhook endpoint URL")
    parser.add_argument("--events", help="Comma-separated webhook events")

    # Task list options
    parser.add_argument("--archived", action="store_true", help="Include archived")
    parser.add_argument("--subtasks", action="store_true", help="Include subtasks")
    parser.add_argument("--include-closed", action="store_true", help="Include closed")
    parser.add_argument("--page", type=int, default=0, help="Page number")

    # Output options
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON")

    args = parser.parse_args()

    # Execute action
    result = None

    if args.action == "get-workspaces":
        result = get_workspaces()

    elif args.action == "get-spaces":
        if not args.team_id:
            parser.error("--team-id required for get-spaces")
        result = get_spaces(args.team_id)

    elif args.action == "get-folders":
        if not args.space_id:
            parser.error("--space-id required for get-folders")
        result = get_folders(args.space_id)

    elif args.action == "get-lists":
        if not args.folder_id and not args.space_id:
            parser.error("--folder-id or --space-id required for get-lists")
        result = get_lists(args.folder_id, args.space_id)

    elif args.action == "get-tasks":
        if not args.list_id:
            parser.error("--list-id required for get-tasks")
        result = get_tasks(
            args.list_id,
            archived=args.archived,
            page=args.page,
            subtasks=args.subtasks,
            include_closed=args.include_closed
        )

    elif args.action == "get-task":
        if not args.task_id:
            parser.error("--task-id required for get-task")
        result = get_task(args.task_id)

    elif args.action == "create-task":
        if not args.list_id or not args.name:
            parser.error("--list-id and --name required for create-task")
        assignees = [int(x) for x in args.assignees.split(",")] if args.assignees else None
        tags = args.tags.split(",") if args.tags else None
        result = create_task(
            args.list_id,
            args.name,
            description=args.description,
            status=args.status,
            priority=args.priority,
            due_date=args.due_date,
            assignees=assignees,
            tags=tags
        )

    elif args.action == "update-task":
        if not args.task_id:
            parser.error("--task-id required for update-task")
        result = update_task(
            args.task_id,
            name=args.name,
            description=args.description,
            status=args.status,
            priority=args.priority,
            due_date=args.due_date
        )

    elif args.action == "delete-task":
        if not args.task_id:
            parser.error("--task-id required for delete-task")
        result = delete_task(args.task_id)

    elif args.action == "get-time-entries":
        if not args.team_id:
            parser.error("--team-id required for get-time-entries")
        result = get_time_entries(
            args.team_id,
            start_date=args.start_date,
            end_date=args.end_date,
            task_id=args.task_id
        )

    elif args.action == "get-goals":
        if not args.team_id:
            parser.error("--team-id required for get-goals")
        result = get_goals(args.team_id)

    elif args.action == "create-comment":
        if not args.task_id or not args.comment:
            parser.error("--task-id and --comment required for create-comment")
        result = create_comment(args.task_id, args.comment)

    elif args.action == "get-comments":
        if not args.task_id:
            parser.error("--task-id required for get-comments")
        result = get_comments(args.task_id)

    elif args.action == "get-custom-fields":
        if not args.list_id:
            parser.error("--list-id required for get-custom-fields")
        result = get_custom_fields(args.list_id)

    elif args.action == "get-webhooks":
        if not args.team_id:
            parser.error("--team-id required for get-webhooks")
        result = get_webhooks(args.team_id)

    elif args.action == "create-webhook":
        if not args.team_id or not args.endpoint or not args.events:
            parser.error("--team-id, --endpoint, and --events required for create-webhook")
        events = args.events.split(",")
        result = create_webhook(args.team_id, args.endpoint, events)

    elif args.action == "delete-webhook":
        if not args.webhook_id:
            parser.error("--webhook-id required for delete-webhook")
        result = delete_webhook(args.webhook_id)

    # Output result
    if result:
        indent = 2 if args.pretty else None
        print(json.dumps(result, indent=indent))


if __name__ == "__main__":
    main()
