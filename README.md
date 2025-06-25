# AAP Workflow Registration GitHub Action

This GitHub Action registers a workflow with Ansible Automation Platform using a unified JSON spec.

## Inputs

| Name           | Description                             | Required |
|----------------|-----------------------------------------|----------|
| `aap_url`      | AAP base URL                            | ✅        |
| `aap_token`    | API token                               | ✅        |
| `workflow_file`| Path to the unified JSON spec file      | ✅        |

## Example usage

```yaml
name: Register Paved Path
on:
  workflow_dispatch:

jobs:
  register-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout LOB repo
        uses: actions/checkout@v4

      - name: Register AAP Workflow
        uses: torc-poc/paved-path@main
        with:
          aap_url: https://abc.aap-torc.xyz
          aap_token: ${{ secrets.AAP_TOKEN }}
          workflow_file: compositions/asp-sql-webapp-aap.json
```
