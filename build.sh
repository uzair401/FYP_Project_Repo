#!/bin/bash

# Install required packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Setup groups and permissions
python manage.py setup_groups_and_permissions

# Apply database migrations
python manage.py migrate
