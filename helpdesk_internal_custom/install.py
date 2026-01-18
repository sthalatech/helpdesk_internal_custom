"""Installation script for Helpdesk Internal Custom app.

This runs after the app is installed via bench.
Creates custom fields, roles, and permissions for the internal helpdesk.
"""
import frappe
from frappe import _


def after_install():
    """Run after app installation"""
    print("Installing Helpdesk Internal Custom app...")
    
    try:
        create_roles()
        create_custom_fields()
        setup_permissions()
        frappe.db.commit()
        print("✓ Helpdesk Internal Custom app installed successfully!")
    except Exception as e:
        print(f"✗ Error during installation: {str(e)}")
        frappe.db.rollback()
        raise


def create_custom_fields():
    """Create custom fields for the permission system"""
    print("  → Setting up custom fields...")
    
    from helpdesk_internal_custom.setup_custom_fields import create_custom_fields as _create
    result = _create()
    
    for field in result.get("created", []):
        print(f"    ✓ Created: {field}")
    for field in result.get("skipped", []):
        print(f"    → Exists: {field}")


def create_roles():
    """Create custom roles for internal helpdesk"""
    print("  → Creating custom roles...")
    
    roles = [
        {
            "role_name": "Helpdesk User Internal",
            "desk_access": 1,
            "is_custom": 1
        },
        {
            "role_name": "Helpdesk Manager Internal",
            "desk_access": 1,
            "is_custom": 1
        },
        {
            "role_name": "Helpdesk Admin Internal",
            "desk_access": 1,
            "is_custom": 1
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                **role_data
            })
            role.insert(ignore_permissions=True)
            print(f"    ✓ Created role: {role_data['role_name']}")
        else:
            print(f"    → Role exists: {role_data['role_name']}")


def setup_permissions():
    """Setup DocType permissions for custom roles"""
    print("  → Configuring permissions...")
    
    # Add HD Ticket permissions for our custom roles
    permissions = [
        {
            "doctype": "HD Ticket",
            "role": "Helpdesk User Internal",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        },
        {
            "doctype": "HD Ticket",
            "role": "Helpdesk Manager Internal",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "doctype": "HD Ticket",
            "role": "Helpdesk Admin Internal",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
    ]
    
    for perm in permissions:
        doctype = perm.pop("doctype")
        role = perm["role"]
        
        # Check if permission already exists
        exists = frappe.db.exists("Custom DocPerm", {
            "parent": doctype,
            "role": role
        })
        
        if not exists:
            # Add permission via API
            from frappe.permissions import add_permission
            add_permission(doctype, role, 0)
            print(f"    ✓ Added {role} permission to {doctype}")
        else:
            print(f"    → Permission exists: {role} on {doctype}")


def before_uninstall():
    """Cleanup before app uninstallation"""
    print("Uninstalling Helpdesk Internal Custom app...")
    # Custom fields and roles will be removed by Frappe
    # based on module association
