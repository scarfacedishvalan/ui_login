#!/bin/bash
# Simple launcher script for testing FastAPI app

# Example: Start a dummy process that listens on port 8080 for testing
# This will run a simple Python HTTP server in the background

nohup python -m http.server 8080 > /dev/null 2>&1 &