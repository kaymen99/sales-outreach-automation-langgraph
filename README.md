# AI-sales-outreach

I developed an AI-powered lead outreach automation system that integrates with HubSpot and LinkedIn to streamline lead research and outreach. This project includes automated lead research, lead scoring, identification of company pain points, and personalized communication via email, video, and call scripts.

- **Integrate with HubSpot to add and analyze new leads.**
- **Research leads on LinkedIn and score them based on specified business rules.**
- **Identify key pain points and generate personalized outreach materials.**
- **Create customized emails, videos, and call scripts to engage leads effectively.**

## Key Features and Design Choices

### **AI-Powered Lead Analysis**

- **Lead and Company Research**: Scrape LinkedIn for lead and company information, and gather current open positions by scraping the company's website for deeper insights into their needs.
- **Automated Lead Scoring**: Assess and rank leads based on predefined criteria to prioritize high-value prospects.
- **Personalized Outreach**: Generate tailored emails, videos, and call scripts to engage leads with relevant solutions and content.
- **Pain Point Identification**: Detect company challenges that align with your services for more impactful communication.

### **Integration with APIs**

- **LinkedIn Data**: Scrape profile information using the RapidAPI LinkedIn Profile Data API. [Get your API key here](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-profile-data).
- **Google Searches**: Perform web searches with the Serper API. [Get your API key here](https://serper.dev).
- **Content Generation**: Use Groq for LLAMA3.1 and LLAMA3 models. [Get your API key here](https://groq.com).

## Future Development

- **HubSpot Integration**: The current version does not yet connect with HubSpot. Future updates will include integration with HubSpot for enhanced lead management.
- **Enhanced Personalization**: Improve the system by expanding the dataset of personalized outreach materials and implementing a continuous feedback loop to refine content generation.

## How to Run

### Prerequisites

- Python 3.9+
- API keys for RapidAPI (LinkedIn), Serper, and Groq
- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen99/AI-sales-outreach.git
   cd AI-sales-outreach
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add your API keys:

   ```env
   RAPIDAPI_KEY=your_rapidapi_key
   SERPER_API_KEY=your_serper_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

### Running the Application

1. **Start the automation:** Add the lead name and email and then run:

   ```sh
   python main.py
   ```

   The application will start analyzing leads, scoring them, and generating personalized outreach materials.

### Customization

* To customize the scoring rules or outreach templates, edit the relevant configuration file in `src/prompts`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

### Contact

For questions or suggestions, contact me at `aymenMir10001@gmail.com`.