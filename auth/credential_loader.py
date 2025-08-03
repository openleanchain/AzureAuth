"""
credential_loader.py

This module provides a class `AuthCredentialLoader` for securely loading Azure credentials and configuration
from environment variables or system environment settings. It supports two modes of credential resolution:
- "env": Directly reads values from a .env file using python-dotenv.
- "system": Resolves values from system environment variables referenced in the .env file.

Key Features:
- Loads Azure tenant ID, client ID, and client secret for authentication.
- Retrieves project endpoint and OpenAI configuration (endpoint, API key, version).
- Validates presence of required environment variables and raises informative errors.
- Designed for use in applications that integrate with Azure services and OpenAI APIs.

Usage:
    loader = AuthCredentialLoader(env_path=".env")
    credentials = loader.get_credentials()
    endpoint = loader.get_project_endpoint()
    openai_config = loader.get_openai_config()

Dependencies:
- python-dotenv
- azure-identity

Author: openleanchain
Date: 2025-08-03

License:
This script is provided 'as-is', without any express or implied warranty.
You are free to use, modify, and distribute this code at your own risk.
The author(s) shall not be held liable for any damages arising from the use of this software.
"""

# Import the os module to interact with the operating system
import os
# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv
# Import Azure SDK's ClientSecretCredential for authentication
from azure.identity import ClientSecretCredential

# Define a class to load and manage authentication credentials
class AuthCredentialLoader:
    # Initialize the class with the path to the .env file and load environment variables
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        self.auth_credential_mode = None
        self.load_env()
        self.set_mode()

    # Load environment variables from the specified .env file
    def load_env(self):
        load_dotenv(self.env_path)

    # Set the mode for credential resolution (either 'env' or 'system')
    def set_mode(self):
        self.auth_credential_mode = os.getenv("AUTH_CREDENTIAL_MODE", "env").lower()
        if self.auth_credential_mode not in ["env", "system"]:
            raise ValueError(f"Invalid AUTH_CREDENTIAL_MODE: {self.auth_credential_mode}. Must be 'env' or 'system'.")

    # Resolve the value of a given key based on the credential mode
    def resolve(self, key):
        raw_value = os.getenv(key)
        if not raw_value:
            raise ValueError(f"Missing config value for {key}")
        
        if self.auth_credential_mode == "env":
            return raw_value
        elif self.auth_credential_mode == "system":
            resolved = os.environ.get(raw_value)
            if not resolved:
                raise ValueError(f"System environment variable '{raw_value}' (from {key}) is not set")
            return resolved

    # Retrieve Azure credentials using resolved environment variables
    def get_credentials(self):
        tenant_id = self.resolve("AZURE_TENANT_ID")
        client_id = self.resolve("AZURE_CLIENT_ID")
        client_secret = self.resolve("AZURE_CLIENT_SECRET")

        return ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

    # Retrieve the Azure AI project endpoint from environment variables
    def get_project_endpoint(self):
        return self.resolve("AZURE_AI_PROJECT_ENDPOINT")

    # Retrieve OpenAI configuration details from environment variables
    def get_openai_config(self):
        return {
            "endpoint": self.resolve("AZURE_OPENAI_ENDPOINT"),
            "api_key": self.resolve("AZURE_OPENAI_API_KEY"),
            "api_version": self.resolve("AZURE_OPENAI_API_VERSION")
        }

