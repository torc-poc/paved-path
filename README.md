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
## Usage

This GitHub Action triggers AAP to create or update a Workflow Job Template based on a composition file and unified job templates.

### Minimal Example (External Usage)

```yaml
name: Register AAP Workflow

on:
  workflow_dispatch:

jobs:
  register-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout LOB repo
        uses: actions/checkout@v4

      - name: Register AAP Workflow
        uses: torc-poc/aap-workflow-action@v1
        with:
          aap_url: https://abc.aap-torc.xyz
          aap_token: ${{ secrets.AAP_TOKEN }}
          workflow_file: compositions/asp-sql-webapp.json
```
