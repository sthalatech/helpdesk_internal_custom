import frappe
import json

@frappe.whitelist()
def get_hd_ticket_structure():
    """Get HD Ticket DocType structure for analysis"""
    meta = frappe.get_meta("HD Ticket")
    
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "options": f.options,
                "reqd": f.reqd,
                "read_only": f.read_only,
                "hidden": f.hidden
            })
    
    permissions = []
    for p in meta.permissions:
        permissions.append({
            "role": p.role,
            "read": p.read,
            "write": p.write,
            "create": p.create,
            "delete": p.delete,
            "submit": p.submit,
            "cancel": p.cancel,
            "amend": p.amend
        })
    
    return {
        "doctype": "HD Ticket",
        "fields": fields,
        "permissions": permissions,
        "is_submittable": meta.is_submittable,
        "track_changes": meta.track_changes
    }

@frappe.whitelist()
def get_hd_team_structure():
    """Get HD Team DocType structure for analysis"""
    meta = frappe.get_meta("HD Team")
    
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "options": f.options,
                "reqd": f.reqd
            })
    
    return {
        "doctype": "HD Team",
        "fields": fields
    }

@frappe.whitelist()
def get_user_team_fields():
    """Check if User DocType has any team-related fields"""
    meta = frappe.get_meta("User")
    
    team_fields = []
    for f in meta.fields:
        if 'team' in f.fieldname.lower() or (f.options and 'team' in str(f.options).lower()):
            team_fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "options": f.options
            })
    
    return team_fields

@frappe.whitelist()
def get_helpdesk_roles():
    """Get all helpdesk-related roles"""
    roles = frappe.get_all("Role", 
        filters={"name": ["like", "%helpdesk%"]}, 
        fields=["name", "desk_access"]
    )
    return roles

@frappe.whitelist()
def get_hd_team_member_structure():
    """Get HD Team Member DocType structure"""
    meta = frappe.get_meta("HD Team Member")
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "options": f.options
            })
    return fields

@frappe.whitelist()
def get_hd_ticket_comment_structure():
    """Get HD Ticket Comment structure for internal/external comment handling"""
    meta = frappe.get_meta("HD Ticket Comment")
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "options": f.options
            })
    return fields

@frappe.whitelist()
def get_existing_hd_teams():
    """Get all existing HD Teams"""
    return frappe.get_all("HD Team", fields=["name", "team_name"])

@frappe.whitelist()
def get_hd_agent_structure():
    """Get HD Agent DocType structure"""
    meta = frappe.get_meta("HD Agent")
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "options": f.options
            })
    return fields

@frappe.whitelist()
def get_helpdesk_hooks():
    """Get helpdesk app hooks that we need to be aware of"""
    from helpdesk import hooks
    return {
        "has_permission": getattr(hooks, "has_permission", {}),
        "permission_query_conditions": getattr(hooks, "permission_query_conditions", {}),
        "doc_events": getattr(hooks, "doc_events", {}),
        "override_whitelisted_methods": getattr(hooks, "override_whitelisted_methods", {})
    }

@frappe.whitelist()
def get_hd_settings_structure():
    """Get HD Settings DocType structure"""
    meta = frappe.get_meta("HD Settings")
    fields = []
    for f in meta.fields:
        if f.fieldtype not in ["Section Break", "Column Break", "Tab Break"]:
            fields.append({
                "fieldname": f.fieldname,
                "fieldtype": f.fieldtype,
                "label": f.label,
                "default": f.default
            })
    return fields

@frappe.whitelist()
def get_hd_settings_values():
    """Get current HD Settings values related to permissions"""
    doc = frappe.get_doc("HD Settings")
    return {
        "restrict_tickets_by_agent_group": doc.restrict_tickets_by_agent_group,
        "do_not_restrict_tickets_without_an_agent_group": doc.do_not_restrict_tickets_without_an_agent_group
    }
