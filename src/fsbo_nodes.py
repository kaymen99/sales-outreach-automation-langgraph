from colorama import Fore, Style
from .prompts_fsbo import (
    PROPERTY_ANALYSIS_PROMPT,
    SCORE_FSBO_LEAD_PROMPT,
    GENERATE_SELLER_OUTREACH_EMAIL_PROMPT,
    GENERATE_SELLER_INTERVIEW_SCRIPT_PROMPT,
)
from .state import FSBOLeadData, FSBOPropertyData, FSBOReport, FSBOGraphState
from .structured_outputs import FSBOSellerEmail
from .utils import invoke_llm, get_report, get_current_date, save_reports_locally
from .tools.fsbo_tools import search_fsbo_listings, get_fsbo_market_stats


class FSBOAutomationNodes:
    def __init__(self, location: str, max_leads: int = 10):
        self.location = location
        self.max_leads = max_leads
        self.reports_folder = "reports/fsbo"

    def discover_fsbo_listings(self, state: FSBOGraphState):
        print(Fore.YELLOW + "----- Discovering FSBO listings -----\n" + Style.RESET_ALL)
        listings = search_fsbo_listings(self.location, max_results=self.max_leads)
        leads = [
            FSBOLeadData(
                id=l.listing_url or l.address,
                address=l.address,
                price=l.price,
                bedrooms=l.bedrooms,
                bathrooms=l.bathrooms,
                sqft=l.sqft,
                lot_size=l.lot_size,
                days_on_market=l.days_on_market,
                seller_name=l.seller_name,
                seller_phone=l.seller_phone,
                seller_email=l.seller_email,
                description=l.description,
                listing_url=l.listing_url,
                property_type=l.property_type,
                year_built=l.year_built,
                source=l.source,
            )
            for l in listings
        ]
        print(Fore.YELLOW + f"----- Found {len(leads)} FSBO listings -----\n" + Style.RESET_ALL)
        return {
            "fsbo_leads": leads,
            "number_leads": len(leads),
            "location": self.location,
        }

    @staticmethod
    def check_for_remaining_leads(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Checking for remaining FSBO leads -----\n" + Style.RESET_ALL)
        current_lead = None
        if state["fsbo_leads"]:
            current_lead = state["fsbo_leads"].pop()
        return {"current_lead": current_lead}

    @staticmethod
    def check_if_more_leads(state: FSBOGraphState):
        num_leads = state["number_leads"]
        if num_leads > 0:
            print(Fore.YELLOW + f"----- Found {num_leads} more FSBO leads -----\n" + Style.RESET_ALL)
            return "Found leads"
        else:
            print(Fore.GREEN + "----- Finished, no more FSBO leads -----\n" + Style.RESET_ALL)
            return "No more leads"

    @staticmethod
    def analyze_property(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Analyzing FSBO property -----\n" + Style.RESET_ALL)
        lead = state["current_lead"]

        property_input = f"""
Address: {lead.address}
Price: ${lead.price:,}
Bedrooms: {lead.bedrooms}
Bathrooms: {lead.bathrooms}
Sqft: {lead.sqft}
Lot Size: {lead.lot_size}
Property Type: {lead.property_type}
Year Built: {lead.year_built}
Days on Market: {lead.days_on_market}
Description: {lead.description}
Source: {lead.source}
Seller: {lead.seller_name}
"""

        property_analysis = invoke_llm(
            system_prompt=PROPERTY_ANALYSIS_PROMPT,
            user_message=property_input,
            model="gemini-1.5-flash",
        )

        analysis_report = FSBOReport(
            title=f"Property Analysis — {lead.address}",
            content=property_analysis,
            is_markdown=True,
        )

        return {
            "property_analysis": property_analysis,
            "reports": [analysis_report],
        }

    @staticmethod
    def score_seller_lead(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Scoring FSBO seller lead -----\n" + Style.RESET_ALL)
        lead = state["current_lead"]
        analysis = state.get("property_analysis", "")

        scoring_input = f"""
Property: {lead.address}
Price: ${lead.price:,}
Bedrooms: {lead.bedrooms} | Bathrooms: {lead.bathrooms} | Sqft: {lead.sqft}
Days on Market: {lead.days_on_market}
Seller Contact: {lead.seller_name} | {lead.seller_email} | {lead.seller_phone}
Description: {lead.description}

Analysis Report:
{analysis}
"""

        score = invoke_llm(
            system_prompt=SCORE_FSBO_LEAD_PROMPT,
            user_message=scoring_input,
            model="gemini-1.5-pro",
        )

        try:
            score_val = float(score.strip())
        except (ValueError, AttributeError):
            score_val = 0.0

        print(Fore.CYAN + f"FSBO Lead Score: {score_val}/10\n" + Style.RESET_ALL)
        return {"lead_score": str(score_val)}

    @staticmethod
    def check_if_qualified(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Checking if FSBO seller is qualified -----\n" + Style.RESET_ALL)
        try:
            score = float(state["lead_score"])
        except (ValueError, TypeError):
            score = 0.0

        is_qualified = score >= 5.0
        if is_qualified:
            print(Fore.GREEN + "FSBO seller is qualified — proceeding with outreach\n" + Style.RESET_ALL)
            return "qualified"
        else:
            print(Fore.RED + "FSBO seller is not qualified — saving reports\n" + Style.RESET_ALL)
            return "not qualified"

    @staticmethod
    def generate_seller_outreach_email(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Generating outreach email for FSBO seller -----\n" + Style.RESET_ALL)
        lead = state["current_lead"]
        analysis = state.get("property_analysis", "")

        email_input = f"""
Seller Name: {lead.seller_name or "Homeowner"}
Property Address: {lead.address}
List Price: ${lead.price:,}
Bedrooms: {lead.bedrooms} | Bathrooms: {lead.bathrooms} | Sqft: {lead.sqft}
Days on Market: {lead.days_on_market}
Property Description: {lead.description}

Property Analysis:
{analysis}
"""

        output = invoke_llm(
            system_prompt=GENERATE_SELLER_OUTREACH_EMAIL_PROMPT,
            user_message=email_input,
            model="gemini-1.5-flash",
            response_format=FSBOSellerEmail,
        )

        subject = output.subject
        email_body = output.email

        email_report = FSBOReport(
            title=f"Outreach Email — {lead.address}",
            content=email_body,
            is_markdown=False,
        )

        return {
            "personalized_email": f"Subject: {subject}\n\n{email_body}",
            "reports": [email_report],
        }

    @staticmethod
    def generate_seller_interview_script(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Generating seller interview script -----\n" + Style.RESET_ALL)
        lead = state["current_lead"]
        analysis = state.get("property_analysis", "")

        script_input = f"""
Seller: {lead.seller_name or "Homeowner"}
Property: {lead.address}
Price: ${lead.price:,}
Days on Market: {lead.days_on_market}

Property Analysis:
{analysis}
"""

        interview_script = invoke_llm(
            system_prompt=GENERATE_SELLER_INTERVIEW_SCRIPT_PROMPT,
            user_message=script_input,
            model="gemini-1.5-flash",
        )

        script_report = FSBOReport(
            title=f"Interview Script — {lead.address}",
            content=interview_script,
            is_markdown=True,
        )

        return {
            "interview_script": interview_script,
            "reports": [script_report],
        }

    @staticmethod
    def save_reports(state: FSBOGraphState):
        print(Fore.YELLOW + "----- Saving FSBO lead reports -----\n" + Style.RESET_ALL)
        reports = state["reports"]
        folder = "reports/fsbo"
        import os
        if not os.path.exists(folder):
            os.makedirs(folder)
        for report in reports:
            file_path = os.path.join(folder, f"{report.title}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report.content)
        print(Fore.GREEN + f"Saved {len(reports)} reports to {folder}/\n" + Style.RESET_ALL)
        return {"reports": []}
