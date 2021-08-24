#!/bin/bash

gunicorn -c gunicorn.conf aiot_server_system.wsgi:application