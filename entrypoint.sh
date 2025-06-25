#!/bin/bash
set -euo pipefail

WORKFLOW_FILE="$1"

echo "📂 Workflow file: $WORKFLOW_FILE"
python3 register_workflow_template.py "$WORKFLOW_FILE"
