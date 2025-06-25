#!/bin/bash
set -euo pipefail

WORKFLOW_FILE="$1"

echo "🔧 Starting AAP workflow registration..."
echo "🌐 AAP_HOST = $AAP_HOST"
echo "🔐 AAP_TOKEN = [REDACTED]"
echo "📄 Workflow file: $WORKFLOW_FILE"

export AAP_TOKEN=$AAP_TOKEN
export AAP_HOST=$AAP_HOST

python3 $GITHUB_ACTION_PATH/register_workflow_template.py "$WORKFLOW_FILE"
