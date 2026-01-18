"""
Custom Ticket class extending Frappe Helpdesk.
Contains validation and business logic hooks.
"""
import frappe
from frappe import _

def before_insert(doc, method):
    """
    Auto-set originating team on ticket creation.
    
    This hook runs before a new ticket is inserted into the database.
    It automatically sets the originating_team based on the creator's team.
    """
    if not doc.get("originating_team"):
        user_team = frappe.db.get_value("User", frappe.session.user, "assigned_team")
        if user_team:
            doc.originating_team = user_team
            frappe.logger().debug(f"Auto-set originating_team to {user_team} for ticket created by {frappe.session.user}")

def validate(doc, method):
    """
    Validate team assignments on ticket save.
    
    Business rules:
    - Cannot assign ticket to the same team that raised it
    - Assigned team must exist
    """
    # Prevent self-assignment (team raising ticket to itself)
    if doc.originating_team and doc.assigned_team:
        if doc.originating_team == doc.assigned_team:
            frappe.throw(_("Cannot assign ticket to the same team that raised it"))
    
    # Validate assigned team exists
    if doc.assigned_team and not frappe.db.exists("HD Team", doc.assigned_team):
        frappe.throw(_("Invalid assigned team: {0}").format(doc.assigned_team))

def before_save(doc, method):
    """
    Additional validation before saving ticket.
    """
    pass
