# Current Blockers

## None Currently

---

## Resolved Blockers:

### 1. Telephony Module Not Found (Resolved)
- **Date**: 2026-01-18
- **Issue**: Helpdesk install failed with "No module named 'telephony'"
- **Cause**: Helpdesk requires telephony app as dependency
- **Solution**: `bench get-app telephony --branch develop` (main branch didn't exist)
- **Status**: ✅ Resolved

### 2. Redis Connection Error (Resolved)
- **Date**: 2026-01-18  
- **Issue**: "Error 111 connecting to 127.0.0.1:13000"
- **Cause**: common_site_config.json had non-standard Redis ports
- **Solution**: Updated redis_cache, redis_queue, redis_socketio to use port 6379
- **Status**: ✅ Resolved
