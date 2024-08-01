import requests
import json
import re
import os
from litellm import completion
from bs4 import BeautifulSoup
from .prompts import (
    extract_customer_support_jobs_prompt,
    lead_score_prompt,
    spin_questions_prompt,
    personalize_email_prompt,
    cold_script_writer_prompt
)

def extract_company_name(email):
    """
    Extracts the company name from a professional email address.
    
    @param email: The email address to extract the company name from.
    @return: The extracted company name or "Company not found" if extraction fails.
    """
    try:
        # Split the email to get the domain part
        company_name = email.split('@')[1].split('.')[0]
        return company_name
    except IndexError:
        return "Company not found"

def google_search(query):
    """
    Performs a Google search using the provided query.
    
    @param query: The search query.
    @return: A list of search results.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json().get('organic', [])
    return results

def extract_linkedin_url(search_results, is_company):
    """
    Extracts the LinkedIn URL from the search results.
    
    @param search_results: The search results from which to extract the URL.
    @param is_company: Boolean indicating whether to extract a company URL or a person URL.
    @return: The extracted LinkedIn URL or an error message if not found.
    """
    try:
        for result in search_results:
            if is_company and 'linkedin.com/company' in result['link']:
                return result['link']
            elif not is_company and 'linkedin.com/in' in result['link']:
                return result['link']
        return "LinkedIn URL not found."
    except KeyError:
        return "Invalid search results format."

def scrape_linkedin(linkedin_url, is_company):
    """
    Scrapes LinkedIn profile data based on the provided LinkedIn URL.
    
    @param linkedin_url: The LinkedIn URL to scrape.
    @param is_company: Boolean indicating whether to scrape a company profile or a person profile.
    @return: The scraped LinkedIn profile data.
    """
    if is_company:
        url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-company-by-linkedinurl"
    else:
        url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile"

    querystring = {"linkedin_url": linkedin_url}
    headers = {
      "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
      "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")

def search_lead_company(company_name):
    """
    Searches for the company LinkedIn profile based on the company name.
    
    @param company_name: The name of the company to search for.
    @return: A dictionary containing the company profile data or an error message if not found.
    """
    # Find company LinkedIn URL by searching on Google 'LinkedIn {{company_name}}'
    query = f"LinkedIn {company_name}"
    search_results = google_search(query)
    company_linkedin_url = extract_linkedin_url(search_results, True)
    print(company_linkedin_url)

    if not company_linkedin_url:
        return "Company LinkedIn URL not found."

    # Scrape company LinkedIn page
    company_page_content = scrape_linkedin(company_linkedin_url, True)
    if "data" not in company_page_content:
        return "LinkedIn profile not found"
    
    company_profile = company_page_content["data"]
    return {
        "company_name": company_profile.get("company_name", ""),
        "company_description": company_profile.get("description", ""),
        "company_website": company_profile.get("website", ""),
        "company_location": company_profile.get("locations", []),
        "company_industry": company_profile.get("industries", []),
        "company_size": company_profile.get("employee_count", company_profile.get("employee_range", ""))
    }

def search_lead_profile(lead_name, company_name):
    """
    Searches for the lead's LinkedIn profile based on the lead name and company name.
    
    @param lead_name: The name of the lead to search for.
    @param company_name: The name of the company to associate with the lead.
    @return: A dictionary containing the lead profile data or an error message if not found.
    """
    # Find lead LinkedIn URL by searching on Google 'LinkedIn {{lead_name}} {{company_name}}'
    query = f"LinkedIn {lead_name} {company_name}"
    search_results = google_search(query)
    lead_linkedin_url = extract_linkedin_url(search_results, False)

    if not lead_linkedin_url:
        return "Lead LinkedIn URL not found."

    # Scrape lead LinkedIn profile
    lead_profile_content = scrape_linkedin(lead_linkedin_url, False)
    if "data" not in lead_profile_content:
        return "LinkedIn profile not found"
    
    lead_profile_content = lead_profile_content["data"]
    return {
        "about": lead_profile_content.get('about', ''),
        "skills": lead_profile_content.get('skills', []),
        "educations": [
            {
                "field_of_study": edu.get('field_of_study', ''),
                "date_range": edu.get('date_range', '')
            } for edu in lead_profile_content.get('educations', [])
        ],
        "experiences": [
            {
                "company": exp.get('company', ''),
                "title": exp.get('title', ''),
                "date_range": exp.get('date_range', ''),
                "is_current": exp.get('is_current', False),
                "location": exp.get('location', ''),
                "description": exp.get('description', '')
            } for exp in lead_profile_content.get('experiences', [])
        ]
    }

def scrape_website(url):
    """
    Scrapes text content from the provided website URL.
    
    @param url: The URL of the website to scrape.
    @return: The scraped text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text()

    # Normalize whitespaces and clean up text
    content = re.sub("\s+", " ", content).strip()

    return content

def fetch_company_jobs(company_url):
    """
    Fetches the open positions from the company's career page.
    
    @param company_url: The URL of the company's career page.
    @return: The extracted job positions from the career page.
    """
    content = scrape_website(company_url)
    messages = [
        {"role": "system", "content": extract_customer_support_jobs_prompt},
        {"role": "user", "content": content}
    ]
    response = completion(
        model="groq/llama3-70b-8192",
        messages=messages,
        temperature=0.1
    )
    response_message = response.choices[0].message.content
    return response_message

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
