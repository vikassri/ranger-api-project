import gradio as gr
import requests
import openai
import json

# Apache Ranger API Base URL
RANGER_API_BASE_URL = "https://ccycloud.cdpy.root.comops.site:6182/service/public/v2/api/policy"

hive_create_template = """{
    "service": "cm_hive",
    "name": "POLICY_NAME",
    "policyType": 0,
    "resources": {
        "database": {"values": DBASE, "isRecursive": false},
        "table": {"values": ["*"], "isRecursive": false},
        "column": {"values": ["*"], "isRecursive": false}
    },
    "policyItems": [
        {
            "users": ["USERNAME"],
            "accesses": [{"type": perm, "isAllowed": true} for perm in PERMISSIONS],
            "delegateAdmin": false
        }
    ]
}
"""

def get_policies(user=None):
    """Fetch policies from Apache Ranger API and return in JSON format."""
    url = f"{RANGER_API_BASE_URL}?user={user}" if user else RANGER_API_BASE_URL
    response = requests.get(url, auth=("admin", "Password1"), verify=False)
    
    if response.status_code == 200:
        policies = response.json()
        if not policies:
            return json.dumps({"message": "No relevant policies found."}, indent=4)
        return json.dumps(policies, indent=4)
    
    return json.dumps({"error": response.text}, indent=4)


def delete_policy(policy_name):
    """Delete a specific policy and return response in JSON format."""
    print("Policie_name: ",policy_name)
    policies = get_policies()
    policy_to_delete = next((p for p in json.loads(policies) if p['name'] == policy_name), None)
    if not policy_to_delete:
        return json.dumps({"error": "Policy not found."}, indent=4)
    
    delete_url = f"{RANGER_API_BASE_URL}/{policy_to_delete['id']}"
    response = requests.delete(delete_url, auth=("admin", "Password1"), verify=False)
    
    if response.status_code == 204:
        return json.dumps({"status": "Policy deleted successfully."}, indent=4)
    return json.dumps({"error": response.text}, indent=4)


def modify_policy(policy_id, updated_data):
    """Modify an existing policy and return response in JSON format."""
    url = f"{RANGER_API_BASE_URL}/{policy_id}"
    response = requests.put(url, json=updated_data, auth=("admin", "Password1"), verify=False)
    if response.status_code == 200:
        return json.dumps({"status": "Policy updated successfully."}, indent=4)
    return json.dumps({"error": response.text}, indent=4)


def create_policy(policy_data):
    """Create a new policy and return response in JSON format."""
    print("policy_data:", policy_data)
    response = requests.post(RANGER_API_BASE_URL, json=policy_data, auth=("admin", "Password1"), verify=False)
    if response.status_code == 200:
        return json.dumps({"status": "Policy created successfully."}, indent=4)
    return json.dumps({"error": response.text}, indent=4)

import uuid
def generate_policy_name():
    return str(uuid.uuid4())

def classify_intent(user_input):
    """Use OpenAI to determine user intent (get, create, delete, modify)."""
    prompt = f"""
    Classify the following user request into one of the intents: get_policy, create_policy, delete_policy, modify_policy.
    Convert component name eg. hive, hbase etc name into lowercase and add cm_ as prefix
    if intent is delete_policy there will be policy name given if not please ask for policy name
    if intent is create_policy policy name will be test_policy_{generate_policy_name()}
    use double quotes for string

    Request: "{user_input}"
    
    Response format: {{"intent": "<intent>", "details": <json_details_if_needed>}}
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an AI that classifies user requests into specific intents."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def chatbot_response(user_input, history=[]):
    """Processes user input using OpenAI classification and determines the appropriate API call."""
    classification = classify_intent(user_input)
    
    try:
        intent_data = json.loads(classification)  # Convert string to dict
        intent = intent_data.get("intent")
        details = intent_data.get("details", {})
        
        if intent == "get_policy":
            return get_policies(details.get("user"))
        elif intent == "delete_policy":
            print("details: ", details)
            return delete_policy(details.get("policy_name"))
        elif intent == "modify_policy":
            return modify_policy(details.get("policy_id"), details.get("updated_data"))
        elif intent == "create_policy":
            print(details)
            if details.get("component") == "cm_hive":
                print("Replacing Values")
                policy_json = hive_create_template.replace("POLICY_NAME",details.get("policy_name")).replace("DBASE",str(details.get("databases"))).replace("USERNAME",details.get("user")).replace("PERMISSIONS",str(details.get("permissions")))
                print(policy_json)
                return create_policy(json.loads(policy_json))
            return create_policy(details)
    
    except Exception as e:
        return json.dumps({"error": f"Error processing request: {str(e)}"}, indent=4)
    
    return json.dumps({"error": "Invalid request. Please provide more details."}, indent=4)


demo = gr.ChatInterface(chatbot_response, title="Apache Ranger Policy Chatbot",
                        description="Interact with Apache Ranger Policy Manager using natural language.")


demo.launch()
