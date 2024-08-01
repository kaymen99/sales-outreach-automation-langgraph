import json
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import List
from colorama import Fore, Style, init
from .utils import (
    search_lead_company,
    search_lead_profile,
    extract_company_name,
    fetch_company_jobs,
    score_lead,
    generate_spin_questions,
    generate_cold_call_script,
    personnalize_email
)


### global graph state
class GraphState(TypedDict):
    lead_name: str
    lead_email: str
    lead_profile: str
    lead_score: int
    company_summary: str
    company_open_positions: str
    cold_call_script: str
    personal_email: str
    is_qualified: bool
from langgraph.graph import END, StateGraph
from colorama import Fore, Style

class OutReachAutomation:
    def __init__(self):
        # Build graph
        self.graph = self.build_graph()

    def search_lead_data(self, state):
        """
        Search for lead data based on the lead name.

        @param state: The current state of the application.
        @return: Updated state with lead data.
        """
        print(Fore.YELLOW + "----- Searching for lead data -----\n" + Style.RESET_ALL)
        lead_name = state["lead_name"]
        lead_email = state["lead_email"]
        # Extracting company name from email
        company_name = extract_company_name(lead_email)
        # Searching for company profile
        company_profile = search_lead_company(company_name)
        # Searching for lead profile
        lead_profile = search_lead_profile(lead_name, company_name)
        # Fetching company jobs
        if "company_website" in company_profile:
            company_website = company_profile["company_website"] + "/careers"
            company_open_positions = fetch_company_jobs(company_website)
        return {
            **state,
            "company_summary": company_profile,
            "lead_profile": lead_profile,
            "company_open_positions": company_open_positions
        }

    def score_lead(self, state):
        """
        Score the lead based on the company profile and open positions.

        @param state: The current state of the application.
        @return: Updated state with the lead score.
        """
        print(Fore.YELLOW + "----- Scoring lead -----\n" + Style.RESET_ALL)
        # Scoring lead
        lead_score = score_lead(state["company_summary"], state["company_open_positions"])
        return {**state, "lead_score": lead_score}

    def is_lead_qualified(self, state):
        """
        Check if the lead is qualified based on the lead score.

        @param state: The current state of the application.
        @return: Updated state with the qualification status.
        """
        print(Fore.YELLOW + "----- Checking if lead is qualified -----\n" + Style.RESET_ALL)
        return state

    def check_if_qualified(self, state):
        """
        Check if the lead is qualified based on the lead score.

        @param state: The current state of the application.
        @return: Updated state with the qualification status.
        """
        # Checking if the lead score is 50 or higher
        is_qualified = int(state["lead_score"]) >= 50
        if is_qualified:
            print(Fore.GREEN + "Lead is qualified\n" + Style.RESET_ALL)
            return "qualified"
        else:
            print(Fore.RED + "Lead is not qualified\n" + Style.RESET_ALL)
            return "not qualified"

    def generate_personal_email(self, state):
        """
        Generate a personalized email for the lead.

        @param state: The current state of the application.
        @return: Updated state with the generated email.
        """
        print(Fore.YELLOW + "----- Generating personalized email -----\n" + Style.RESET_ALL)
        # Personalizing email
        personal_email = personnalize_email(state["company_summary"], state["lead_profile"])
        return {**state, "personal_email": personal_email}

    def generate_cold_call_script(self, state):
        """
        Generate a cold call script for the lead.

        @param state: The current state of the application.
        @return: Updated state with the generated cold call script.
        """
        print(Fore.YELLOW + "----- Generating cold call script -----\n" + Style.RESET_ALL)
        lead_name = state["lead_name"]
        # Generating SPIN questions
        spin_questions = generate_spin_questions(lead_name, state["lead_profile"], state["company_summary"])
        # Generating cold call script
        cold_call_script = generate_cold_call_script(lead_name, state["lead_profile"], state["company_summary"], spin_questions)
        return {
            **state,
            "cold_call_script": cold_call_script
        }

    def send_email(self, state):
        """
        Send an email to the lead.

        @param state: The current state of the application.
        @return: Updated state after sending the email.
        """
        print(Fore.YELLOW + "----- Sending email -----\n" + Style.RESET_ALL)
        # Writing email and call script to output file
        with open("output.txt", "a") as file:
            file.write("Email:\n\n")
            file.write(state["personal_email"] + f'\n{"-"*70}\n')
            file.write("Call Script:\n\n")
            file.write(state["cold_call_script"] + f'\n{"-"*70}\n')
        return state

    def update_CRM(self, state):
        """
        Update CRM records for the lead.

        @param state: The current state of the application.
        @return: The updated state after updating CRM records.
        """
        print(Fore.YELLOW + "----- Updating CRM records -----\n" + Style.RESET_ALL)
        return state

    def update_CRM_and_exit(self, state):
        """
        Update CRM records for the lead and exit the workflow.

        @param state: The current state of the application.
        @return: The updated state after updating CRM records.
        """
        print(Fore.YELLOW + "----- Lead not qualified, updating CRM records and Stopping -----\n" + Style.RESET_ALL)
        return state

    def build_graph(self):
        # Initializing StateGraph
        graph = StateGraph(GraphState)

        # Adding nodes to the graph
        graph.add_node("search_lead_data", self.search_lead_data)
        graph.add_node("score_lead", self.score_lead)
        graph.add_node("is_lead_qualified", self.is_lead_qualified)
        graph.add_node("generate_personal_email", self.generate_personal_email)
        graph.add_node("generate_cold_call_script", self.generate_cold_call_script)
        graph.add_node("send_email", self.send_email)
        graph.add_node("update_CRM", self.update_CRM)
        graph.add_node("update_CRM_and_exit", self.update_CRM_and_exit)

        # Setting the entry point of the graph
        graph.set_entry_point("search_lead_data")
        # Adding edges between nodes
        graph.add_edge("search_lead_data", "score_lead")
        graph.add_edge("score_lead", "is_lead_qualified")
        graph.add_conditional_edges(
            "is_lead_qualified",
            self.check_if_qualified,
            {
                "qualified": "generate_personal_email",
                "not qualified": "update_CRM_and_exit"
            }
        )
        graph.add_edge("generate_personal_email", "generate_cold_call_script")
        graph.add_edge("generate_cold_call_script", "update_CRM")
        graph.add_edge("update_CRM", "send_email")
        graph.add_edge("send_email", END)
        graph.add_edge("update_CRM_and_exit", END)

        # Compiling the graph
        return graph.compile()

    def run(self, lead_name, lead_email):
        print(Fore.GREEN + "----- Running outreach automation -----\n" + Style.RESET_ALL)
        # Invoking the graph with the initial state
        return self.graph.invoke({"lead_name": lead_name, "lead_email": lead_email})
