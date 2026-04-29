#!/bin/bash
# Start monitor daemon in background
python src/monitor/monitor.py &
# Start web dashboard in foreground
python src/web/app.py
