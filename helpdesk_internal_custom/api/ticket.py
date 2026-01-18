"""
Custom API endpoints for tickets.
These provide team-filtered ticket access.
"""
import frappe
from frappe import _

@frappe.whitelist()
def get_my_team_tickets():
    """
    API endpoint for getting tickets assigned to user's team (Agent view).
    
    Returns:
        list: Tickets assigned to user's team
    """
    user_team = frappe.db.get_value("User", frappe.session.user, "assigned_team")
    
    if not user_team:
        return []
    
    tickets = frappe.get_all(
        "HD Ticket",
        filters={"assigned_team": user_team},
        fields=["name", "subject", "status", "priority", "creation", "modified"]
    )
    
    return tickets

@frappe.whitelist()
def get_my_raised_tickets():
    """
    API endpoint for getting tickets raised by user's team (Customer view).
    
    Returns:
        list: Tickets raised by user's team
    """
    user_team = frappe.db.get_value("User", frappe.session.user, "assigned_team")
    
    if not user_team:
        return []
    
    tickets = frappe.get_all(
        "HD Ticket",
        filters={"originating_team": user_team},
        fields=["name", "subject", "status", "priority", "creation", "modified"]
    )
    
    return tickets

@frappe.whitelist()
def get_ticket_context(ticket_name):
    """
    Get ticket with context about user's relationship to it.
    
    Returns:
        dict: Ticket data with view_mode (agent/customer/admin/none)
    """
    user = frappe.session.user
    user_team = frappe.db.get_value("User", user, "assigned_team")
    
    # Check if admin
    is_admin = "System Manager" in frappe.get_roles(user) or "Helpdesk Admin Internal" in frappe.get_roles(user)
    
    ticket = frappe.get_doc("HD Ticket", ticket_name)
    
    view_mode = "none"
    
    if is_admin:
        view_mode = "admin"
    elif hasattr(ticket, 'assigned_team') and ticket.assigned_team == user_team:
        view_mode = "agent"
    elif hasattr(ticket, 'originating_team') and ticket.originating_team == user_team:
        view_mode = "customer"
    
    return {
        "ticket": ticket.as_dict(),
        "view_mode": view_mode,
        "can_edit": view_mode in ["agent", "admin"],
        "can_assign": view_mode in ["agent", "admin"] and "Helpdesk Manager Internal" in frappe.get_roles(user)
    }
