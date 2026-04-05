#!/bin/bash
# Run database migrations before starting the app
# Continue even if migrations fail (they might already be applied)
alembic upgrade head || echo "Migrations may already be applied, continuing..."
