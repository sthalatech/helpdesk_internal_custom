# Next Session Action Plan

## IMMEDIATE FIRST ACTION:
Push the custom app to GitHub under sthalatech organization.

Commands to run:
```bash
cd /home/exedev/frappe-bench/apps/helpdesk_internal_custom
git init
git add .
git commit -m "feat(session-1): Initial app structure with permission scaffolding"
git remote add origin https://github.com/sthalatech/helpdesk_internal_custom.git
git push -u origin main
```

## Context for Next Session:
- Custom app is created at /home/exedev/frappe-bench/apps/helpdesk_internal_custom
- Frappe bench is at /home/exedev/frappe-bench
- Site is helpdesk.localhost
- PATH needs: export PATH="$HOME/.local/bin:$PATH"
- To start bench: `bench start` from /home/exedev/frappe-bench

## Priority Queue (in order):
1. **Session 1 Completion**:
   - Push custom app to GitHub
   - Configure CORS in site_config.json
   - Install custom app on site
   - Test that bench starts correctly

2. **Session 2 - Discovery Phase**:
   - Analyze Frappe Helpdesk permission framework via API
   - Document existing DocTypes (HD Ticket, HD Team, etc.)
   - Research internal/external comment handling
   - Check if HD Team exists or needs to be created
   - Run: `bench console` and explore:
     ```python
     frappe.get_meta("HD Ticket").fields
     frappe.get_meta("HD Ticket").permissions
     frappe.db.exists("DocType", "HD Team")
     ```

3. **Session 3 - Data Model Changes**:
   - Add custom fields to User (assigned_team)
   - Add custom fields to HD Ticket (originating_team, assigned_team)
   - Create indexes for team fields

4. **Session 4-5 - Permission Layer**:
   - Implement has_permission method
   - Implement get_permission_query_conditions
   - Add document event hooks
   - Test permission filtering

## Dependencies to Check:
- GitHub PAT: [GITHUB_PAT_REDACTED]
- Verify sthalatech org access on GitHub

## Questions to Answer:
- Does HD Team DocType already exist in Frappe Helpdesk?
- What existing permission framework does Helpdesk use?
- How are internal vs external comments handled?

## Files Ready for Next Session:
- helpdesk_internal_custom/hooks.py - Ready for uncommenting permission hooks
- helpdesk_internal_custom/permissions.py - Has placeholder implementation
- helpdesk_internal_custom/overrides/ticket.py - Has placeholder hooks
- helpdesk_internal_custom/api/ticket.py - Has API endpoints
