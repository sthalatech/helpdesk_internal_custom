import frappe

def create_custom_fields():
    """Create custom fields required for internal helpdesk permission system"""
    
    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "User",
            "fieldname": "assigned_team",
            "fieldtype": "Link",
            "options": "HD Team",
            "label": "Assigned Team",
            "insert_after": "full_name",
            "reqd": 0,  # Start as optional, make mandatory after data migration
            "description": "The team this user belongs to for helpdesk purposes. Required for internal helpdesk users.",
            "translatable": 0
        },
        {
            "doctype": "Custom Field",
            "dt": "HD Ticket",
            "fieldname": "originating_team",
            "fieldtype": "Link",
            "options": "HD Team",
            "label": "Originating Team",
            "insert_after": "agent_group",
            "read_only": 1,
            "description": "Team that created this ticket (auto-set from creator's assigned_team)",
            "translatable": 0,
            "allow_on_submit": 0
        }
    ]
    
    created = []
    skipped = []
    
    for cf in custom_fields:
        field_key = f"{cf['dt']}-{cf['fieldname']}"
        
        # Check if already exists
        existing = frappe.db.exists("Custom Field", {"dt": cf["dt"], "fieldname": cf["fieldname"]})
        
        if existing:
            skipped.append(field_key)
            print(f"⏭️  Skipped (already exists): {field_key}")
        else:
            doc = frappe.get_doc(cf)
            doc.insert(ignore_permissions=True)
            created.append(field_key)
            print(f"✅ Created: {field_key}")
    
    frappe.db.commit()
    
    return {
        "created": created,
        "skipped": skipped
    }

@frappe.whitelist()
def execute():
    """Execute custom field creation"""
    return create_custom_fields()

@frappe.whitelist()
def check_custom_fields():
    """Check if custom fields exist"""
    fields = [
        ("User", "assigned_team"),
        ("HD Ticket", "originating_team")
    ]
    
    result = {}
    for dt, fieldname in fields:
        exists = frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname})
        result[f"{dt}.{fieldname}"] = bool(exists)
    
    return result
