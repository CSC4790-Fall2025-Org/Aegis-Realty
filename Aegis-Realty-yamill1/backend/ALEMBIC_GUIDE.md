# Alembic Database Migration Guide

## Setup
```bash
# Initialize Alembic (only needed once)
alembic init migrations
```
### Creating and Applying Migrations
```bash
# Generate a migration based on model changes
alembic revision --autogenerate -m "Description of changes"

# Upgrade to the latest version
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Upgrade to a specific version
alembic upgrade <revision_id>
```

### Rolling Back Changes
```bash
# Downgrade by one version
alembic downgrade -1

# Downgrade to a specific version
alembic downgrade <revision_id>

# Downgrade to base (remove all migrations)
alembic downgrade base
```

### Checking Migration Status
```bash
# Show current migration version
alembic current

# Show migration history
alembic history

# Show migration history with details
alembic history -v
```

### Resetting Migrations 
```bash
# Remove versions directory contents
rm migrations/versions/*

# Create a fresh initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration
alembic upgrade head
```