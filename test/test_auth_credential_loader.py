import os
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI
from common.auth.credential_loader import AuthCredentialLoader

# Get credentials from environment variables
loader = AuthCredentialLoader()
# credential using the service principal
credentials = loader.get_credentials()
project_endpoint = loader.get_project_endpoint()
print("project_endpoint", project_endpoint)
# Azure OpenAI specific variables
openai_config = loader.get_openai_config()

# print("Azure credentials and configuration loaded successfully.")

# Initialize the AI Project client with the endpoint and credential
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=credentials
)

try:
    # Example: list your deployments or perform inference
    deployments = list(project_client.deployments.list())
    print(f"Found {len(deployments)} model deployments")
    for deployment in deployments:
        print(deployment.name)

    # Perform chat completions (if you have deployments)
    if deployments:
        # Get connection info for Azure OpenAI
        connections = project_client.connections.list()
        print(f"Total connections: {len(list(connections))}")

        for conn in connections:
            print(f"Name: {conn.name}")
            print(f"Type: {conn.connection_type}")
            print(f"Resource URL: {conn.properties.get('resource_url')}")
            print("----")
            if "openai" in conn.name.lower():
                print(f"*********OpenAI connection: {conn.name}")

        # Use Azure OpenAI client directly
        if openai_config:
            client = AzureOpenAI(
                openai_config
            )

            response = client.chat.completions.create(
                model="gpt-4.1-nano",  # Use one of your available models
                messages=[
                    {"role": "user", "content": "Hello, how are you?"}
                ]
            )

            print("Response:", response.choices[0].message.content)
        else:
            print("Azure OpenAI endpoint or API key not provided in .env file")
    else:
        print("No model deployments found")

except Exception as e:
    print(f"Error: {e}")
    print("Make sure all your environment variables are correctly set in the .env file")

