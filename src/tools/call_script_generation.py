from litellm import completion
from src.prompts import spin_questions_prompt, cold_script_writer_prompt


def generate_spin_questions(lead_name, lead_profile, company_summary):
    """
    Generates SPIN (Situation, Problem, Implication, Need-Payoff) questions based on the lead profile and company summary.
    
    @param lead_name: The name of the lead.
    @param lead_profile: The profile of the lead.
    @param company_summary: The summary of the company.
    @return: The generated SPIN questions.
    """
    content = f"""
    Customer (Company) Information:
    {company_summary}

    Customer (Person):
    {lead_profile}

    Customer Name:
    {lead_name}
    """
    messages = [
        {"role": "system", "content": spin_questions_prompt},
        {"role": "user", "content": content}
    ]
    response = completion(
        model="groq/llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.1
    )
    response_message = response.choices[0].message.content
    return response_message

def generate_cold_call_script(lead_name, lead_profile, company_summary, spin_questions):
    """
    Generates a cold call script based on the lead profile, company summary, and SPIN questions.
    
    @param lead_name: The name of the lead.
    @param lead_profile: The profile of the lead.
    @param company_summary: The summary of the company.
    @param spin_questions: The SPIN questions to include in the script.
    @return: The generated cold call script.
    """
    content = f"""
    Customer (Company) Information:
    {company_summary}

    Customer (Person):
    {lead_profile}

    Customer Name:
    {lead_name}

    Spin questions:
    {spin_questions}
    """
    messages = [
        {"role": "system", "content": cold_script_writer_prompt},
        {"role": "user", "content": content}
    ]
    response = completion(
        model="groq/llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.1
    )
    response_message = response.choices[0].message.content
    return response_message
