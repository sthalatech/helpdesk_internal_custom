# Maintenance Guide

## Updating the App

```bash
cd /path/to/frappe-bench
bench update --apps helpdesk_internal_custom
bench --site [site] migrate
```

## Troubleshooting

### Permission Issues
Check that:
1. User has `assigned_team` set
2. Ticket has `originating_team` and `assigned_team` set
3. User has appropriate role assigned

### Console Debugging
```python
bench console

# Check user's team
frappe.db.get_value("User", "user@example.com", "assigned_team")

# Check ticket teams
ticket = frappe.get_doc("HD Ticket", "HD-TICKET-0001")
print(ticket.originating_team, ticket.assigned_team)

# Test permission
from helpdesk_internal_custom.permissions import has_permission
has_permission(ticket, "read", "user@example.com")
```

## Custom Field Locations

Custom fields created by this app:
- User.assigned_team
- HD Ticket.originating_team
- HD Ticket.assigned_team

## Logs

Check Frappe logs at:
```
/path/to/frappe-bench/logs/
```
