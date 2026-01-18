"""Custom permission methods for HD Ticket.

These implement the dual-role permission model:
- AGENT VIEW: Full access to tickets assigned to user's team (agent_group)
- CUSTOMER VIEW: Read-only access to tickets raised by user's team (originating_team)
- ADMIN VIEW: Full access to all tickets
"""
import frappe
from frappe import _


def is_helpdesk_admin(user=None):
    """Check if user is a helpdesk admin."""
    if not user:
        user = frappe.session.user
    return (
        user == "Administrator"
        or "System Manager" in frappe.get_roles(user)
        or "Helpdesk Admin Internal" in frappe.get_roles(user)
    )


def get_user_team(user=None):
    """Get user's assigned team."""
    if not user:
        user = frappe.session.user
    return frappe.db.get_value("User", user, "assigned_team")


def hd_ticket_has_permission(doc, ptype=None, user=None):
    """Custom permission check for HD Ticket.
    
    Implements the dual-role permission model:
    - Admin: Full access to all tickets
    - Agent: Full access if ticket's agent_group matches user's team
    - Customer: Read-only access if ticket's originating_team matches user's team
    
    Args:
        doc: The HD Ticket document being checked
        ptype: Permission type (read, write, create, delete, etc.)
        user: User to check permissions for
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user:
        user = frappe.session.user
    
    # Admin has full access
    if is_helpdesk_admin(user):
        return True
    
    # Get user's team
    user_team = get_user_team(user)
    
    if not user_team:
        # User has no team - fall back to original helpdesk permissions
        # This allows non-team users (like external customers) to still work
        return None  # Return None to let Frappe continue checking
    
    # Agent access: ticket assigned to user's team (full access)
    # Uses agent_group which is the existing "Team" field on HD Ticket
    ticket_team = doc.get("agent_group")
    if ticket_team and ticket_team == user_team:
        return True
    
    # Customer access: ticket raised by user's team (read-only)
    originating = doc.get("originating_team")
    if originating and originating == user_team:
        # Customer view - only read access
        if ptype in ("read", "select", None):
            return True
        return False
    
    # Check if user is owner/raised_by (standard helpdesk behavior)
    if doc.get("owner") == user or doc.get("raised_by") == user:
        return True
    
    # No access
    return False


def hd_ticket_permission_query(user=None):
    """SQL WHERE clause for filtering HD Ticket list view.
    
    Returns a condition that shows tickets where:
    - User is admin (no filter)
    - Ticket's agent_group matches user's team (agent view)
    - Ticket's originating_team matches user's team (customer view)
    - User is owner/raised_by (standard helpdesk behavior)
    
    Args:
        user: User to filter for
    
    Returns:
        str: SQL WHERE clause condition (empty string for no filter, "1=0" for no access)
    """
    if not user:
        user = frappe.session.user
    
    # Admin sees all
    if is_helpdesk_admin(user):
        return ""
    
    # Get user's team
    user_team = get_user_team(user)
    
    if not user_team:
        # User has no team - show only tickets they own/raised
        # This maintains backwards compatibility with external customers
        return """(
            `tabHD Ticket`.owner = {user}
            OR `tabHD Ticket`.raised_by = {user}
        )""".format(user=frappe.db.escape(user))
    
    # User with team sees:
    # 1. Tickets assigned to their team (agent_group)
    # 2. Tickets raised by their team (originating_team)
    # 3. Tickets they own/raised (backwards compatibility)
    return """(
        `tabHD Ticket`.agent_group = {team}
        OR `tabHD Ticket`.originating_team = {team}
        OR `tabHD Ticket`.owner = {user}
        OR `tabHD Ticket`.raised_by = {user}
    )""".format(
        team=frappe.db.escape(user_team),
        user=frappe.db.escape(user)
    )


# Aliases for hooks.py compatibility
has_permission = hd_ticket_has_permission
get_permission_query_conditions = hd_ticket_permission_query
