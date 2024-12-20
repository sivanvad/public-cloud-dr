import requests
import json

# Ranger REST API endpoint
RANGER_API_URL = ""

# Ranger admin credentials
USERNAME = ""
PASSWORD = ""

# Authenticate (Basic Auth)
def authenticate(username, password):
    # Return the credentials as a tuple for HTTP Basic Authentication
    return (username, password)

# Get policies from Ranger
def get_policies():
    auth = authenticate(USERNAME, PASSWORD)
    
    # Send GET request to fetch policies
    response = requests.get(RANGER_API_URL, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching policies: {response.status_code}")
        return None


def update_prod_to_dr(data):
    # Check if 'resources.storageaccount.values' exists and contains one element
    values = data.get("resources", {}).get("storageaccount", {}).get("values", [])
    if len(values) == 1:
        # Get the first (and only) element in the array
        element = values[0]
        # Check and update 'name', 'description', and 'details' if they contain 'prod'
        if isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, str) and 'prod' in value:
                    print(f"Updating {key}: {value}")
                    element[key] = value.replace('prod', 'dr')
                elif isinstance(value, dict):
                    # Check within nested dictionaries (like 'details')
                    for nested_key, nested_value in value.items():
                        if isinstance(nested_value, str) and 'prod' in nested_value:
                            print(f"Updating {nested_key}: {nested_value}")
                            value[nested_key] = nested_value.replace('prod', 'dr')
    return data

# Update policies on the Ranger server
def update_policies_on_ranger(updated_policies):
    auth = authenticate(USERNAME, PASSWORD)
    for policy in updated_policies:
        policy_id = policy.get('id')
        if policy_id:
            url = f"{RANGER_API_URL}/{policy_id}"
            headers = {"Content-Type": "application/json"}
            response = requests.put(url, auth=auth, headers=headers, data=json.dumps(policy))
            if response.status_code == 200:
                print(f"Policy {policy_id} updated successfully.")
            else:
                print(f"Failed to update policy {policy_id}: {response.status_code}")
        else:
            print("Policy ID missing, cannot update.")
    
# Main function to fetch, update, and push policies
def main():
    # Step 1: Get policies from Ranger
    policies = get_policies()
    if policies:
        # Step 2: Update policies (replace 'prod' with 'dr')
        updated_policies = update_policies(policies)
        # Step 3: Push the updated policies back to Ranger
        update_policies_on_ranger(updated_policies)
    else:
        print("No policies found to update.")

if __name__ == "__main__":
    main()
