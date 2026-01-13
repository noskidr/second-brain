---
name: clickup
description: ClickUp API integration for tasks, lists, spaces, and project management
allowed-tools: [Bash, Read, Write]
---

# ClickUp API Skill

Interact with ClickUp's API v2 for task management, project organization, and team collaboration.

## When to Use

- Create, read, update, delete tasks in ClickUp
- Manage lists, folders, and spaces
- Track time entries
- Create and manage webhooks
- Interact with goals and custom fields
- Search and filter tasks

## Authentication

ClickUp supports two authentication methods:

### Personal API Token (Recommended for personal use)

1. Log into ClickUp → Settings (avatar) → Apps → API Token
2. Generate or copy your token (starts with `pk_`)
3. Set environment variable:

```bash
export CLICKUP_API_TOKEN="pk_your_token_here"
```

Or add to `~/.claude/.env`:
```
CLICKUP_API_TOKEN=pk_your_token_here
```

### OAuth 2.0 (For apps serving multiple users)

1. Create OAuth app: Settings → Apps → Create new app
2. Authorization URL: `https://app.clickup.com/api?client_id={client_id}&redirect_uri={redirect_uri}`
3. Token endpoint: `POST https://api.clickup.com/api/v2/oauth/token`

## API Base URLs

```
v2: https://api.clickup.com/api/v2
v3: https://api.clickup.com/api/v3
```

## Rate Limits

| Plan | Limit |
|------|-------|
| Free/Unlimited/Business | 100 requests/min |
| Business Plus | 1,000 requests/min |
| Enterprise | 10,000 requests/min |

Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Quick Start

```bash
# Set your token
export CLICKUP_API_TOKEN="pk_your_token"

# Get workspaces
curl -s "https://api.clickup.com/api/v2/team" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq

# Get spaces in a workspace
curl -s "https://api.clickup.com/api/v2/team/{team_id}/space" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq
```

## Core Endpoints

### Workspaces (Teams)

```bash
# Get authorized workspaces
curl -s "https://api.clickup.com/api/v2/team" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Spaces

```bash
# Get spaces in workspace
curl -s "https://api.clickup.com/api/v2/team/{team_id}/space" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create space
curl -X POST "https://api.clickup.com/api/v2/team/{team_id}/space" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Space"}'
```

### Folders

```bash
# Get folders in space
curl -s "https://api.clickup.com/api/v2/space/{space_id}/folder" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create folder
curl -X POST "https://api.clickup.com/api/v2/space/{space_id}/folder" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Folder"}'
```

### Lists

```bash
# Get lists in folder
curl -s "https://api.clickup.com/api/v2/folder/{folder_id}/list" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get folderless lists in space
curl -s "https://api.clickup.com/api/v2/space/{space_id}/list" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create list
curl -X POST "https://api.clickup.com/api/v2/folder/{folder_id}/list" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New List"}'
```

### Tasks

```bash
# Get tasks in list (paginated, 100 per page)
curl -s "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get single task
curl -s "https://api.clickup.com/api/v2/task/{task_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create task
curl -X POST "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Task Name",
    "description": "Task description",
    "status": "to do",
    "priority": 3,
    "due_date": 1609459200000,
    "assignees": [123456]
  }'

# Update task
curl -X PUT "https://api.clickup.com/api/v2/task/{task_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "status": "in progress"}'

# Delete task
curl -X DELETE "https://api.clickup.com/api/v2/task/{task_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Comments

```bash
# Get task comments
curl -s "https://api.clickup.com/api/v2/task/{task_id}/comment" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create task comment
curl -X POST "https://api.clickup.com/api/v2/task/{task_id}/comment" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment_text": "This is a comment"}'
```

### Time Tracking

```bash
# Get time entries (last 30 days by default)
curl -s "https://api.clickup.com/api/v2/team/{team_id}/time_entries" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get time entries with filters
curl -s "https://api.clickup.com/api/v2/team/{team_id}/time_entries?start_date=1609459200000&end_date=1612137600000" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Filter by location (only one allowed)
curl -s "https://api.clickup.com/api/v2/team/{team_id}/time_entries?task_id={task_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Goals

```bash
# Get goals in workspace
curl -s "https://api.clickup.com/api/v2/team/{team_id}/goal" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create goal
curl -X POST "https://api.clickup.com/api/v2/team/{team_id}/goal" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 Goals",
    "due_date": 1617235200000,
    "description": "Goals for Q1"
  }'
```

### Custom Fields

```bash
# Get custom fields for a list
curl -s "https://api.clickup.com/api/v2/list/{list_id}/field" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Webhooks

```bash
# Get webhooks
curl -s "https://api.clickup.com/api/v2/team/{team_id}/webhook" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create webhook
curl -X POST "https://api.clickup.com/api/v2/team/{team_id}/webhook" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "https://your-server.com/webhook",
    "events": ["taskCreated", "taskUpdated", "taskDeleted"]
  }'

# Delete webhook
curl -X DELETE "https://api.clickup.com/api/v2/webhook/{webhook_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

## Using the Python Script

For more complex operations, use the included Python script:

```bash
cd ~/.claude/skills/clickup && python scripts/clickup_api.py \
  --action get-workspaces

cd ~/.claude/skills/clickup && python scripts/clickup_api.py \
  --action get-tasks \
  --list-id "your_list_id"

cd ~/.claude/skills/clickup && python scripts/clickup_api.py \
  --action create-task \
  --list-id "your_list_id" \
  --name "New Task" \
  --description "Task description"
```

### Script Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `get-workspaces` | - | List all accessible workspaces |
| `get-spaces` | `--team-id` | List spaces in workspace |
| `get-folders` | `--space-id` | List folders in space |
| `get-lists` | `--folder-id` OR `--space-id` | List lists |
| `get-tasks` | `--list-id` | Get tasks in list |
| `get-task` | `--task-id` | Get single task details |
| `create-task` | `--list-id`, `--name` | Create new task |
| `update-task` | `--task-id` | Update existing task |
| `delete-task` | `--task-id` | Delete task |
| `get-time-entries` | `--team-id` | Get time tracking entries |
| `get-goals` | `--team-id` | Get workspace goals |

## Common Workflows

### Find your workspace and list IDs

```bash
# 1. Get workspaces
curl -s "https://api.clickup.com/api/v2/team" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq '.teams[] | {id, name}'

# 2. Get spaces (use team_id from step 1)
curl -s "https://api.clickup.com/api/v2/team/{team_id}/space" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq '.spaces[] | {id, name}'

# 3. Get folders (use space_id from step 2)
curl -s "https://api.clickup.com/api/v2/space/{space_id}/folder" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq '.folders[] | {id, name}'

# 4. Get lists (use folder_id from step 3)
curl -s "https://api.clickup.com/api/v2/folder/{folder_id}/list" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq '.lists[] | {id, name}'
```

### Create a task with full details

```bash
curl -X POST "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Important Task",
    "description": "This is the task description with **markdown** support",
    "status": "to do",
    "priority": 1,
    "due_date": 1704067200000,
    "due_date_time": true,
    "start_date": 1703980800000,
    "start_date_time": true,
    "assignees": [123456],
    "tags": ["urgent", "feature"],
    "notify_all": false
  }'
```

### Priority Values

| Value | Priority |
|-------|----------|
| 1 | Urgent |
| 2 | High |
| 3 | Normal |
| 4 | Low |

## Error Handling

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (check parameters) |
| 401 | Unauthorized (check token) |
| 403 | Forbidden (no permission) |
| 404 | Resource not found |
| 429 | Rate limited (check headers) |
| 500 | Server error |

---

## ClickUp Public API v3

The v3 API provides additional features for Chat, Docs, Privacy/Access, and Audit Logs.

### Chat - Channels

```bash
# Get all channels in workspace
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get a specific channel
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create a channel
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Channel"}'

# Create channel on Space, Folder, or List
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/location" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"location_id": "123", "location_type": "space"}'

# Create direct message channel
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/dm" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member_ids": [123, 456]}'

# Update a channel
curl -X PATCH "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Channel Name"}'

# Delete a channel
curl -X DELETE "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get channel followers
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/followers" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get channel members
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/members" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Chat - Messages

```bash
# Get channel messages
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Send a message
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from API!"}'

# Update a message
curl -X PATCH "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated message"}'

# Delete a message
curl -X DELETE "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get message reactions
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/reactions" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create message reaction
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/reactions" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reaction": "thumbsup"}'

# Delete message reaction
curl -X DELETE "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/reactions/{reaction_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get message replies
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/replies" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create reply message
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/replies" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a reply"}'

# Get tagged users in message
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages/{message_id}/tagged" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get post subtype IDs
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/chat/subtypes" \
  -H "Authorization: $CLICKUP_API_TOKEN"
```

### Docs

```bash
# Search for docs in workspace
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs?query=search_term" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create a doc
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Doc", "parent_id": "123", "parent_type": "space"}'

# Get a doc
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get doc page listing
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pagelisting" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Get all pages in doc
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Create a page in doc
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Page", "content": "Page content here"}'

# Get a specific page
curl -s "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN"

# Edit a page
curl -X PUT "https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Page", "content": "Updated content"}'
```

### Privacy and Access

```bash
# Update privacy and access of an object or location
curl -X PATCH "https://api.clickup.com/api/v3/workspaces/{workspace_id}/acl" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "object_id": "123",
    "object_type": "task",
    "access_level": "private"
  }'
```

### Audit Logs

```bash
# Create workspace-level audit logs query
curl -X POST "https://api.clickup.com/api/v3/workspaces/{workspace_id}/audit" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": 1609459200000,
    "end_date": 1612137600000,
    "event_types": ["task_created", "task_updated"]
  }'
```

### Tasks (v3)

```bash
# Move task to a new list
curl -X PUT "https://api.clickup.com/api/v3/task/{task_id}/move" \
  -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"list_id": "new_list_id"}'
```

---

## v3 API Endpoint Reference

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v3/workspaces/{id}/chat/channels` | Retrieve channels |
| POST | `/v3/workspaces/{id}/chat/channels` | Create channel |
| POST | `/v3/workspaces/{id}/chat/channels/location` | Create channel on location |
| POST | `/v3/workspaces/{id}/chat/channels/dm` | Create direct message |
| GET | `/v3/workspaces/{id}/chat/channels/{channel_id}` | Retrieve a channel |
| PATCH | `/v3/workspaces/{id}/chat/channels/{channel_id}` | Update channel |
| DELETE | `/v3/workspaces/{id}/chat/channels/{channel_id}` | Delete channel |
| GET | `.../{channel_id}/followers` | Get channel followers |
| GET | `.../{channel_id}/members` | Get channel members |
| GET | `.../{channel_id}/messages` | Get messages |
| POST | `.../{channel_id}/messages` | Send message |
| PATCH | `.../{message_id}` | Update message |
| DELETE | `.../{message_id}` | Delete message |
| GET | `.../{message_id}/reactions` | Get reactions |
| POST | `.../{message_id}/reactions` | Create reaction |
| DELETE | `.../{reaction_id}` | Delete reaction |
| GET | `.../{message_id}/replies` | Get replies |
| POST | `.../{message_id}/replies` | Create reply |
| GET | `.../{message_id}/tagged` | Get tagged users |
| GET | `/v3/workspaces/{id}/chat/subtypes` | Get post subtypes |

### Docs Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v3/workspaces/{id}/docs` | Search docs |
| POST | `/v3/workspaces/{id}/docs` | Create doc |
| GET | `/v3/workspaces/{id}/docs/{doc_id}` | Fetch doc |
| GET | `.../{doc_id}/pagelisting` | Fetch page listing |
| GET | `.../{doc_id}/pages` | Fetch pages |
| POST | `.../{doc_id}/pages` | Create page |
| GET | `.../{doc_id}/pages/{page_id}` | Get page |
| PUT | `.../{doc_id}/pages/{page_id}` | Edit page |

### Other v3 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| PATCH | `/v3/workspaces/{id}/acl` | Update privacy/access |
| POST | `/v3/workspaces/{id}/audit` | Create audit logs query |
| PUT | `/v3/task/{task_id}/move` | Move task to new list |

---

## API Reference

Full documentation: https://developer.clickup.com/reference/

Key sections:
- Authentication: https://developer.clickup.com/docs/authentication
- Tasks (v2): https://developer.clickup.com/reference/gettasks
- Webhooks: https://developer.clickup.com/reference/createwebhook
- Time Tracking: https://developer.clickup.com/reference/gettimeentrieswithinadaterange
- Chat (v3): https://developer.clickup.com/reference/getchatchannels
- Docs (v3): https://developer.clickup.com/reference/searchdocspublic
