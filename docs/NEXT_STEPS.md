# Next Session Action Plan

## Session 3 Tasks: UI & Security

### 1. Verify Frontend Behavior
Start the server and test with different user logins:

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
bench serve --port 8000
```

Test URLs:
- https://frappe-helpdesk.exe.xyz:8000/helpdesk/tickets

Login credentials:
| User | Password | Expected View |
|------|----------|---------------|
| it_agent@test.local | TestP@ss123! | IT tickets + read-only customer view |
| hr_agent@test.local | TestP@ss123! | HR tickets + read-only customer view |
| admin@test.local | TestP@ss123! | All tickets |

### 2. UI Read-Only Enforcement
Current state: Backend permissions work. Need to verify:
- Customer view tickets show as read-only in UI
- Edit buttons hidden/disabled for customer view
- Comment creation blocked for customer view

### 3. Cross-Team Transfer Blocking
Implement validation in overrides/ticket.py:
- Block changing agent_group to a team other than user's team (for non-admins)
- Allow initial assignment
- Test with bench execute

### 4. Security Hardening Checklist
- [ ] Verify API endpoints respect permissions
- [ ] Test permission bypass attempts
- [ ] Validate originating_team immutability
- [ ] Test with Frappe's permission debugger
- [ ] Review SQL injection prevention in permission queries

### 5. Push to GitHub
```bash
cd /home/exedev/frappe-bench/apps/helpdesk_internal_custom
git add <files>
git commit -m "Session 2: Implement permission layer with dual-role model"
git push origin main
```

## Files to Test:
- helpdesk_internal_custom/permissions.py
- helpdesk_internal_custom/overrides/ticket.py
- helpdesk_internal_custom/hooks.py

## Test Commands:
```bash
# Test as IT agent
bench --site helpdesk.localhost execute helpdesk_internal_custom.test_setup.test_ticket_access

# Verify permission query
bench --site helpdesk.localhost execute helpdesk_internal_custom.permissions.hd_ticket_permission_query --args '["it_agent@test.local"]'

# Check originating_team auto-set
bench --site helpdesk.localhost execute frappe.get_doc --args '["HD Ticket", "6"]' | grep originating
```

## Remaining Work:
1. **Session 3**: UI testing, security hardening
2. **Session 4**: Reporting, deployment preparation
3. **Session 5**: Final testing, documentation update

## Quick Reference:
- Site: helpdesk.localhost
- Custom app: /home/exedev/frappe-bench/apps/helpdesk_internal_custom
- Test users: it_agent@test.local, hr_agent@test.local, admin@test.local
- Password: TestP@ss123!
