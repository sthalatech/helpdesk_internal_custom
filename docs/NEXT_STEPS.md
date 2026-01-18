# Next Session Action Plan

## IMMEDIATE FIRST ACTION (Session 3):
Create Custom Fields for the permission system.

## Session 3 Tasks: Data Model Changes

### 1. Create User.assigned_team Custom Field

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
```

Use Frappe's Custom Field system (not Property Setter, since User is a core DocType):

```python
# Create custom field via code
frappe.get_doc({
    "doctype": "Custom Field",
    "dt": "User",
    "fieldname": "assigned_team",
    "fieldtype": "Link",
    "options": "HD Team",
    "label": "Assigned Team",
    "insert_after": "full_name",
    "reqd": 0,  # Make mandatory later after data migration
    "description": "The team this user belongs to for helpdesk purposes"
}).insert()
```

### 2. Create HD Ticket.originating_team Custom Field

```python
frappe.get_doc({
    "doctype": "Custom Field",
    "dt": "HD Ticket",
    "fieldname": "originating_team",
    "fieldtype": "Link",
    "options": "HD Team",
    "label": "Originating Team",
    "insert_after": "agent_group",
    "read_only": 1,
    "description": "Team that created this ticket (auto-set)"
}).insert()
```

### 3. Create Fixtures for Custom Fields

Store custom fields in fixtures for version control and deployment:

```bash
# Export to fixtures
bench --site helpdesk.localhost export-fixtures --app helpdesk_internal_custom
```

Or define in `helpdesk_internal_custom/fixtures/custom_field.json`

### 4. Create Database Indexes

For performance on permission queries:
- Index on `HD Ticket.originating_team`
- Index on `User.assigned_team`

## Session 4 Tasks: Permission Layer

### 1. Implement has_permission Override

Edit: `helpdesk_internal_custom/permissions.py`

```python
def hd_ticket_has_permission(doc, user=None, permission_type=None):
    """
    Custom permission check for HD Ticket.
    
    Returns True if:
    1. User has Helpdesk Admin Internal role (full access)
    2. Ticket's agent_group matches user's assigned_team (agent view)
    3. Ticket's originating_team matches user's assigned_team (customer view - read only)
    """
    pass  # Implement
```

### 2. Implement permission_query_conditions

```python
def hd_ticket_permission_query(user):
    """
    SQL WHERE clause for filtering HD Ticket list.
    """
    pass  # Implement
```

### 3. Enable Hooks

Uncomment in `helpdesk_internal_custom/hooks.py`:

```python
has_permission = {
    "HD Ticket": "helpdesk_internal_custom.permissions.hd_ticket_has_permission"
}

permission_query_conditions = {
    "HD Ticket": "helpdesk_internal_custom.permissions.hd_ticket_permission_query"
}
```

## Session 5 Tasks: Workflow Logic

### 1. Auto-set originating_team on Ticket Creation

Hook: `doc_events` -> `HD Ticket` -> `before_insert`

```python
def set_originating_team(doc, method):
    """Set originating_team from the creator's assigned_team"""
    creator = frappe.session.user
    user_team = frappe.db.get_value("User", creator, "assigned_team")
    if user_team:
        doc.originating_team = user_team
```

### 2. Validate Team Assignment

Hook: `doc_events` -> `HD Ticket` -> `validate`

```python
def validate_team_assignment(doc, method):
    """Ensure managers can only assign to their own team"""
    pass  # Implement
```

### 3. Block Cross-Team Transfers

```python
def block_cross_team_transfer(doc, method):
    """Prevent changing agent_group to a different team (for non-admins)"""
    pass  # Implement
```

## Context for Next Session:
- Custom app: /home/exedev/frappe-bench/apps/helpdesk_internal_custom
- Frappe bench: /home/exedev/frappe-bench
- Site: helpdesk.localhost
- GitHub: https://github.com/sthalatech/helpdesk_internal_custom
- PATH needs: `export PATH="$HOME/.local/bin:$PATH"`

## Files Ready for Modification:
- `helpdesk_internal_custom/hooks.py` - Enable permission hooks
- `helpdesk_internal_custom/permissions.py` - Implement permission logic
- `helpdesk_internal_custom/overrides/ticket.py` - Workflow validation
- `helpdesk_internal_custom/custom_fields/` - Define custom fields
- `helpdesk_internal_custom/fixtures/` - Export custom fields

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

## Key Discovery Findings to Remember:
1. Use existing `agent_group` field (not creating new assigned_team on ticket)
2. HD Team Member child table links users to teams
3. Existing permission hooks in helpdesk can be overridden
4. HD Ticket Comment = internal notes (agent-only)
5. Communication = customer-visible messages
