# Discovery Phase Documentation

## Date: 2026-01-18 Session 2

## 1. Frappe Helpdesk DocType Overview

### HD Ticket Fields (Key fields for our implementation)

| Field Name | Type | Options | Purpose |
|------------|------|---------|---------|
| `subject` | Data | - | Ticket subject (required) |
| `raised_by` | Data (Email) | - | Email of person who raised ticket |
| `status` | Link | HD Ticket Status | Current status |
| `priority` | Link | HD Ticket Priority | Ticket priority |
| `ticket_type` | Link | HD Ticket Type | Type of ticket |
| **`agent_group`** | Link | HD Team | **Assigned team** (existing field) |
| `description` | Text Editor | - | Ticket description |
| `contact` | Link | Contact | Contact who raised ticket |
| `customer` | Link | HD Customer | Customer organization |
| `feedback_rating` | Rating | - | Customer feedback |

**Critical Finding**: The `agent_group` field is the existing "assigned team" field. We need to add `originating_team` separately.

### HD Team Structure

| Field Name | Type | Options |
|------------|------|---------|
| `team_name` | Data | - |
| `assignment_rule` | Link | Assignment Rule |
| `users` | Table MultiSelect | HD Team Member |
| `ignore_restrictions` | Check | - |

**Team Membership**: Users are linked to teams via `HD Team Member` child table with single field:
- `user` -> Link to User

### HD Agent Structure

| Field Name | Type | Options |
|------------|------|---------|
| `user` | Link | User |
| `agent_name` | Data | - |
| `is_active` | Check | - |

### HD Ticket Comment (Internal Notes)

| Field Name | Type | Options |
|------------|------|---------|
| `reference_ticket` | Link | HD Ticket |
| `commented_by` | Link | User |
| `is_pinned` | Check | - |
| `content` | Text Editor | - |

**Internal vs External Comments**: 
- `HD Ticket Comment` is used for internal agent comments
- `Communication` DocType is used for customer-visible messages (external)
- Only agents can create `HD Ticket Comment` (enforced in `new_comment` method)

---

## 2. Existing Permission System

### HD Ticket Permissions (DocType Level)

| Role | Read | Write | Create | Delete |
|------|------|-------|--------|--------|
| System Manager | ✅ | ✅ | ✅ | ✅ |
| Agent | ✅ | ✅ | ✅ | ✅ |
| All | ✅ | ✅ | ✅ | ❌ |
| Agent Manager | ✅ | ✅ | ✅ | ✅ |

### Existing Permission Hooks

**Location**: `helpdesk/helpdesk/doctype/hd_ticket/hd_ticket.py`

```python
# has_permission - Called for each document access check
def has_permission(doc, user=None):
    # Allows access if:
    # 1. User is contact, raised_by, or owner of ticket
    # 2. User is admin
    # 3. User's customer matches ticket customer
    # 4. User is agent AND (restrictions disabled OR user's team matches agent_group)
```

```python
# permission_query - SQL WHERE clause for list filtering
def permission_query(user):
    # Returns SQL condition to filter tickets based on:
    # 1. Owner/contact/raised_by match
    # 2. Customer match
    # 3. Agent team restrictions (if enabled)
```

### Key Settings (HD Settings)

| Setting | Current Value | Purpose |
|---------|---------------|---------|
| `restrict_tickets_by_agent_group` | 0 (disabled) | When enabled, agents only see their team's tickets |
| `do_not_restrict_tickets_without_an_agent_group` | 0 | Show unassigned tickets to all agents |

### Utility Functions (`helpdesk/utils.py`)

```python
def is_admin(user) -> bool:
    # Returns True only if user == "Administrator"

def is_agent(user) -> bool:
    # Returns True if:
    # - User is admin
    # - User has "Agent Manager" role
    # - User has "Agent" role
    # - User exists in HD Agent

def get_agents_team():
    # Returns teams where current user is a member via HD Team Member
```

---

## 3. Custom Fields Required

### User.assigned_team (NEW)

- **Purpose**: Link user to their single team for permission checks
- **Type**: Link to HD Team
- **Required**: Yes (mandatory for all internal users)
- **Notes**: This is different from HD Team Member which allows multi-team membership

### HD Ticket.originating_team (NEW)

- **Purpose**: Track which team created the ticket
- **Type**: Link to HD Team
- **Auto-Set**: From creator's `assigned_team` on ticket creation
- **Read-Only**: Yes (cannot be changed after creation)

### HD Ticket.assigned_team

- **Existing Field**: `agent_group` already serves this purpose
- **Action**: Use existing `agent_group` field instead of creating new one

---

## 4. Permission Logic Design

### Our Custom Rules (vs existing Helpdesk rules)

| Scenario | Existing Helpdesk | Our Requirement |
|----------|-------------------|-----------------|
| User views own team's tickets (as agent) | ✅ if team matches `agent_group` | ✅ Same |
| User views tickets raised by own team | ❌ Not supported | ✅ NEW - Read-only "customer view" |
| Manager assigns within team | No restriction | ✅ Restrict to own team only |
| Cross-team transfers | Allowed | ❌ Block completely |
| Admin access | Only "Administrator" | ✅ Users with admin role see all |

### Permission Matrix

```
IF user has Helpdesk Admin Internal role:
    → FULL ACCESS to all tickets

ELSE IF ticket.agent_group == user.assigned_team:
    → FULL AGENT ACCESS (read/write/comment)

ELSE IF ticket.originating_team == user.assigned_team:
    → READ-ONLY ACCESS (customer view)

ELSE:
    → NO ACCESS
```

---

## 5. Implementation Strategy

### Phase 1: Custom Fields (Session 3)
1. Add `User.assigned_team` custom field via Property Setter or Custom Field
2. Add `HD Ticket.originating_team` custom field
3. Create database indexes for performance

### Phase 2: Permission Hooks (Session 4)
1. Override `has_permission` for HD Ticket in our app
2. Override `permission_query_conditions` for list filtering
3. Hook order: Our app loads AFTER helpdesk, so our hooks override theirs

### Phase 3: Validation Hooks (Session 5)
1. Auto-set `originating_team` on ticket creation
2. Validate team assignment (manager can only assign to own team)
3. Block cross-team transfers

### Hook Override Mechanism

Frappe processes hooks in app installation order. Our app is installed after helpdesk, so we can override by:

```python
# hooks.py
has_permission = {
    "HD Ticket": "helpdesk_internal_custom.permissions.hd_ticket_has_permission"
}

permission_query_conditions = {
    "HD Ticket": "helpdesk_internal_custom.permissions.hd_ticket_permission_query"
}
```

---

## 6. Testing Strategy

### Test Scenarios
1. Admin can see all tickets ✅
2. Agent can see/edit tickets assigned to their team ✅
3. Agent can view (read-only) tickets raised by their team ✅
4. Agent cannot see other teams' tickets ❌
5. Manager can assign tickets only within their team
6. Cross-team transfer is blocked
7. Originating team is auto-set and immutable

### Test Users to Create
| User | Role | Team |
|------|------|------|
| admin@test.com | Helpdesk Admin Internal | - |
| agent1@test.com | Helpdesk User Internal | IT Support |
| agent2@test.com | Helpdesk User Internal | HR Support |
| manager1@test.com | Helpdesk Manager Internal | IT Support |
| manager2@test.com | Helpdesk Manager Internal | HR Support |

---

## 7. Key Findings Summary

1. ✅ `HD Team` DocType exists - use for team management
2. ✅ `agent_group` field on HD Ticket is the assigned team
3. ❌ No `originating_team` field exists - must create
4. ❌ No `User.assigned_team` field exists - must create  
5. ✅ Existing permission system can be overridden via hooks
6. ✅ `HD Ticket Comment` is for internal notes (agent-only)
7. ✅ `Communication` is for customer-visible messages
8. ⚠️ Current restriction settings are disabled - need to enable for our model
