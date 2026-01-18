# API Documentation

## Custom Endpoints

### Get My Team Tickets (Agent View)
```
GET /api/method/helpdesk_internal_custom.api.ticket.get_my_team_tickets
```

Returns tickets assigned to the current user's team.

**Response:**
```json
[
  {
    "name": "HD-TICKET-0001",
    "subject": "Issue title",
    "status": "Open",
    "priority": "Medium",
    "creation": "2026-01-18 15:00:00",
    "modified": "2026-01-18 15:30:00"
  }
]
```

### Get My Raised Tickets (Customer View)
```
GET /api/method/helpdesk_internal_custom.api.ticket.get_my_raised_tickets
```

Returns tickets raised by the current user's team.

### Get Ticket Context
```
GET /api/method/helpdesk_internal_custom.api.ticket.get_ticket_context
```

**Parameters:**
- `ticket_name`: HD Ticket name

**Response:**
```json
{
  "ticket": { ... },
  "view_mode": "agent|customer|admin|none",
  "can_edit": true,
  "can_assign": false
}
```
