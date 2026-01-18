# Key Decisions Log

## Session 1 - 2026-01-18

### 1. Frappe Version Choice
- **Decision**: Use Frappe v15 (version-15 branch)
- **Rationale**: Latest stable version with modern features
- **Impact**: All code must be compatible with v15 APIs

### 2. Helpdesk Branch Choice
- **Decision**: Use main branch for Helpdesk
- **Rationale**: Most stable release
- **Impact**: Need to track Helpdesk releases for compatibility

### 3. App Structure
- **Decision**: Create modular structure with separate files for:
  - permissions.py (central permission logic)
  - overrides/ticket.py (document hooks)
  - api/ticket.py (custom endpoints)
- **Rationale**: Better maintainability and clear separation of concerns
- **Impact**: Easier to test and debug individual components

### 4. Role Naming Convention
- **Decision**: Suffix internal roles with "Internal" (e.g., "Helpdesk User Internal")
- **Rationale**: Distinguish from standard Helpdesk roles
- **Impact**: Clear separation from vanilla Helpdesk permissions

### 5. Installation Hook
- **Decision**: Use after_install hook for setup
- **Rationale**: Automatic setup on app installation
- **Impact**: Fresh installations get roles and fields automatically

### 6. Redis Configuration
- **Decision**: Use standard port 6379 for all Redis connections
- **Rationale**: Default Redis installation uses this port
- **Impact**: Simpler configuration, standard setup
