# AAP Workflow Registration GitHub Action

This GitHub Action registers a workflow in Ansible Automation Platform based on a unified JSON spec.

## 🔧 Inputs

- `workflow_file`: Path to a unified JSON workflow file (e.g., `asp-sql-webapp_aap.json`)

## 📦 Environment Variables

The following **must** be set in your GitHub workflow or repo secrets:

- `AAP_HOST`: URL to your AAP controller, e.g. `https://abc.aap-torc.xyz`
- `AAP_TOKEN`: Bearer token for API access

## 🧪 Example Usage

```yaml
name: Register AAP Workflow

on:
  workflow_dispatch:

jobs:
  register:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Use AAP Workflow Action
        uses: ./  # path to this action repo
        with:
          workflow_file: workflows/asp-sql-webapp_aap.json
        env:
          AAP_HOST: ${{ secrets.AAP_HOST }}
          AAP_TOKEN: ${{ secrets.AAP_TOKEN }}
```
# paved-path
