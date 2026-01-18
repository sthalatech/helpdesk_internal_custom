"""Create test data for permission testing"""
import frappe

@frappe.whitelist()
def create_test_teams():
    """Create test teams"""
    teams = ["IT Support", "HR Support"]
    created = []
    
    for team_name in teams:
        if not frappe.db.exists("HD Team", {"team_name": team_name}):
            doc = frappe.get_doc({
                "doctype": "HD Team",
                "team_name": team_name
            })
            doc.insert(ignore_permissions=True)
            created.append(team_name)
            print(f"✅ Created team: {team_name}")
        else:
            print(f"⏭️  Team exists: {team_name}")
    
    frappe.db.commit()
    return {"created": created}

@frappe.whitelist()
def create_test_users():
    """Create test users with roles and teams"""
    
    # First ensure teams exist
    create_test_teams()
    
    # Get team names (they use auto-generated names)
    it_team = frappe.db.get_value("HD Team", {"team_name": "IT Support"}, "name")
    hr_team = frappe.db.get_value("HD Team", {"team_name": "HR Support"}, "name")
    
    users = [
        {
            "email": "it_agent@test.local",
            "first_name": "IT",
            "last_name": "Agent",
            "assigned_team": it_team,
            "roles": ["Helpdesk User Internal", "Agent"]
        },
        {
            "email": "it_manager@test.local",
            "first_name": "IT",
            "last_name": "Manager",
            "assigned_team": it_team,
            "roles": ["Helpdesk Manager Internal", "Agent Manager", "Agent"]
        },
        {
            "email": "hr_agent@test.local",
            "first_name": "HR",
            "last_name": "Agent",
            "assigned_team": hr_team,
            "roles": ["Helpdesk User Internal", "Agent"]
        },
        {
            "email": "hr_manager@test.local",
            "first_name": "HR",
            "last_name": "Manager",
            "assigned_team": hr_team,
            "roles": ["Helpdesk Manager Internal", "Agent Manager", "Agent"]
        },
        {
            "email": "admin@test.local",
            "first_name": "Helpdesk",
            "last_name": "Admin",
            "assigned_team": None,
            "roles": ["Helpdesk Admin Internal", "Agent Manager", "Agent"]
        }
    ]
    
    created = []
    
    for user_data in users:
        email = user_data["email"]
        if frappe.db.exists("User", email):
            # Update existing user
            user = frappe.get_doc("User", email)
            user.assigned_team = user_data["assigned_team"]
            user.save(ignore_permissions=True)
            print(f"⏭️  Updated user: {email}")
        else:
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "enabled": 1,
                "send_welcome_email": 0,
                "new_password": "TestP@ss123!",
                "assigned_team": user_data["assigned_team"]
            })
            for role in user_data["roles"]:
                user.append("roles", {"role": role})
            user.insert(ignore_permissions=True)
            created.append(email)
            print(f"✅ Created user: {email}")
        
        # Create HD Agent record if doesn't exist
        if not frappe.db.exists("HD Agent", email):
            frappe.get_doc({
                "doctype": "HD Agent",
                "user": email,
                "agent_name": f"{user_data['first_name']} {user_data['last_name']}",
                "is_active": 1
            }).insert(ignore_permissions=True)
            print(f"   → Created HD Agent: {email}")
    
    frappe.db.commit()
    return {"created": created}

@frappe.whitelist()
def create_test_tickets():
    """Create test tickets for permission testing"""
    
    # Get team names
    it_team = frappe.db.get_value("HD Team", {"team_name": "IT Support"}, "name")
    hr_team = frappe.db.get_value("HD Team", {"team_name": "HR Support"}, "name")
    
    if not it_team or not hr_team:
        return {"error": "Teams not found. Run create_test_users first."}
    
    tickets = [
        {
            "subject": "IT Ticket 1 - Assigned to IT",
            "description": "IT team's ticket assigned to IT",
            "raised_by": "it_agent@test.local",
            "agent_group": it_team,
            "originating_team": it_team
        },
        {
            "subject": "IT Ticket 2 - Raised by IT, Assigned to HR",
            "description": "IT created this but assigned to HR (customer view for IT)",
            "raised_by": "it_agent@test.local",
            "agent_group": hr_team,
            "originating_team": it_team
        },
        {
            "subject": "HR Ticket 1 - Assigned to HR",
            "description": "HR team's ticket assigned to HR",
            "raised_by": "hr_agent@test.local",
            "agent_group": hr_team,
            "originating_team": hr_team
        },
        {
            "subject": "HR Ticket 2 - Raised by HR, Assigned to IT",
            "description": "HR created this but assigned to IT (customer view for HR)",
            "raised_by": "hr_agent@test.local",
            "agent_group": it_team,
            "originating_team": hr_team
        },
    ]
    
    created = []
    
    for ticket_data in tickets:
        # Check if similar ticket exists
        exists = frappe.db.exists("HD Ticket", {"subject": ticket_data["subject"]})
        if exists:
            print(f"⏭️  Ticket exists: {ticket_data['subject']}")
            continue
            
        # Set initial_sync flag to skip SLA validation and email
        frappe.flags.initial_sync = True
        
        # Get status name
        status_name = frappe.db.get_value("HD Ticket Status", {"label_agent": "Open"}, "name")
        
        ticket = frappe.get_doc({
            "doctype": "HD Ticket",
            "status": status_name,
            **ticket_data
        })
        ticket.insert(ignore_permissions=True)
        
        frappe.flags.initial_sync = False
        created.append(ticket.name)
        print(f"✅ Created ticket: {ticket.name} - {ticket_data['subject']}")
    
    frappe.db.commit()
    return {"created": created}

@frappe.whitelist()
def test_permissions():
    """Test permission logic"""
    from helpdesk_internal_custom.permissions import (
        hd_ticket_has_permission, 
        hd_ticket_permission_query,
        get_user_team
    )
    
    # Get test data
    it_team = frappe.db.get_value("HD Team", {"team_name": "IT Support"}, "name")
    
    results = {}
    
    # Test IT Agent
    user = "it_agent@test.local"
    results[user] = {
        "team": get_user_team(user),
        "query": hd_ticket_permission_query(user)
    }
    
    # Test Admin
    user = "admin@test.local"
    results[user] = {
        "team": get_user_team(user),
        "query": hd_ticket_permission_query(user)
    }
    
    return results

@frappe.whitelist()
def test_ticket_access():
    """Test which users can see which tickets"""
    from helpdesk_internal_custom.permissions import (
        hd_ticket_has_permission, 
        hd_ticket_permission_query,
        get_user_team
    )
    
    tickets = frappe.get_all("HD Ticket", fields=["name", "subject", "agent_group", "originating_team"])
    users = ["it_agent@test.local", "hr_agent@test.local", "admin@test.local"]
    
    results = {}
    
    for user in users:
        user_team = get_user_team(user)
        results[user] = {
            "team": user_team,
            "can_access": {}
        }
        
        for ticket in tickets:
            doc = frappe.get_doc("HD Ticket", ticket.name)
            can_read = hd_ticket_has_permission(doc, "read", user)
            can_write = hd_ticket_has_permission(doc, "write", user)
            
            results[user]["can_access"][ticket.name] = {
                "subject": ticket.subject[:40],
                "read": can_read,
                "write": can_write,
                "agent_group": ticket.agent_group,
                "originating_team": ticket.originating_team
            }
    
    return results
