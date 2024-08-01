from dotenv import load_dotenv
from src.graph import OutReachAutomation

# Load environment variables from a .env file
load_dotenv()

if __name__ == "__main__":
    # Define the lead's name and email address
    lead_name = ""
    lead_email = ""

    # Instantiate the OutReachAutomation class
    bot = OutReachAutomation()

    # Run the outreach automation with the provided lead name and email
    bot.run(lead_name, lead_email)
