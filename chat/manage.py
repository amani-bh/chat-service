#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import py_eureka_client.eureka_client as eureka_client

def eureka_init():
    eureka_client.init(
        eureka_server="http://localhost:8761",
        app_name="chat-service",
        instance_host="localhost",
        instance_port=8000,
    )

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    eureka_init()
