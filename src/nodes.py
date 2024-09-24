from colorama import Fore, Style
from .tools.lead_search import search_lead_profile, search_lead_company, extract_company_name, fetch_company_jobs
from .tools.lead_scoring import score_lead
from .tools.personalized_email import personalize_email
from .tools.call_script_generation import generate_spin_questions, generate_cold_call_script
from .tools.hubspot import get_new_leads, update_lead_status


class OutReachAutomationNodes:
    @staticmethod
    def get_new_leads(state):
        """
        Fetch new leads and initialize the leads list in the state.

        @param state: The current state of the application.
        @return: Updated state with leads list.
        """
        print(Fore.YELLOW + "----- Fetching new leads -----\n" + Style.RESET_ALL)
        
        # Fetch new leads from our Hubspot CRM
        leads = get_new_leads()
        
        print(Fore.YELLOW + f"----- Fetched {len(leads)} leads -----\n" + Style.RESET_ALL)
        return {"leads": leads, "num_leads": len(leads)}
    
    @staticmethod
    def check_for_remaining_leads(state):
        """
        Check if there are remaining leads in the list.

        @param state: The current state of the application.
        @return: The next node based on whether there are remaining leads.
        """
        print(Fore.YELLOW + "----- Checking for remaining leads -----\n" + Style.RESET_ALL)
        leads = state["leads"]
        lead_data = state["lead_data"]
        if len(leads) > 0:
            lead_data.id = leads[-1]["lead_id"]
            lead_data.name = leads[-1]["lead_name"]
            lead_data.email = leads[-1]["lead_email"]
            lead_data.profile = ""
            lead_data.score = 0
            # Remove lead being processed
            leads.pop()
        return {"lead_data": lead_data}

    @staticmethod
    def check_if_there_more_leads(state):
        """
        Check if there are more leads in the list.

        @param state: The current state of the application.
        @return: The next node based on whether there are more leads.
        """
        num_leads = state["num_leads"]
        if num_leads > 0:
            print(Fore.YELLOW + f"----- Found {num_leads} more leads -----\n" + Style.RESET_ALL)
            return "Found leads"
        else:
            print(Fore.GREEN + "----- Finished, No more leads -----\n" + Style.RESET_ALL)
            return "No more leads"

    @staticmethod
    def search_lead_data(state):
        """
        Search for lead data based on the lead name.

        @param state: The current state of the application.
        @return: Updated state with lead data.
        """
        print(Fore.YELLOW + "----- Searching for lead data -----\n" + Style.RESET_ALL)
        lead_data = state["lead_data"]
        company_data = state["company_data"]

        # extract company name from pro email
        company_name = extract_company_name(lead_data.email)
        
        # scrape lead linkedin profile
        lead_profile = search_lead_profile(lead_data.name, company_name)
        lead_data.profile = lead_profile

        # scrape lead's company linkedin & website
        company_profile = search_lead_company(company_name)
        company_data.profile = str(company_profile)
        
        # Fetching company jobs
        if "company_website" in company_profile:
            company_website = company_profile["company_website"] + "/careers"
            company_open_positions = fetch_company_jobs(company_website)
            company_data.open_positions = company_open_positions
        return {
            "lead_data": lead_data,
            "company_data": company_data
        }

    @staticmethod
    def score_lead(state):
        """
        Score the lead based on the company profile and open positions.

        @param state: The current state of the application.
        @return: Updated state with the lead score.
        """
        print(Fore.YELLOW + "----- Scoring lead -----\n" + Style.RESET_ALL)
        # Scoring lead
        company_data = state["company_data"]
        lead_score = score_lead(company_data.profile, company_data.open_positions)
        lead_data = state["lead_data"]
        lead_data.score = lead_score
        return {"lead_data": lead_data}

    @staticmethod
    def is_lead_qualified(state):
        """
        Check if the lead is qualified based on the lead score.

        @param state: The current state of the application.
        @return: Updated state with the qualification status.
        """
        print(Fore.YELLOW + "----- Checking if lead is qualified -----\n" + Style.RESET_ALL)
        return state

    @staticmethod
    def check_if_qualified(state):
        """
        Check if the lead is qualified based on the lead score.

        @param state: The current state of the application.
        @return: Updated state with the qualification status.
        """
        # Checking if the lead score is 50 or higher
        is_qualified = int(state["lead_data"].score) > 50
        if is_qualified:
            print(Fore.GREEN + "Lead is qualified\n" + Style.RESET_ALL)
            return "qualified"
        else:
            print(Fore.RED + "Lead is not qualified\n" + Style.RESET_ALL)
            return "not qualified"
    
    @staticmethod
    def generate_outreach_materials(state):
        return state

    @staticmethod
    def generate_personal_email(state):
        """
        Generate a personalized email for the lead.

        @param state: The current state of the application.
        @return: Updated state with the generated email.
        """
        print(Fore.YELLOW + "----- Generating personalized email -----\n" + Style.RESET_ALL)
        lead_data = state["lead_data"]
        company_data = state["company_data"]
        personal_email = personalize_email(company_data.profile, lead_data.profile)

        # save email to file or as draft
        with open("output.txt", "a") as file:
            file.write("Email:\n\n")
            file.write(personal_email + f'\n{"-"*70}\n')
        return {"personal_email": personal_email}

    @staticmethod
    def generate_cold_call_script(state):
        """
        Generate a cold call script for the lead.

        @param state: The current state of the application.
        @return: Updated state with the generated cold call script.
        """
        print(Fore.YELLOW + "----- Generating cold call script -----\n" + Style.RESET_ALL)
        lead_data = state["lead_data"]
        company_data = state["company_data"]
        
        # Generating SPIN questions
        spin_questions = generate_spin_questions(lead_data.name, lead_data.profile, company_data.profile)
        
        # Generating cold call script
        cold_call_script = generate_cold_call_script(lead_data.name, lead_data.profile, company_data.profile, spin_questions)

        # save script to file
        with open("output.txt", "a") as file:
            file.write("Call Script:\n\n")
            file.write(cold_call_script + f'\n{"-"*70}\n')
        return {"cold_call_script": cold_call_script}

    @staticmethod
    def update_CRM(state):
        """
        Update CRM records for the lead.

        @param state: The current state of the application.
        @return: The updated state after updating CRM records.
        """
        print(Fore.YELLOW + "----- Updating CRM records -----\n" + Style.RESET_ALL)
        # Set lead to attempt contact in Hubspot contacts CRM
        update_lead_status(state["lead_id"], "ATTEMPTED_TO_CONTACT")
        return {"num_leads": state["num_leads"] - 1}

    @staticmethod
    def update_CRM_and_exit(state):
        """
        Update CRM records for the lead and exit the workflow.

        @param state: The current state of the application.
        @return: The updated state after updating CRM records.
        """
        print(Fore.YELLOW + "----- Lead not qualified, updating CRM records and Stopping -----\n" + Style.RESET_ALL)
        # Set lead to unqualified in Hubspot contacts CRM
        update_lead_status(state["lead_id"], "UNQUALIFIED")
        return {"num_leads": state["num_leads"] - 1}