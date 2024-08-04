from litellm import completion
from src.prompts import lead_score_prompt

def score_lead(company_profile, open_positions):
    """
    Scores the lead based on the company profile and open positions.
    
    @param company_profile: The profile of the company.
    @param open_positions: The open positions at the company.
    @return: The lead score.
    """
    lead_data = f"""
    Company Profile: {company_profile}
    Open Positions: {open_positions}
    """
    messages = [
        {"role": "system", "content": lead_score_prompt},
        {"role": "user", "content": lead_data}
    ]
    response = completion(
        model="groq/llama3-70b-8192",
        messages=messages,
        temperature=0.1
    )
    response_message = response.choices[0].message.content
    return response_message