import requests
import json
import re
import os
from litellm import completion
from bs4 import BeautifulSoup
from src.prompts import extract_customer_support_jobs_prompt

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

# def search_lead_company(company_name):
#     """
#     Searches for the company LinkedIn profile based on the company name.
    
#     @param company_name: The name of the company to search for.
#     @return: A dictionary containing the company profile data or an error message if not found.
#     """
#     # Find company LinkedIn URL by searching on Google 'LinkedIn {{company_name}}'
#     query = f"LinkedIn {company_name}"
#     search_results = google_search(query)
#     company_linkedin_url = extract_linkedin_url(search_results, True)
#     print(company_linkedin_url)

#     if not company_linkedin_url:
#         return "Company LinkedIn URL not found."

#     # Scrape company LinkedIn page
#     company_page_content = scrape_linkedin(company_linkedin_url, True)
#     if "data" not in company_page_content:
#         return "LinkedIn profile not found"
    
#     company_profile = company_page_content["data"]
#     return {
#         "company_name": company_profile.get("company_name", ""),
#         "company_description": company_profile.get("description", ""),
#         "company_website": company_profile.get("website", ""),
#         "company_location": company_profile.get("locations", []),
#         "company_industry": company_profile.get("industries", []),
#         "company_size": company_profile.get("employee_count", company_profile.get("employee_range", ""))
#     }

# def search_lead_profile(lead_name, company_name):
#     """
#     Searches for the lead's LinkedIn profile based on the lead name and company name.
    
#     @param lead_name: The name of the lead to search for.
#     @param company_name: The name of the company to associate with the lead.
#     @return: A dictionary containing the lead profile data or an error message if not found.
#     """
#     # Find lead LinkedIn URL by searching on Google 'LinkedIn {{lead_name}} {{company_name}}'
#     query = f"LinkedIn {lead_name} {company_name}"
#     search_results = google_search(query)
#     lead_linkedin_url = extract_linkedin_url(search_results, False)

#     if not lead_linkedin_url:
#         return "Lead LinkedIn URL not found."

#     # Scrape lead LinkedIn profile
#     lead_profile_content = scrape_linkedin(lead_linkedin_url, False)
#     if "data" not in lead_profile_content:
#         return "LinkedIn profile not found"
    
#     lead_profile_content = lead_profile_content["data"]
#     return {
#         "about": lead_profile_content.get('about', ''),
#         "skills": lead_profile_content.get('skills', []),
#         "educations": [
#             {
#                 "field_of_study": edu.get('field_of_study', ''),
#                 "date_range": edu.get('date_range', '')
#             } for edu in lead_profile_content.get('educations', [])
#         ],
#         "experiences": [
#             {
#                 "company": exp.get('company', ''),
#                 "title": exp.get('title', ''),
#                 "date_range": exp.get('date_range', ''),
#                 "is_current": exp.get('is_current', False),
#                 "location": exp.get('location', ''),
#                 "description": exp.get('description', '')
#             } for exp in lead_profile_content.get('experiences', [])
#         ]
#     }

# create mock functions for testing
def search_lead_company(company_name):
    return {'company_name': 'Mountain Goat Software',
            'company_description': 'Led by CST, author and Scrum practitioner Mike Cohn, Mountain Goat Software helps companies adopt and improve their use of agile processes and techniques in order to build high-performance development organizations. \n\nMountain Goat Software provides live online training courses all over\nthe world. Live online courses include Certified ScrumMaster (CSM)\ntraining and Certified Scrum Product Owner (CSPO) training. We also\noffer on demand video courses such as Agile Estimating and Planning,\nScrum Repair Guide, Better User Stories and Estimating with Story\nPoints. In addition to our training offerings we provide mentoring to\ncompanies to help you Succeed with Agile.\n',
            'company_website': 'http://www.mountaingoatsoftware.com',
            'company_location': [{'city': 'Broomfield',
              'country': 'US',
              'full_address': '1140 US Highway 287, Broomfield, CO 80020, US',
              'is_headquarter': True,
              'line1': '1140 US Highway 287',
              'line2': '',
              'region': 'CO',
              'zipcode': '80020'}],
            'company_industry': ['Software Development'],
            'company_size': 21
            }

def search_lead_profile(lead_name, company_name):
    return {'about': 'Please FOLLOW rather than connect unless we really know each other. If we know each other, say how. \n\nI CANNOT RESPOND to individual questions about agile as I simply get too many here to meet my other commitments. Besides, I\'ve probably already answered it in a book, video course, or on my blog at www.mountaingoatsoftware.com/blog. \n\nAs an in-demand agile and Scrum instructor, I train groups all over the world on how to adopt and succeed with agile software development using the Scrum framework. \n\nAs an author, I\'ve written three popular books on Scrum and agile: "Succeeding with Agile," "Agile Estimating and Planning" and "User Stories Applied for Agile Software Development."\n\nI\'m co-founder and past chairperson of the non-profit Agile Alliance, and also co-founded and served on the board of directors of the non-profit Scrum Alliance.\n\nI started running projects with Scrum in 1995, working in domains from banking to aerospace to video game development, with companies ranging in size from 1 to 400,000.  \n\nI served as VP of development at four different companies where agile was instrumental to the their success. Three of those companies were startups, and the other was a Fortune 40 company. \n\nMy hands-on experience means my Scrum and agile training and coaching is relevant to the real business world and not just theory.\n\nIf you link to me just to sell me something, I will block you. \n',
            'skills': [],
            'educations': [{'field_of_study': 'Economics', 'date_range': '1984 - 1986'}],
            'experiences': [{'company': 'Mountain Goat Software',
              'title': 'Owner',
              'date_range': 'Jan 2000 - present',
              'is_current': True,
              'location': '',
              'description': "As the founder of Mountain Goat Software, an agile and Scrum training company, I lead all public Scrum and agile training in person. I'm a Certified Scrum Trainer (CST), author of three popular books on agile and Scrum, an agile practitioner and consultant."},
              {'company': 'ePlan Services',
              'title': 'Vice President, Software Development',
              'date_range': '2003 - 2004',
              'is_current': False,
              'location': 'Denver',
              'description': 'I was the vice president of software development at ePlan Services and over the course of a year introduced the organization to Scrum.'},
              {'company': 'Genomica',
              'title': 'VP, Software Development',
              'date_range': 'Sep 2000 - Dec 2001',
              'is_current': False,
              'location': '',
              'description': ''},
              {'company': 'Access Health',
              'title': 'VP Software Development',
              'date_range': '1994 - 1998',
              'is_current': False,
              'location': '',
              'description': ''},
              {'company': 'Telephone Response Technologies Inc',
              'title': 'Software Team Leader',
              'date_range': '1990 - 1994',
              'is_current': False,
              'location': '',
              'description': ''}]
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
