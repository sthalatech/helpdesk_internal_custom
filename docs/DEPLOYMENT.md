# Deployment Guide

## Prerequisites
- Frappe Framework v15+
- Frappe Helpdesk installed
- MariaDB 10.3+
- Redis 6+

## Installation Steps

1. Get the app:
```bash
bench get-app https://github.com/sthalatech/helpdesk_internal_custom
```

2. Install on site:
```bash
bench --site [site-name] install-app helpdesk_internal_custom
```

3. Run migrations:
```bash
bench --site [site-name] migrate
```

4. Create teams and assign users via Desk or API

## Configuration

### CORS (for development)
Add to `site_config.json`:
```json
{
  "allow_cors": "*",
  "ignore_csrf": 1
}
```

### Production
```json
{
  "allow_cors": "https://yourdomain.com",
  "ignore_csrf": 0
}
```

## Rollback

To uninstall:
```bash
bench --site [site-name] uninstall-app helpdesk_internal_custom
```
