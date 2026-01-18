"""
Custom permission methods for HD Ticket.
These will filter tickets based on team membership.
"""
import frappe
from frappe import _

def has_permission(doc, ptype, user=None):
    """
    Custom permission check for tickets.
    
    Args:
        doc: The document being checked
        ptype: Permission type (read, write, create, delete)
        user: User to check permissions for
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user:
        user = frappe.session.user
    
    # Admin has full access
    if "System Manager" in frappe.get_roles(user):
        return True
    
    # Helpdesk Admin Internal has full access
    if "Helpdesk Admin Internal" in frappe.get_roles(user):
        return True
    
    # Get user's team
    user_team = frappe.db.get_value("User", user, "assigned_team")
    
    if not user_team:
        return False
    
    # Agent access: ticket assigned to user's team (full access)
    if hasattr(doc, 'assigned_team') and doc.assigned_team == user_team:
        return True
    
    # Customer access: ticket raised by user's team (read-only)
    if hasattr(doc, 'originating_team') and doc.originating_team == user_team:
        if ptype == "read":
            return True
        return False
    
    return False

def get_permission_query_conditions(user):
    """
    Filter tickets in list view based on permissions.
    
    Args:
        user: User to filter for
    
    Returns:
        str: SQL WHERE clause condition
    """
    if not user:
        user = frappe.session.user
    
    # Admin sees all
    if "System Manager" in frappe.get_roles(user):
        return ""
    
    # Helpdesk Admin Internal sees all
    if "Helpdesk Admin Internal" in frappe.get_roles(user):
        return ""
    
    # Get user's team
    user_team = frappe.db.get_value("User", user, "assigned_team")
    
    if not user_team:
        return "1=0"  # No access
    
    # User sees tickets where they're agent OR customer
    return f"""(
        `tabHD Ticket`.assigned_team = {frappe.db.escape(user_team)}
        OR `tabHD Ticket`.originating_team = {frappe.db.escape(user_team)}
    )"""
