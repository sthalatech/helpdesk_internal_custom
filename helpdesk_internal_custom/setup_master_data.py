"""Create minimum required master data for Helpdesk"""
import frappe

@frappe.whitelist()
def setup():
    """Create minimum required master data"""
    
    # Create Ticket Statuses
    statuses = [
        {"label_agent": "Open", "category": "Open"},
        {"label_agent": "Replied", "category": "Paused"},
        {"label_agent": "Resolved", "category": "Resolved"},
        {"label_agent": "Closed", "category": "Resolved"}
    ]
    
    for status in statuses:
        if not frappe.db.exists("HD Ticket Status", {"label_agent": status["label_agent"]}):
            doc = frappe.get_doc({
                "doctype": "HD Ticket Status",
                "label_agent": status["label_agent"],
                "category": status["category"]
            })
            doc.insert(ignore_permissions=True)
            print(f"✅ Created status: {status['label_agent']}")
        else:
            print(f"⏭️  Status exists: {status['label_agent']}")
    
    # Get Open status name for settings
    open_status = frappe.db.get_value("HD Ticket Status", {"label_agent": "Open"}, "name")
    
    # Create Ticket Priorities
    priorities = [
        {"name": "Low", "integer_value": 1},
        {"name": "Medium", "integer_value": 2},
        {"name": "High", "integer_value": 3},
        {"name": "Urgent", "integer_value": 4}
    ]
    
    for priority in priorities:
        if not frappe.db.exists("HD Ticket Priority", priority["name"]):
            doc = frappe.get_doc({
                "doctype": "HD Ticket Priority",
                "name": priority["name"],
                "integer_value": priority["integer_value"]
            })
            doc.insert(ignore_permissions=True)
            print(f"✅ Created priority: {priority['name']}")
        else:
            print(f"⏭️  Priority exists: {priority['name']}")
    
    # Create Ticket Types
    types = ["General", "Bug", "Feature Request", "Support"]
    
    for type_name in types:
        if not frappe.db.exists("HD Ticket Type", type_name):
            doc = frappe.get_doc({
                "doctype": "HD Ticket Type",
                "name": type_name,
                "priority": "Medium"
            })
            doc.insert(ignore_permissions=True)
            print(f"✅ Created type: {type_name}")
        else:
            print(f"⏭️  Type exists: {type_name}")
    
    # Update HD Settings
    settings = frappe.get_doc("HD Settings")
    settings.default_priority = "Medium"
    settings.default_ticket_type = "General"
    settings.default_ticket_status = open_status
    settings.ticket_reopen_status = open_status
    settings.save(ignore_permissions=True)
    print("✅ Updated HD Settings")
    
    frappe.db.commit()
    return "Setup complete"

@frappe.whitelist()
def create_default_sla():
    """Create a default SLA with required holiday list"""
    if frappe.db.exists("HD Service Level Agreement", {"service_level": "Default"}):
        print("⏭️  Default SLA exists")
        return
    
    # First create a holiday list if needed
    holiday_list_name = "Default Helpdesk Holidays"
    if not frappe.db.exists("HD Service Holiday List", holiday_list_name):
        from datetime import date
        holiday_list = frappe.get_doc({
            "doctype": "HD Service Holiday List",
            "holiday_list_name": holiday_list_name,
            "from_date": date(2020, 1, 1),
            "to_date": date(2030, 12, 31)
        })
        holiday_list.insert(ignore_permissions=True)
        print(f"✅ Created holiday list: {holiday_list_name}")
    
    # Get Open status for SLA
    open_status = frappe.db.get_value("HD Ticket Status", {"label_agent": "Open"}, "name")
    
    sla = frappe.get_doc({
        "doctype": "HD Service Level Agreement",
        "service_level": "Default",
        "enabled": 1,
        "default_sla": 1,  # Mark as default
        "default_priority": "Medium",
        "default_ticket_status": open_status,
        "ticket_reopen_status": open_status,
        "holiday_list": holiday_list_name
    })
    
    # Add working hours for all days (24/7 support)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        sla.append("support_and_resolution", {
            "workday": day,
            "start_time": "00:00:00",
            "end_time": "23:59:59"
        })
    # Add priority entries
    sla.append("priorities", {
        "priority": "Low",
        "response_time": 1440,  # 24 hours in minutes
        "resolution_time": 2880,  # 48 hours in minutes
        "default_priority": 0
    })
    sla.append("priorities", {
        "priority": "Medium",
        "response_time": 480,  # 8 hours in minutes
        "resolution_time": 1440,  # 24 hours in minutes
        "default_priority": 1  # This is the default
    })
    sla.append("priorities", {
        "priority": "High",
        "response_time": 240,  # 4 hours in minutes
        "resolution_time": 480,  # 8 hours in minutes
        "default_priority": 0
    })
    sla.append("priorities", {
        "priority": "Urgent",
        "response_time": 60,  # 1 hour in minutes
        "resolution_time": 240,  # 4 hours in minutes
        "default_priority": 0
    })
    sla.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"✅ Created default SLA: {sla.name}")
    return sla.name
