# Testing Documentation

## Test Users (To Be Created)

| User | Team | Role |
|------|------|------|
| user_a1@test.com | Team A | Helpdesk Manager Internal |
| user_a2@test.com | Team A | Helpdesk User Internal |
| user_b1@test.com | Team B | Helpdesk Manager Internal |
| user_b2@test.com | Team B | Helpdesk User Internal |
| admin@test.com | - | System Manager |

## Test Scenarios

### Scenario 1: Ticket Creation
- [ ] User A1 creates ticket assigned to Team B
- [ ] Verify originating_team auto-set to Team A
- [ ] Verify A1 can see ticket in "My Raised Tickets"
- [ ] Verify B1 can see ticket in "My Team Tickets"

### Scenario 2: Permission Isolation
- [ ] User A2 cannot see Team B's internal tickets
- [ ] User B2 cannot edit tickets raised by Team A

### Scenario 3: Assignment Restrictions
- [ ] Manager can assign only to own team members
- [ ] Cross-team assignment is blocked

### Scenario 4: Admin Access
- [ ] Admin can see all tickets
- [ ] Admin can assign to any team

### Scenario 5: API Security
- [ ] Direct API calls respect team boundaries

## Test Results

*No tests run yet*
