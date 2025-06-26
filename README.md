# Paved Path Framework

Core GitHub Action for registering and managing workflow templates in Ansible Automation Platform (AAP).

## Directory Structure

```
paved-path/
├── action.yml                    # GitHub Action definition
├── entrypoint.sh                # Action entrypoint script
├── register_workflow_template.py # Template registration script
└── README.md                    # This documentation
```

## Components

### action.yml
GitHub Action definition that:
- Sets up Python environment
- Configures AAP credentials
- Executes workflow registration

Key Parameters:
- `controller_host`: AAP controller hostname
- `controller_username`: AAP username
- `controller_password`: AAP password
- `github_token`: GitHub access token
- `workflow_template`: Path to workflow template

### entrypoint.sh
Bash script that:
- Validates environment
- Sets up Python dependencies
- Executes registration script
- Handles error conditions

Features:
- Environment validation
- Dependency installation
- Error handling
- Exit code management

### register_workflow_template.py
Python script for workflow registration:
- Connects to AAP
- Validates workflow template
- Creates/updates workflow
- Sets up job templates

Key Functions:
- Template validation
- AAP API interaction
- Error handling
- Status reporting

## Usage

### GitHub Workflow Example
```yaml
name: Register AAP Workflow
on:
  push:
    paths:
      - 'workflows/**'

jobs:
  register:
    runs-on: ubuntu-latest
    steps:
      - uses: ./paved-path
        with:
          controller_host: ${{ secrets.AAP_HOST }}
          controller_username: ${{ secrets.AAP_USERNAME }}
          controller_password: ${{ secrets.AAP_PASSWORD }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          workflow_template: './workflows/example.json'
```

## Best Practices

1. **Security**
   - Use GitHub secrets for credentials
   - Validate input parameters
   - Handle errors gracefully
   - Log appropriately

2. **Template Management**
   - Version control templates
   - Validate before registration
   - Use consistent naming
   - Document dependencies

3. **Error Handling**
   - Validate inputs
   - Check API responses
   - Provide clear error messages
   - Handle retries appropriately

## Common Operations

### Registering New Workflow
1. Create workflow template
2. Configure GitHub Action
3. Set required secrets
4. Push changes

### Updating Existing Workflow
1. Modify workflow template
2. Push changes
3. Action automatically updates

### Troubleshooting
1. Check Action logs
2. Verify AAP connectivity
3. Validate template syntax
4. Check permissions

## Integration Points

### GitHub
- Actions workflow
- Secrets management
- Repository integration
- Event triggers

### AAP
- Controller API
- Template management
- Job template creation
- Workflow updates

## Error Handling

### Common Issues
1. Authentication failures
   - Check credentials
   - Verify secret configuration
   - Check API access

2. Template validation
   - Verify JSON syntax
   - Check required fields
   - Validate dependencies

3. Registration failures
   - Check AAP permissions
   - Verify template format
   - Review API responses
