import requests
import json, urllib3, os
from config_tools import tools, base_url,user_url , columns_dict , policy_url

urllib3.disable_warnings()
def is_host_available(url, timeout=3):
    try:
        print(url)
        response = requests.head(url, timeout=timeout, verify=False)
        if response.status_code < 500:
            return True
    except requests.RequestException:
        return False
    
def api_request(method, url, **kwargs):
    USERNAME=os.environ["user"]
    PASSWORD=os.environ["pass"]
    RANGER_HOST=os.environ["host"]
    url = f"{RANGER_HOST}{url}"
    if is_host_available(url):
        auth = (USERNAME, PASSWORD)
        try:
            return getattr(requests, method.lower(), lambda *a, **k: None)(url,auth=auth, verify=False, **kwargs)
        except requests.RequestException as e:
            return type("response", (), {"status_code": "00", "text": "Please check the connection url"})()
    return type("response", (), {"status_code": "00", "text": "Please check the connection, Host is unavailable"})()
        

def get_policy_by_id(id=None):
    """Fetch policies from Apache Ranger API and return in JSON format."""
    url = f"{base_url}/{id}"
    response = api_request("get",url)
    if response.status_code == 200:
        policies = response.json()
        if not policies:
            return json.dumps({"message": "No relevant policies found."}, indent=4)
        return json.dumps(policies, indent=4)
    
    return json.dumps({"error": "Cluster is busy, please try again"}, indent=4)

def get_policy_by_user(user=None):
    """Fetch policies from Apache Ranger API and return in JSON format."""
    if user is not None:
        user = user.lower()
    url = f"{policy_url}?user={user}"
    response = api_request("get",url)
    if response.status_code == 200:
        policies = response.json()
        if not policies:
            return json.dumps({"message": "No relevant policies found."}, indent=4)
        return json.dumps(policies, indent=4)
    
    return json.dumps({"error": "Cluster is busy, please try again"}, indent=4)


def delete_policy_by_id(id):
    """Delete a specific policy by id and return response in JSON format."""
    url = f"{base_url}/{id}"
    response = api_request("delete",url)
    if response.status_code == 204:
        return json.dumps({"status": "Policy deleted successfully."}, indent=4)
    return json.dumps({"error": response.text}, indent=4)
        

def get_users(user):
    """Fetch users from Apache Ranger API and return in JSON format."""
    user = user.lower()
    url = f"{user_url}/{user}"
    response = api_request("get",url)
    if response.status_code == 200:
        users = response.json()
        if not users:
            return json.dumps({"message": "No relevant User found."}, indent=4)
        return json.dumps(users, indent=4)
    
    return json.dumps({"error": response.text}, indent=4)

def delete_users(user):
    """delete users from Apache Ranger API and return in JSON format."""
    url = f"{user_url}/{user}" 
    response = api_request("delete",url)
    if response.status_code == 200:
        users = response.json()
        if not users:
            return json.dumps({"message": "No relevant User found."}, indent=4)
        return json.dumps(users, indent=4)
    
    return json.dumps({"error": response.text}, indent=4)

def create_hive_policy(name=None, database=None, tables=None, users=None, groups=None, access=None, isadmin=False):
    if tables == "all":
        tables = "*"
    if database == "all":
        database = "*"
        
    hive_create_policy = {
        "service": "cm_hive",
        "name": name,
        "policyType": 0,
        "resources": {
            "database": {"values": [database], "isRecursive": False},
            "table": {"values": [tables], "isRecursive": False},
            "column": {"values": ["*"], "isRecursive": False}
        },
        "policyItems": [
            {
                "users": [users],
                "groups": [groups],
                "accesses": [{"type": perm, "isAllowed": True} for perm in access],
                "delegateAdmin": False
            }
        ]
    }
    return json.dumps(hive_create_policy)
        
def get_column(function_name: str):
    return columns_dict.get(function_name)

functions  = {
                "get_policy_by_id": get_policy_by_id,
                "delete_policy_by_id":delete_policy_by_id,
                "get_users": get_users,
                "delete_users": delete_users,
                "create_hive_policy": create_hive_policy,
                "get_policy_by_user": get_policy_by_user,
}
