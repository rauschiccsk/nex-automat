# Scripts Directory

Production scripts for NEX Automat v2.0 deployment and management.

## Deployment

| Script | Description |
|--------|-------------|
| `deploy_fresh.py` | Main deployment script - clones repo, creates venv, installs deps, configures service |

## Service Management

| Script | Description |
|--------|-------------|
| `manage_service.py` | Windows service control (start/stop/restart/status/logs) |

## Validation & Testing

| Script | Description |
|--------|-------------|
| `preflight_check.py` | Pre-flight validation before deployment (6 checks) |
| `error_handling_tests.py` | Error handling validation (12 tests) |
| `performance_tests.py` | Performance benchmarks (6 tests) |
| `create_baseline.py` | Creates performance baseline for comparison |
| `test_database_connection.py` | Tests PostgreSQL connectivity |
| `validate_config.py` | Validates config.yaml and config_customer.py |

## Dependencies

| File | Description |
|------|-------------|
| `requirements.txt` | Python dependencies for scripts |

---

**Usage Examples:**

```powershell
# Fresh deployment
python deploy_fresh.py

# Service management
python manage_service.py status
python manage_service.py restart
python manage_service.py logs

# Validation
python preflight_check.py
python error_handling_tests.py
python performance_tests.py
```
