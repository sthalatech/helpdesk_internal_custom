# Development Environment Setup

## Quick Start (for new sessions)

```bash
# 1. Set PATH
export PATH="$HOME/.local/bin:$PATH"

# 2. Start services
sudo systemctl start mariadb
sudo systemctl start redis-server

# 3. Navigate to bench
cd /home/exedev/frappe-bench

# 4. Start development server
bench serve --port 8000
```

Access at: http://localhost:8000 or https://frappe-helpdesk.exe.xyz:8000

## Credentials

| Service | Username | Password |
|---------|----------|----------|
| Frappe Admin | Administrator | admin123 |
| MariaDB root | root | frappe123 |
| Database name | _6394f86cc9bf73b4 | MXXzanwoq3WV7cNn |

## Directory Structure

```
/home/exedev/
└── frappe-bench/                    # Frappe bench directory
    ├── apps/
    │   ├── frappe/                  # Frappe Framework v15
    │   ├── helpdesk/                # Frappe Helpdesk (vanilla - DO NOT MODIFY)
    │   ├── telephony/               # Telephony dependency
    │   └── helpdesk_internal_custom/ # OUR CUSTOM APP (modify this only)
    ├── sites/
    │   ├── helpdesk.localhost/      # Our development site
    │   │   └── site_config.json     # Site-specific config
    │   ├── apps.txt                 # Installed apps list
    │   ├── common_site_config.json  # Shared config
    │   └── currentsite.txt          # Default site
    ├── env/                         # Python virtual environment
    └── logs/                        # Log files
```

## Installed Apps

1. **frappe** - v15 (version-15 branch)
2. **telephony** - develop branch (helpdesk dependency)
3. **helpdesk** - main branch (vanilla Frappe Helpdesk)
4. **helpdesk_internal_custom** - Our custom app

## GitHub Repository

- **URL**: https://github.com/sthalatech/helpdesk_internal_custom
- **Branch**: main

## Custom Roles Created

- Helpdesk User Internal
- Helpdesk Manager Internal
- Helpdesk Admin Internal

## Bench Console Access

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
bench --site helpdesk.localhost console
```

## Common Commands

```bash
# Start development server
bench serve --port 8000

# Run migrations
bench --site helpdesk.localhost migrate

# Clear cache
bench --site helpdesk.localhost clear-cache

# Install app on site
bench --site helpdesk.localhost install-app [app_name]

# Access bench console
bench --site helpdesk.localhost console

# Build assets
bench build --app helpdesk_internal_custom

# Git push (from custom app directory)
cd /home/exedev/frappe-bench/apps/helpdesk_internal_custom
git add [files]
git commit -m "message"
git push origin main
```

## Configuration Files

### sites/helpdesk.localhost/site_config.json
```json
{
  "db_name": "_6394f86cc9bf73b4",
  "db_password": "MXXzanwoq3WV7cNn",
  "db_type": "mariadb",
  "allow_cors": "*",
  "ignore_csrf": 1,
  "developer_mode": 1
}
```

### sites/common_site_config.json
```json
{
  "redis_cache": "redis://127.0.0.1:6379",
  "redis_queue": "redis://127.0.0.1:6379",
  "webserver_port": 8000
}
```
