# Next Session Context & Instructions

## Quick Start for Next Session

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench

# Check services are running
sudo systemctl status mariadb redis-server --no-pager | grep Active

# Start the development server (if not running)
bench serve --port 8000 &

# Or check if already running
curl -s http://localhost:8000 | head -1
```

## Project Overview

**App**: `helpdesk_internal_custom` - Custom Frappe app for internal departmental helpdesk  
**Location**: `/home/exedev/frappe-bench/apps/helpdesk_internal_custom`  
**GitHub**: https://github.com/sthalatech/helpdesk_internal_custom  
**Site**: `helpdesk.localhost`  

### Core Feature: Dual-Role Permission Model
- **Agent View**: Full access to tickets assigned to user's team (`agent_group`)
- **Customer View**: Read-only access to tickets raised by user's team (`originating_team`)
- **Admin View**: Full access to all tickets (`Helpdesk Admin Internal` role)

## Current Project Status: 90% Complete

### ✅ Completed
| Phase | Status |
|-------|--------|
| 1. Setup & Repository | ✅ Complete |
| 2. Discovery Phase | ✅ Complete |
| 3. Data Model Changes | ✅ Complete |
| 4. Permission Layer | ✅ Complete |
| 5. UI Verification | ⚠️ Backend works, UI enhancements pending |
| 6. Role Configuration | ✅ Complete |
| 7. Workflow Logic | ✅ Complete |
| 8. Reporting | ❌ Not started |
| 9. Testing | ✅ Complete |
| 10. Security Hardening | ⚠️ Core tests pass, advanced checks pending |
| 11. Documentation | ✅ Complete |
| 12. Deployment Prep | ⚠️ Mostly complete |

### Key Files
```
helpdesk_internal_custom/
├── permissions.py          # Permission logic (has_permission, permission_query)
├── hooks.py                # Hook configuration
├── overrides/ticket.py     # Document events (auto-set originating_team)
├── install.py              # Installation script
├── security_tests.py       # Security test suite
├── test_setup.py           # Test data creation
├── setup_custom_fields.py  # Custom field creation
├── setup_master_data.py    # Master data setup
└── fixtures/
    ├── custom_field.json   # User.assigned_team, HD Ticket.originating_team
    └── role.json           # Custom roles
```

## Test Data Available

### Teams
- IT Support
- HR Support

### Users
| User | Password | Team | Role |
|------|----------|------|------|
| it_agent@test.local | TestP@ss123! | IT Support | Helpdesk User Internal |
| it_manager@test.local | TestP@ss123! | IT Support | Helpdesk Manager Internal |
| hr_agent@test.local | TestP@ss123! | HR Support | Helpdesk User Internal |
| hr_manager@test.local | TestP@ss123! | HR Support | Helpdesk Manager Internal |
| admin@test.local | TestP@ss123! | None | Helpdesk Admin Internal |
| Administrator | admin123 | None | System Manager |

### Tickets
| ID | Subject | Assigned To | Raised By | IT Agent Sees | HR Agent Sees |
|----|---------|-------------|-----------|---------------|---------------|
| 6 | IT Ticket 1 | IT Support | IT Support | ✅ Full | ❌ Hidden |
| 7 | IT Ticket 2 | HR Support | IT Support | 📖 Read-only | ✅ Full |
| 8 | HR Ticket 1 | HR Support | HR Support | ❌ Hidden | ✅ Full |
| 9 | HR Ticket 2 | IT Support | HR Support | ✅ Full | 📖 Read-only |

## Useful Commands

### Run Security Tests
```bash
bench --site helpdesk.localhost execute helpdesk_internal_custom.security_tests.run_all_security_tests
```

### Run Permission Tests
```bash
bench --site helpdesk.localhost execute helpdesk_internal_custom.test_setup.test_ticket_access
```

### Check Custom Fields
```bash
bench --site helpdesk.localhost execute helpdesk_internal_custom.setup_custom_fields.check_custom_fields
```

### Clear Cache
```bash
bench --site helpdesk.localhost clear-cache
```

### Migrate (after schema changes)
```bash
bench --site helpdesk.localhost migrate
```

## Remaining Work Options

### Option 1: UI Enhancements (Medium Priority)
Add visual indicators for read-only customer view tickets:
- Show "Read Only" badge on customer view tickets
- Disable edit controls (Reply, Comment, Team dropdown)
- Show informational message explaining limited access

**Approach**: Modify Vue frontend or add client-side script in hooks.py

### Option 2: Reporting (Low Priority)
Create reports:
- Tickets by originating team
- Tickets by assigned team
- Cross-team ticket tracking

**Approach**: Create Report DocType or use Script Report

### Option 3: Advanced Security (Low Priority)
- Rate limiting on API endpoints
- Audit logging for permission-sensitive actions
- CSRF token validation review

### Option 4: Production Deployment
- Create deployment checklist
- Test on fresh site
- Create backup/restore procedures
- Document rollback plan

## Access URLs
- **External**: https://frappe-helpdesk.exe.xyz:8000
- **Helpdesk**: https://frappe-helpdesk.exe.xyz:8000/helpdesk/tickets
- **Local**: http://localhost:8000

## Architecture Notes

### Permission Flow
```
User Request → permission_query_conditions (list filter)
            → has_permission (document access)
            → Backend validates write operations
```

### Custom Fields
- `User.assigned_team` → Links user to single team
- `HD Ticket.originating_team` → Auto-set on creation, immutable

### Hooks Enabled
```python
has_permission = {"HD Ticket": "helpdesk_internal_custom.permissions.has_permission"}
permission_query_conditions = {"HD Ticket": "helpdesk_internal_custom.permissions.get_permission_query_conditions"}
doc_events = {"HD Ticket": {"before_insert": ..., "validate": ..., "before_save": ...}}
```

## Read Before Modifying

**IMPORTANT**: Always read the AGENTS.md file before modifying files:
```bash
cat /home/exedev/frappe-bench/apps/helpdesk/AGENTS.md
```

This contains Frappe Helpdesk coding standards and architecture guidelines.

## Git Workflow
```bash
cd /home/exedev/frappe-bench/apps/helpdesk_internal_custom
git status
git add <specific-files>
git commit -m "Description of changes"
git push origin main
```
