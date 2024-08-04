from litellm import completion
from src.prompts import personalize_email_prompt

def personalize_email(company_profile, lead_profile):
    """
    Generates a personalized email based on the company profile and lead profile.
    
    @param company_profile: The profile of the company.
    @param lead_profile: The profile of the lead.
    @return: The personalized email content.
    """
    lead_data = f"""
    LinkedIn Lead Profile: {lead_profile}\n

    Company Profile: {company_profile}
    """
    messages = [
        {"role": "system", "content": personalize_email_prompt},
        {"role": "user", "content": lead_data}
    ]
    response = completion(
        model="groq/llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.1
    )
    response_message = response.choices[0].message.content
    return response_message
