# Development Environment Setup

## Prerequisites Installed:
- Ubuntu 24.04 LTS
- Python 3.12.3
- Node.js 18.19.1
- MariaDB 10.11.13
- Redis 7.0.15
- yarn 1.22.22
- wkhtmltopdf 0.12.6

## Frappe Bench Installation

```bash
# Install bench
pip3 install frappe-bench --break-system-packages
export PATH="$HOME/.local/bin:$PATH"

# Initialize bench with Frappe v15
bench init --frappe-branch version-15 frappe-bench
cd frappe-bench

# Create site
bench new-site helpdesk.localhost --db-root-password frappe123 --admin-password admin123

# Install apps
bench get-app telephony --branch develop
bench get-app helpdesk --branch main
bench --site helpdesk.localhost install-app helpdesk
```

## Custom App

The custom app is located at:
```
/home/exedev/frappe-bench/apps/helpdesk_internal_custom
```

## Starting Development

```bash
export PATH="$HOME/.local/bin:$PATH"
cd /home/exedev/frappe-bench
bench start
```

## Accessing the Site

- **Frappe Desk**: http://helpdesk.localhost:8000
- **Helpdesk App**: http://helpdesk.localhost:8000/helpdesk

## Credentials

- **Administrator**: admin123
- **MariaDB root**: frappe123
- **Database**: _6394f86cc9bf73b4

## CORS Configuration

Update `sites/helpdesk.localhost/site_config.json` to add:
```json
{
  "allow_cors": "*",
  "ignore_csrf": 1,
  "developer_mode": 1
}
```
