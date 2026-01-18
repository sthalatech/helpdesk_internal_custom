"""Custom Ticket hooks for internal helpdesk.

Contains validation and business logic for:
- Auto-setting originating_team
- Validating team assignments
- Blocking cross-team transfers
"""
import frappe
from frappe import _

from helpdesk_internal_custom.permissions import is_helpdesk_admin, get_user_team


def before_insert(doc, method):
    """Auto-set originating_team on ticket creation.
    
    This hook runs before a new ticket is inserted into the database.
    It automatically sets the originating_team based on the creator's team.
    
    Args:
        doc: HD Ticket document
        method: Hook method name
    """
    if not doc.get("originating_team"):
        user_team = get_user_team(frappe.session.user)
        if user_team:
            doc.originating_team = user_team
            frappe.logger("helpdesk_internal").debug(
                f"Auto-set originating_team to {user_team} for ticket by {frappe.session.user}"
            )


def validate(doc, method):
    """Validate ticket on save.
    
    Business rules:
    - Manager can only assign to their own team
    - Block cross-team transfers for non-admins
    - originating_team cannot be changed after creation
    
    Args:
        doc: HD Ticket document
        method: Hook method name
    """
    user = frappe.session.user
    
    # Skip validation for admins
    if is_helpdesk_admin(user):
        return
    
    # Validate originating_team is not changed after creation
    if not doc.is_new():
        old_doc = doc.get_doc_before_save()
        if old_doc and old_doc.originating_team:
            if doc.originating_team != old_doc.originating_team:
                frappe.throw(
                    _("Originating team cannot be changed after ticket creation"),
                    frappe.PermissionError
                )
    
    # Validate team assignment (manager can only assign to their own team)
    user_team = get_user_team(user)
    
    if not user_team:
        # User without team can't do team-based assignments
        return
    
    # Check if user has Helpdesk Manager Internal role
    is_manager = "Helpdesk Manager Internal" in frappe.get_roles(user)
    
    if is_manager and doc.agent_group:
        # Manager can only assign to their own team
        if doc.agent_group != user_team:
            frappe.throw(
                _("You can only assign tickets to your own team ({0})").format(user_team),
                frappe.PermissionError
            )
    
    # Block cross-team transfers for non-admins
    if not doc.is_new():
        old_doc = doc.get_doc_before_save()
        if old_doc and old_doc.agent_group and doc.agent_group:
            if old_doc.agent_group != doc.agent_group:
                # Check if user's team is involved in the transfer
                if old_doc.agent_group != user_team and doc.agent_group != user_team:
                    frappe.throw(
                        _("You cannot transfer tickets between other teams"),
                        frappe.PermissionError
                    )


def before_save(doc, method):
    """Additional processing before saving ticket.
    
    Args:
        doc: HD Ticket document
        method: Hook method name
    """
    # Set originating_team if still not set (edge case)
    if doc.is_new() and not doc.originating_team:
        user_team = get_user_team(doc.owner or frappe.session.user)
        if user_team:
            doc.originating_team = user_team
