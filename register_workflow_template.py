import os
import json
import requests
import sys

AAP_HOST = os.environ["AAP_HOST"]
AAP_TOKEN = os.environ["AAP_TOKEN"]
ORG_NAME = os.getenv("AAP_ORG", "TORC")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AAP_TOKEN}"
}

def get_id(endpoint, name):
    response = requests.get(f"{AAP_HOST}/api/v2/{endpoint}/?name={name}", headers=HEADERS)
    response.raise_for_status()
    results = response.json()["results"]
    if not results:
        raise Exception(f"{name} not found in {endpoint}")
    return results[0]["id"]

def create_or_update_workflow(name, org_id, inventory_id, description, extra_vars):
    response = requests.get(f"{AAP_HOST}/api/v2/workflow_job_templates/?name={name}", headers=HEADERS)
    results = response.json()["results"]

    payload = {
        "name": name,
        "organization": org_id,
        "inventory": inventory_id,
        "description": description,
        "extra_vars": json.dumps(extra_vars),
        "labels": ["torc"]
    }

    if results:
        print(f"🔁 Workflow '{name}' already exists.")
        workflow_id = results[0]["id"]
        patch_response = requests.patch(f"{AAP_HOST}/api/v2/workflow_job_templates/{workflow_id}/", headers=HEADERS, json=payload)
        patch_response.raise_for_status()
        return workflow_id
    else:
        post_response = requests.post(f"{AAP_HOST}/api/v2/workflow_job_templates/", headers=HEADERS, json=payload)
        post_response.raise_for_status()
        print(f"✅ Created workflow: {name}")
        return post_response.json()["id"]

def clear_existing_nodes(workflow_id):
    response = requests.get(f"{AAP_HOST}/api/v2/workflow_job_templates/{workflow_id}/workflow_nodes/", headers=HEADERS)
    for node in response.json()["results"]:
        node_id = node["id"]
        print(f"🧹 Deleting existing node {node_id}")
        requests.delete(f"{AAP_HOST}/api/v2/workflow_job_template_nodes/{node_id}/", headers=HEADERS)

def create_node(workflow_id, job_template_id, identifier, node_vars=None):
    payload = {
        "workflow_job_template": workflow_id,
        "unified_job_template": job_template_id,
        "identifier": identifier
    }
    if node_vars:
        payload["extra_data"] = node_vars

    response = requests.post(f"{AAP_HOST}/api/v2/workflow_job_template_nodes/", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["id"]

def link_nodes(source_id, target_id, relation="success"):
    relation_url = {
        "success": "success_nodes",
        "failure": "failure_nodes",
        "always": "always_nodes"
    }[relation]
    url = f"{AAP_HOST}/api/v2/workflow_job_template_nodes/{source_id}/{relation_url}/"
    response = requests.post(url, headers=HEADERS, json={"id": target_id})
    response.raise_for_status()

def build_workflow(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    name = data["workflow"]
    description = data.get("description", "")
    inventory = data["inventory"]
    extra_vars = data.get("extra_vars", {})
    nodes = data["nodes"]

    print(f"🔧 Setting up workflow '{name}'")
    org_id = get_id("organizations", ORG_NAME)
    workflow_id = create_or_update_workflow(name, org_id, inventory, description, extra_vars)
    clear_existing_nodes(workflow_id)

    node_map = {}
    for node in nodes:
        jt_name = node["job_template"]
        jt_id = get_id("job_templates", jt_name)
        node_vars = node.get("vars", {})
        node_id = create_node(workflow_id, jt_id, node["identifier"], node_vars)
        node_map[node["identifier"]] = node_id
        print(f"🧩 Created node '{node['identifier']}' → job_template '{jt_name}'")

    for node in nodes:
        src = node_map[node["identifier"]]
        for rel in ["success_nodes", "failure_nodes", "always_nodes"]:
            for tgt in node.get(rel, []):
                link_nodes(src, node_map[tgt], rel.replace("_nodes", ""))
                print(f"🔗 Linked '{node['identifier']}' {rel} → '{tgt}'")

    print("🎉 Workflow construction complete.")

if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else "workflows/asp-sql-webapp.json"
    build_workflow(json_file)
