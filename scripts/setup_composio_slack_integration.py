import os
from dotenv import load_dotenv
from composio import ComposioToolSet

def setup_slack():
    load_dotenv()
    toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
    
    integration = toolset.get_integration(
        id="97fb6b0d-c5ae-47d6-95c1-3011e6616d59"
    )
    
    # Print expected auth fields
    print("Required authentication fields:")
    print(integration.expectedInputFields)
    
    # Get connection URL
    connection_request = toolset.initiate_connection(
        integration_id=integration.id,
        entity_id="default",
    )
    
    print("\nPlease visit this URL to authorize Slack:")
    print(connection_request.redirectUrl)
    print(f"\nConnection ID: {connection_request.connectedAccountId}")

if __name__ == "__main__":
    setup_slack() 