---
name: asana
description: Asana REST API integration for tasks, projects, workspaces, teams, and project management
allowed-tools: [Bash, Read, Write]
---

# Asana API Skill

Interact with Asana's REST API v1.0 for task management, project organization, and team collaboration.

## When to Use

- Create, read, update, delete tasks in Asana
- Manage projects, sections, and workspaces
- Organize teams and team memberships
- Track goals and progress
- Add comments (stories) to tasks
- Manage tags, custom fields, and attachments
- Set up webhooks for real-time notifications
- Search and filter tasks

## Authentication

Asana supports multiple authentication methods:

### Personal Access Token (PAT) - Recommended for scripts

1. Log into Asana → Profile Settings → Apps → Developer apps
2. Create a personal access token
3. Set environment variable:

```bash
export ASANA_ACCESS_TOKEN="your_token_here"
```

Or add to `~/.claude/.env`:
```
ASANA_ACCESS_TOKEN=your_token_here
```

### Service Account (Enterprise only)

For organization-wide API access. Only Asana super admins can create them.

### OAuth 2.0 (For multi-user apps)

Authorization URL: `https://app.asana.com/-/oauth_authorize`
Token endpoint: `https://app.asana.com/-/oauth_token`

## API Base URL

```
https://app.asana.com/api/1.0
```

## Rate Limits

Asana uses rate limiting to ensure API stability. When rate limited, you'll receive a 429 status code. Implement exponential backoff for retries.

## Quick Start

```bash
# Set your token
export ASANA_ACCESS_TOKEN="your_token"

# Get current user
curl -s "https://app.asana.com/api/1.0/users/me" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq

# Get workspaces
curl -s "https://app.asana.com/api/1.0/workspaces" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq

# Get projects in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq
```

## Core Endpoints

### Users

```bash
# Get current user
curl -s "https://app.asana.com/api/1.0/users/me" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a specific user
curl -s "https://app.asana.com/api/1.0/users/{user_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get users in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/users" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get users in a team
curl -s "https://app.asana.com/api/1.0/teams/{team_gid}/users" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Workspaces

```bash
# Get all workspaces
curl -s "https://app.asana.com/api/1.0/workspaces" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Update a workspace
curl -X PUT "https://app.asana.com/api/1.0/workspaces/{workspace_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Updated Workspace Name"}}'
```

### Teams

```bash
# Get teams in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/teams" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a team
curl -s "https://app.asana.com/api/1.0/teams/{team_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a team
curl -X POST "https://app.asana.com/api/1.0/teams" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "New Team",
      "organization": "{workspace_gid}"
    }
  }'

# Add user to team
curl -X POST "https://app.asana.com/api/1.0/teams/{team_gid}/addUser" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"user": "{user_gid}"}}'

# Remove user from team
curl -X POST "https://app.asana.com/api/1.0/teams/{team_gid}/removeUser" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"user": "{user_gid}"}}'
```

### Projects

```bash
# Get projects (with optional filters)
curl -s "https://app.asana.com/api/1.0/projects?workspace={workspace_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get projects in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get projects for a team
curl -s "https://app.asana.com/api/1.0/teams/{team_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a project
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a project in a workspace
curl -X POST "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "New Project",
      "notes": "Project description",
      "color": "light-green",
      "default_view": "list"
    }
  }'

# Create a project for a team
curl -X POST "https://app.asana.com/api/1.0/teams/{team_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Team Project",
      "notes": "Project for the team"
    }
  }'

# Update a project
curl -X PUT "https://app.asana.com/api/1.0/projects/{project_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Updated Project Name",
      "archived": false
    }
  }'

# Delete a project
curl -X DELETE "https://app.asana.com/api/1.0/projects/{project_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Duplicate a project
curl -X POST "https://app.asana.com/api/1.0/projects/{project_gid}/duplicate" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Copy of Project",
      "include": ["members", "task_notes", "task_assignee", "task_subtasks"]
    }
  }'
```

### Sections

```bash
# Get sections in a project
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/sections" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a section
curl -s "https://app.asana.com/api/1.0/sections/{section_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a section in a project
curl -X POST "https://app.asana.com/api/1.0/projects/{project_gid}/sections" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "New Section"}}'

# Update a section
curl -X PUT "https://app.asana.com/api/1.0/sections/{section_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Updated Section Name"}}'

# Delete a section
curl -X DELETE "https://app.asana.com/api/1.0/sections/{section_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add task to section
curl -X POST "https://app.asana.com/api/1.0/sections/{section_gid}/addTask" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"task": "{task_gid}"}}'

# Move/reorder sections
curl -X POST "https://app.asana.com/api/1.0/projects/{project_gid}/sections/insert" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "section": "{section_gid}",
      "before_section": "{other_section_gid}"
    }
  }'
```

### Tasks

```bash
# Get tasks in a project
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get tasks in a section
curl -s "https://app.asana.com/api/1.0/sections/{section_gid}/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a task
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a task
curl -X POST "https://app.asana.com/api/1.0/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "New Task",
      "notes": "Task description",
      "workspace": "{workspace_gid}",
      "projects": ["{project_gid}"],
      "assignee": "{user_gid}",
      "due_on": "2026-01-31",
      "tags": ["{tag_gid}"]
    }
  }'

# Create a task in a project
curl -X POST "https://app.asana.com/api/1.0/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Project Task",
      "projects": ["{project_gid}"]
    }
  }'

# Update a task
curl -X PUT "https://app.asana.com/api/1.0/tasks/{task_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Updated Task Name",
      "completed": true,
      "due_on": "2026-02-15"
    }
  }'

# Delete a task
curl -X DELETE "https://app.asana.com/api/1.0/tasks/{task_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Duplicate a task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/duplicate" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Copy of Task",
      "include": ["notes", "assignee", "subtasks", "attachments", "tags"]
    }
  }'

# Search tasks in workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tasks/search?text=search_term" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Search with filters
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tasks/search?assignee.any={user_gid}&completed=false&due_on.before=2026-02-01" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Subtasks

```bash
# Get subtasks of a task
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/subtasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a subtask
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/subtasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "New Subtask",
      "notes": "Subtask description"
    }
  }'

# Set parent task (make task a subtask)
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/setParent" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"parent": "{parent_task_gid}"}}'
```

### Dependencies

```bash
# Get dependencies of a task
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/dependencies" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add dependencies (tasks this task depends on)
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/addDependencies" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"dependencies": ["{dependency_task_gid}"]}}'

# Remove dependencies
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/removeDependencies" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"dependencies": ["{dependency_task_gid}"]}}'

# Get dependents (tasks that depend on this task)
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/dependents" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add dependents
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/addDependents" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"dependents": ["{dependent_task_gid}"]}}'
```

### Task Projects and Tags

```bash
# Get projects a task is in
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add task to a project
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/addProject" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "project": "{project_gid}",
      "section": "{section_gid}"
    }
  }'

# Remove task from project
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/removeProject" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"project": "{project_gid}"}}'

# Get task's tags
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/tags" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add tag to task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/addTag" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"tag": "{tag_gid}"}}'

# Remove tag from task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/removeTag" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"tag": "{tag_gid}"}}'
```

### Task Followers

```bash
# Add followers to a task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/addFollowers" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"followers": ["{user_gid}"]}}'

# Remove follower from task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/removeFollower" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"follower": "{user_gid}"}}'
```

### Tags

```bash
# Get tags in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tags" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a tag
curl -s "https://app.asana.com/api/1.0/tags/{tag_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a tag
curl -X POST "https://app.asana.com/api/1.0/tags" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "New Tag",
      "color": "light-blue",
      "workspace": "{workspace_gid}"
    }
  }'

# Create tag in workspace
curl -X POST "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tags" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Workspace Tag", "color": "dark-purple"}}'

# Update a tag
curl -X PUT "https://app.asana.com/api/1.0/tags/{tag_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Updated Tag Name", "color": "dark-green"}}'

# Delete a tag
curl -X DELETE "https://app.asana.com/api/1.0/tags/{tag_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get tasks with a tag
curl -s "https://app.asana.com/api/1.0/tags/{tag_gid}/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Stories (Comments & Activity)

```bash
# Get stories for a task (comments and activity)
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/stories" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a specific story
curl -s "https://app.asana.com/api/1.0/stories/{story_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a comment on a task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/stories" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"text": "This is a comment on the task"}}'

# Update a story (edit comment)
curl -X PUT "https://app.asana.com/api/1.0/stories/{story_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"text": "Updated comment text"}}'

# Delete a story
curl -X DELETE "https://app.asana.com/api/1.0/stories/{story_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Goals

```bash
# Get goals (with optional filters)
curl -s "https://app.asana.com/api/1.0/goals?workspace={workspace_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a goal
curl -s "https://app.asana.com/api/1.0/goals/{goal_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a goal
curl -X POST "https://app.asana.com/api/1.0/goals" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Q1 Revenue Goal",
      "notes": "Achieve 1M in revenue",
      "workspace": "{workspace_gid}",
      "due_on": "2026-03-31",
      "start_on": "2026-01-01",
      "is_workspace_level": true
    }
  }'

# Update a goal
curl -X PUT "https://app.asana.com/api/1.0/goals/{goal_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Updated Goal Name",
      "status": "green"
    }
  }'

# Delete a goal
curl -X DELETE "https://app.asana.com/api/1.0/goals/{goal_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Add collaborator to goal
curl -X POST "https://app.asana.com/api/1.0/goals/{goal_gid}/addFollowers" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"followers": ["{user_gid}"]}}'
```

### Custom Fields

```bash
# Get custom fields in a workspace
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/custom_fields" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get custom fields for a project
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/custom_field_settings" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a custom field
curl -s "https://app.asana.com/api/1.0/custom_fields/{custom_field_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a custom field
curl -X POST "https://app.asana.com/api/1.0/custom_fields" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Priority Level",
      "resource_subtype": "enum",
      "workspace": "{workspace_gid}",
      "enum_options": [
        {"name": "Low", "color": "blue"},
        {"name": "Medium", "color": "yellow"},
        {"name": "High", "color": "red"}
      ]
    }
  }'

# Add custom field to project
curl -X POST "https://app.asana.com/api/1.0/projects/{project_gid}/addCustomFieldSetting" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"custom_field": "{custom_field_gid}"}}'
```

### Attachments

```bash
# Get attachments for a task
curl -s "https://app.asana.com/api/1.0/tasks/{task_gid}/attachments" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get an attachment
curl -s "https://app.asana.com/api/1.0/attachments/{attachment_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Upload attachment to a task
curl -X POST "https://app.asana.com/api/1.0/tasks/{task_gid}/attachments" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -F "file=@/path/to/file.pdf" \
  -F "name=document.pdf"

# Delete an attachment
curl -X DELETE "https://app.asana.com/api/1.0/attachments/{attachment_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Webhooks

```bash
# Get webhooks for a workspace
curl -s "https://app.asana.com/api/1.0/webhooks?workspace={workspace_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Get a webhook
curl -s "https://app.asana.com/api/1.0/webhooks/{webhook_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Create a webhook
curl -X POST "https://app.asana.com/api/1.0/webhooks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "resource": "{project_gid}",
      "target": "https://your-server.com/webhook",
      "filters": [
        {"resource_type": "task", "action": "changed"}
      ]
    }
  }'

# Update a webhook
curl -X PUT "https://app.asana.com/api/1.0/webhooks/{webhook_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "filters": [
        {"resource_type": "task", "action": "added"},
        {"resource_type": "task", "action": "removed"}
      ]
    }
  }'

# Delete a webhook
curl -X DELETE "https://app.asana.com/api/1.0/webhooks/{webhook_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

### Batch API

```bash
# Execute multiple requests in parallel
curl -X POST "https://app.asana.com/api/1.0/batch" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "actions": [
        {
          "method": "get",
          "relative_path": "/users/me"
        },
        {
          "method": "get",
          "relative_path": "/workspaces"
        }
      ]
    }
  }'
```

## Pagination

Asana uses offset-based pagination for list endpoints:

```bash
# First page (default limit is 20, max is 100)
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/tasks?limit=50" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"

# Next page (use offset from previous response)
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/tasks?limit=50&offset={offset_token}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN"
```

Response includes `next_page` object when more results exist:
```json
{
  "data": [...],
  "next_page": {
    "offset": "eyJ0...",
    "path": "/projects/123/tasks?offset=eyJ0...",
    "uri": "https://app.asana.com/api/1.0/projects/123/tasks?offset=eyJ0..."
  }
}
```

## Common Workflows

### Find your workspace, team, and project IDs

```bash
# 1. Get workspaces
curl -s "https://app.asana.com/api/1.0/workspaces" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq '.data[] | {gid, name}'

# 2. Get teams in workspace (use workspace_gid from step 1)
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/teams" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq '.data[] | {gid, name}'

# 3. Get projects for team (use team_gid from step 2)
curl -s "https://app.asana.com/api/1.0/teams/{team_gid}/projects" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq '.data[] | {gid, name}'

# 4. Get sections in project (use project_gid from step 3)
curl -s "https://app.asana.com/api/1.0/projects/{project_gid}/sections" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq '.data[] | {gid, name}'
```

### Create a task with full details

```bash
curl -X POST "https://app.asana.com/api/1.0/tasks" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Important Task",
      "notes": "This is the task description with details",
      "workspace": "{workspace_gid}",
      "projects": ["{project_gid}"],
      "memberships": [
        {
          "project": "{project_gid}",
          "section": "{section_gid}"
        }
      ],
      "assignee": "{user_gid}",
      "due_on": "2026-01-31",
      "start_on": "2026-01-15",
      "tags": ["{tag_gid}"],
      "followers": ["{follower_user_gid}"]
    }
  }'
```

### Move task to different section

```bash
curl -X POST "https://app.asana.com/api/1.0/sections/{section_gid}/addTask" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"task": "{task_gid}"}}'
```

### Get all incomplete tasks assigned to me

```bash
curl -s "https://app.asana.com/api/1.0/workspaces/{workspace_gid}/tasks/search?assignee.any=me&completed=false" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq
```

### Mark task as complete

```bash
curl -X PUT "https://app.asana.com/api/1.0/tasks/{task_gid}" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"completed": true}}'
```

## Resource Subtypes

### Task Types
| Value | Description |
|-------|-------------|
| default_task | Regular task |
| approval | Approval task |
| milestone | Milestone |

### Custom Field Types
| Value | Description |
|-------|-------------|
| text | Text field |
| number | Numeric field |
| enum | Single-select dropdown |
| multi_enum | Multi-select dropdown |
| date | Date field |
| people | People picker |

### Tag Colors
Available colors: `dark-pink`, `dark-green`, `dark-blue`, `dark-red`, `dark-teal`, `dark-brown`, `dark-orange`, `dark-purple`, `dark-warm-gray`, `light-pink`, `light-green`, `light-blue`, `light-red`, `light-teal`, `light-brown`, `light-orange`, `light-purple`, `light-warm-gray`, or `null`

### Goal Status
- Open goals: `green`, `yellow`, `red`
- Closed goals: `achieved`, `partial`, `missed`, `dropped`

## Error Handling

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (check parameters) |
| 401 | Unauthorized (check token) |
| 402 | Payment required (premium feature) |
| 403 | Forbidden (no permission) |
| 404 | Resource not found |
| 429 | Rate limited |
| 451 | Blocked (legal reasons) |
| 500 | Server error |

Error response format:
```json
{
  "errors": [
    {
      "message": "workspace: Missing input",
      "phrase": "6 sad squid snuggle softly"
    }
  ]
}
```

The `phrase` field (for 500 errors) is useful when contacting Asana support.

---

## API Reference

Full documentation: https://developers.asana.com/reference/rest-api-reference

Key sections:
- Authentication: https://developers.asana.com/docs/authentication
- Pagination: https://developers.asana.com/docs/pagination
- Errors: https://developers.asana.com/docs/errors
- Tasks: https://developers.asana.com/reference/tasks
- Projects: https://developers.asana.com/reference/projects
- Webhooks: https://developers.asana.com/reference/webhooks
