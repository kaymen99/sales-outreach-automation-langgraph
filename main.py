from dotenv import load_dotenv
from src.graph import OutReachAutomation, LeadData, CompanyData

# Load environment variables from a .env file
load_dotenv()

if __name__ == "__main__":
    # Instantiate the OutReachAutomation class
    bot = OutReachAutomation()
    
    # initial graph inputs
    inputs = {
        "leads": [],
        "lead_data": LeadData(id=0, name="", email="", profile="", score=0),
        "company_data": CompanyData(profile="", open_positions=""),
        "cold_call_script": "",
        "personal_email": "",
        "num_leads": 0
    } 

    # Run the outreach automation with the provided lead name and email
    bot.invoke(inputs)
