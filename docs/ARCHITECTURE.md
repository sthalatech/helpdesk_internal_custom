# Architecture Overview

## App Structure

```
helpdesk_internal_custom/
├── helpdesk_internal_custom/
│   ├── __init__.py
│   ├── hooks.py              # App configuration and hooks
│   ├── install.py            # Post-installation setup
│   ├── permissions.py        # Permission logic
│   ├── modules.txt           # Module definition
│   ├── api/                  # Custom API endpoints
│   │   ├── __init__.py
│   │   └── ticket.py         # Ticket-related APIs
│   ├── overrides/            # Document class overrides
│   │   ├── __init__.py
│   │   └── ticket.py         # HD Ticket hooks
│   ├── custom_fields/        # Field definitions
│   │   └── __init__.py
│   ├── fixtures/             # Pre-built data
│   │   ├── team.json
│   │   ├── user.json
│   │   ├── role.json
│   │   └── custom_field.json
│   ├── patches/              # Migration scripts
│   │   └── __init__.py
│   └── public/               # Static assets
├── docs/                     # Documentation
├── pyproject.toml
└── README.md
```

## Permission Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        HD Ticket                                 │
├─────────────────────────────────────────────────────────────────┤
│  originating_team  │  assigned_team  │  Who can access          │
├─────────────────────────────────────────────────────────────────┤
│  Team A           │  Team B         │  Team A: Read-only        │
│                   │                 │  Team B: Full access      │
│                   │                 │  Admin: Full access       │
└─────────────────────────────────────────────────────────────────┘
```

## Role Hierarchy

1. **Helpdesk Admin Internal** - Full access to all tickets
2. **Helpdesk Manager Internal** - Team manager, can assign within team
3. **Helpdesk User Internal** - Basic agent, works on team tickets

## Data Flow

```
User creates ticket
       │
       ▼
before_insert hook sets originating_team = user's team
       │
       ▼
Ticket saved with:
- originating_team: Creator's team
- assigned_team: Selected target team
       │
       ▼
Permission checks filter access:
- Agent view: assigned_team matches
- Customer view: originating_team matches
```
