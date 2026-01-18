# Permission Matrix

## Planned Permission Structure

| Role | Read Own Team Tickets | Write Own Team Tickets | Read Raised Tickets | Write Raised Tickets | Assign |
|------|----------------------|----------------------|--------------------|--------------------|--------|
| Helpdesk User Internal | ✓ | ✓ | ✓ | ✗ | ✗ |
| Helpdesk Manager Internal | ✓ | ✓ | ✓ | ✗ | Own Team |
| Helpdesk Admin Internal | ✓ All | ✓ All | ✓ All | ✓ All | Any |

## Permission Logic

```python
# Agent View (Full Access)
if ticket.assigned_team == user.assigned_team:
    return True

# Customer View (Read Only)
if ticket.originating_team == user.assigned_team:
    return ptype == "read"

# No Access
return False
```

## Custom Fields Required

### User DocType
- `assigned_team` (Link to HD Team) - Mandatory

### HD Ticket DocType
- `originating_team` (Link to HD Team) - Auto-set, Read-only
- `assigned_team` (Link to HD Team) - Selectable
