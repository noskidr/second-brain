# Asana Daily Summary

Automated daily summary generator for the **Ideon Scraping Internal** Asana board with optional Claude post-processing and ClickUp integration.

## Quick Start

```bash
# Raw report only (default)
./asana_daily_summary.sh

# With Claude post-processing (deduplicates entries)
./asana_daily_summary.sh -p

# Post to ClickUp #Scraping channel
./asana_daily_summary.sh -c

# All options (process + ClickUp)
./asana_daily_summary.sh -a

# Help
./asana_daily_summary.sh --help
```

## Output

Reports are saved to `asana_daily_summary/{YYYY-MM-DD}.md`

### Sample Output

```
📊 Ideon Scraping Internal - Daily Summary
   Generated: Jan 13, 2026 06:02:55
   Period: Last 24 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COMPLETED/APPROVED
   • Baylor Scott and White → Internal Approved (Rohit Dangol)
   • BCBS IL → Approved (Dikson Rajbanshi)
   ...

🔄 PROGRESSING
   • Anthem → Scraping (Dikson Rajbanshi)
   ...

⚠️  ISSUES FOUND
   • Emblem Health → Scrape Error (Dikson Rajbanshi)
   ...

🔧 FIXES IN PROGRESS
   • BCBS TX → Internal Approved (Rohit Dangol)
   ...

🚨 OVERDUE TASKS
• QualCare (QA Fixes in Progress) - 11 days overdue → ⚠️ Unassigned
...

📋 WORKLOAD DISTRIBUTION (Active Tasks)
   Assignee             │ Tasks │ Breakdown
   ─────────────────────┼───────┼─────────────────────────────────
   ⚠️ Unassigned        │     7 │ 1 Coding, 1 QA Fixes, 3 Scraping
   ...

👥 USER ACTIVITY (Last 24h)
   Dikson Rajbanshi      48 actions
   ...
```

## Sections

| Section | Description |
|---------|-------------|
| **COMPLETED/APPROVED** | Tasks moved to Internal Approved, Submitted, or Approved |
| **PROGRESSING** | Tasks moving forward (Coding, Scraping, QA) |
| **ISSUES FOUND** | Tasks moved to Scrape Error or QA Error |
| **FIXES IN PROGRESS** | Tasks returning from error states |
| **OVERDUE TASKS** | Past due (excludes Submitted/Approved stages) |
| **WORKLOAD DISTRIBUTION** | Active tasks per assignee |
| **USER ACTIVITY** | Action count per user in last 24h |

## Cron Schedule

Runs daily at **8:00 AM** with all options enabled:

```
0 8 * * * /Users/dikson/Work/second_brain/asana_daily_summary_cron.sh
```

### Cron Logs

```bash
# View recent logs
tail -100 asana_daily_summary/cron.log

# Watch live
tail -f asana_daily_summary/cron.log
```

### Manage Cron

```bash
# View current crontab
crontab -l

# Edit crontab
crontab -e

# Remove all cron jobs
crontab -r
```

## Configuration

### Environment Variables

Required in `~/.claude/.env`:

```bash
# Asana
ASANA_ACCESS_TOKEN=your_asana_token

# ClickUp
CLICKUP_API_TOKEN=pk_your_clickup_token
```

### Asana IDs

| Resource | GID |
|----------|-----|
| Workspace | `1200807498271803` |
| Project (Ideon Scraping Internal) | `1208639428824137` |

### ClickUp IDs

| Resource | ID |
|----------|-----|
| Workspace | `9017490901` |
| #Scraping Channel | `8cqqzen-1397` |

## Files

```
second_brain/
├── asana_daily_summary.sh          # Main script
├── asana_daily_summary_cron.sh     # Cron wrapper
├── asana_daily_summary/            # Output directory
│   ├── 2026-01-13.md              # Daily reports
│   └── cron.log                   # Cron execution logs
├── .claude/
│   └── skills/
│       ├── asana/                 # Asana API skill
│       └── clickup/               # ClickUp API skill
└── README.md                      # This file
```

## Skills

Project-specific skills are in `.claude/skills/`:

### Asana Skill

API documentation for Asana REST API v2:
- Tasks, Projects, Sections
- Stories (comments & activity)
- Custom Fields, Tags
- Webhooks

### ClickUp Skill

API documentation for ClickUp API v2/v3:
- Tasks, Lists, Spaces
- Chat Channels & Messages (v3)
- Time Tracking, Goals
- Webhooks

## Troubleshooting

### Cron not running

1. Check cron is installed: `crontab -l`
2. Check logs: `tail asana_daily_summary/cron.log`
3. Test wrapper: `./asana_daily_summary_cron.sh`

### Missing environment variables

```bash
# Test Asana token
curl -s "https://app.asana.com/api/1.0/users/me" \
  -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" | jq

# Test ClickUp token
curl -s "https://api.clickup.com/api/v2/team" \
  -H "Authorization: $CLICKUP_API_TOKEN" | jq
```

### Claude not found in cron

Ensure PATH is set in the cron wrapper script or add Claude to system PATH.
