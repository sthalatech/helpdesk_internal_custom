"""
Installation script for Helpdesk Internal Custom app.
This runs after the app is installed via bench.
"""
import frappe
from frappe import _

def after_install():
    """Run after app installation"""
    print("Installing Helpdesk Internal Custom app...")
    
    try:
        create_custom_fields()
        create_roles()
        setup_permissions()
        print("✓ Helpdesk Internal Custom app installed successfully!")
    except Exception as e:
        print(f"✗ Error during installation: {str(e)}")
        raise

def create_custom_fields():
    """Create custom fields using API"""
    from frappe.custom.doctype.custom_field.custom_field import create_custom_field
    
    # Custom fields will be created in later sessions
    # This is a placeholder for the custom field creation logic
    print("  → Setting up custom fields...")
    pass

def create_roles():
    """Create custom roles using API"""
    print("  → Creating custom roles...")
    
    roles = [
        {
            "role_name": "Helpdesk User Internal",
            "desk_access": 1
        },
        {
            "role_name": "Helpdesk Manager Internal", 
            "desk_access": 1
        },
        {
            "role_name": "Helpdesk Admin Internal",
            "desk_access": 1
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
            print(f"    → Role already exists: {role_data['role_name']}")

def setup_permissions():
    """Setup custom permissions using API"""
    print("  → Configuring permissions...")
    # Permissions will be set up in later sessions
    pass

def load_fixtures():
    """Load fixture data"""
    print("  → Loading fixtures...")
    frappe.db.commit()
