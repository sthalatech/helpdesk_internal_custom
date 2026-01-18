# Helpdesk Internal Custom

Custom Frappe app for internal departmental helpdesk with team-based permissions.

## Features

### Dual-Role Permission Model
Users automatically get two different access levels based on team membership:

1. **Agent View** (Full Access)
   - Tickets assigned to your team (`agent_group` = your team)
   - Full read/write/comment access
   - Can assign tickets within team

2. **Customer View** (Read-Only)
   - Tickets raised by your team (`originating_team` = your team) but assigned elsewhere
   - Read-only access to track ticket progress
   - Cannot modify or add comments

3. **Admin View** (Full Access to All)
   - Users with `Helpdesk Admin Internal` role
   - Full access to all tickets regardless of team

### Custom Roles

| Role | Description |
|------|-------------|
| Helpdesk User Internal | Basic agent role - can handle team tickets |
| Helpdesk Manager Internal | Manager role - can assign within team |
| Helpdesk Admin Internal | Admin role - full access to all tickets |

### Custom Fields

| Field | DocType | Purpose |
|-------|---------|---------|
| `assigned_team` | User | Links user to their team |
| `originating_team` | HD Ticket | Tracks which team created the ticket (auto-set, read-only) |

## Installation

### Prerequisites
- Frappe Framework v15+
- Frappe Helpdesk app installed

### Install the App

```bash
# Get the app
bench get-app https://github.com/sthalatech/helpdesk_internal_custom.git

# Install on site
bench --site <site-name> install-app helpdesk_internal_custom

# Run migrations
bench --site <site-name> migrate
```

### Post-Installation Setup

1. **Create Teams**
   - Go to Helpdesk > HD Team
   - Create teams (e.g., "IT Support", "HR Support")

2. **Assign Users to Teams**
   - Edit each user
   - Set their `Assigned Team` field

3. **Assign Roles**
   - Give users one of:
     - Helpdesk User Internal
     - Helpdesk Manager Internal
     - Helpdesk Admin Internal

## Usage

### Creating Tickets
When a user creates a ticket:
1. `originating_team` is automatically set to the creator's team
2. `agent_group` (Team) can be set to any team

### Viewing Tickets
Users will see:
- All tickets assigned to their team (full access)
- All tickets their team raised to other teams (read-only)
- No other tickets

### Admin Access
Users with `Helpdesk Admin Internal` role see all tickets with full access.

## Security

The permission system enforces:
- ✅ List filtering (users only see permitted tickets)
- ✅ Document access control
- ✅ Write operation blocking for customer view
- ✅ Immutable `originating_team` after creation
- ✅ Cross-team transfer blocking for non-admins

## Development

### Run Security Tests
```bash
bench --site <site> execute helpdesk_internal_custom.security_tests.run_all_security_tests
```

### Run Permission Tests
```bash
bench --site <site> execute helpdesk_internal_custom.test_setup.test_ticket_access
```

## Repository
https://github.com/sthalatech/helpdesk_internal_custom

## License
AGPLv3
