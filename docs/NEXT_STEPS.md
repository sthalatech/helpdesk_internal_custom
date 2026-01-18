# Next Session Action Plan

## IMMEDIATE FIRST ACTION:
Start Discovery Phase - Analyze Frappe Helpdesk structure via API.

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
bench console
```

Then run:
```python
# Explore HD Ticket DocType
frappe.get_meta("HD Ticket").fields
frappe.get_meta("HD Ticket").permissions

# Check if HD Team exists
frappe.db.exists("DocType", "HD Team")
frappe.get_meta("HD Team").fields if frappe.db.exists("DocType", "HD Team") else "HD Team doesn't exist"

# List existing roles
frappe.get_all("Role", filters={"name": ["like", "%helpdesk%"]})

# Check existing hooks from helpdesk
from helpdesk import hooks as hd_hooks
print(dir(hd_hooks))
```

## Context for Next Session:
- Custom app installed at: /home/exedev/frappe-bench/apps/helpdesk_internal_custom
- Frappe bench at: /home/exedev/frappe-bench
- Site: helpdesk.localhost
- GitHub: https://github.com/sthalatech/helpdesk_internal_custom
- PATH needs: `export PATH="$HOME/.local/bin:$PATH"`
- To start bench: `bench serve --port 8000` from /home/exedev/frappe-bench

## Priority Queue (in order):
1. **Session 2 - Discovery Phase**:
   - Analyze HD Ticket DocType structure
   - Document existing fields and permissions
   - Check if HD Team DocType exists
   - Research internal/external comment handling
   - Document findings in docs/DISCOVERY.md

2. **Session 3 - Data Model Changes**:
   - Add custom field: User.assigned_team (Link to HD Team)
   - Add custom field: HD Ticket.originating_team (Link to HD Team)
   - Add custom field: HD Ticket.assigned_team (Link to HD Team)
   - Create database indexes

3. **Session 4-5 - Permission Layer**:
   - Uncomment and implement has_permission in permissions.py
   - Uncomment and implement get_permission_query_conditions
   - Add document event hooks in hooks.py
   - Test permission filtering via bench console

4. **Session 6+ - Remaining Tasks**:
   - Workflow validation hooks
   - UI modifications (if needed)
   - Testing with multiple users
   - Security hardening
   - Deployment preparation

## Dependencies to Check:
- Verify HD Team DocType exists in Helpdesk
- Check User DocType for existing team-related fields
- Research how Helpdesk handles ticket assignments

## Files Ready for Modification:
- helpdesk_internal_custom/hooks.py - Uncomment permission hooks
- helpdesk_internal_custom/permissions.py - Complete implementation
- helpdesk_internal_custom/overrides/ticket.py - Enable validation hooks
- helpdesk_internal_custom/api/ticket.py - API ready to use

## To Start Development Server:
```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
bench serve --port 8000
# Or for full stack: bench start
```

## To Access:
- Local: http://localhost:8000
- External: https://frappe-helpdesk.exe.xyz:8000
