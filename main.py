from dotenv import load_dotenv
from src.graph import OutReachAutomation

# Load environment variables from a .env file
load_dotenv()

if __name__ == "__main__":
    # Instantiate the OutReachAutomation class
    bot = OutReachAutomation()

    # Run the outreach automation with the provided lead name and email
    bot.run()
