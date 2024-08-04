import os
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException

available_statuses = [
    "NEW",
    "OPEN",
    "IN_PROGRESS",
    "OPEN_DEAL",
    "UNQUALIFIED",
    "ATTEMPTED_TO_CONTACT",
    "CONNECTED",
    "BAD_TIMING",
]


def get_new_leads():
    client = hubspot.Client.create(access_token=os.getenv("HUBSPOT_API_KEY"))
    try:
        api_response = client.crm.contacts.basic_api.get_page(
            limit=100,  # Adjust the limit as needed
            properties=["email", "firstname", "lastname", "hs_lead_status"],
            archived=False,
        )
        new_leads = [
            {
                "lead_id": contact.properties.get("hs_lead_status"),
                "lead_name": f"{contact.properties.get('firstname', '')} {contact.properties.get('lastname', '')}",
                "lead_email": contact.properties.get("email")
            }
            for contact in api_response.results
            if contact.properties.get("hs_lead_status") == "NEW"
        ]
        return new_leads
    except ApiException as e:
        print("Exception when calling basic_api->get_page: %s\n" % e)
        return []


def update_lead_status(lead_id, status):
    client = hubspot.Client.create(access_token=os.getenv("HUBSPOT_API_KEY"))
    if status not in available_statuses:
        print(
            f"Invalid status: {status}. Must be one of {available_statuses}."
        )
        return None

    properties = {
        "hs_lead_status": status,
    }
    simple_public_object_input = SimplePublicObjectInput(properties=properties)
    try:
        api_response = client.crm.contacts.basic_api.update(
            contact_id=lead_id,
            simple_public_object_input=simple_public_object_input,
        )
        return api_response
    except ApiException as e:
        print("Exception when calling basic_api->update: %s\n" % e)
        return None
