<!--
Title: AI-Sales-Outreach: AI HubSpot Lead Outreach Automation System
Description: Discover our AI-powered lead outreach automation system that integrates with HubSpot and LinkedIn to streamline lead research, scoring, and personalized emailing and call script generation.
Keywords: AI sales outreach, lead automation, HubSpot integration, LinkedIn lead research, personalized outreach, lead scoring, AI agents, AI tools
Author: kaymen99
-->

<meta name="title" content="AI-Sales-Outreach: AI HubSpot Lead Outreach Automation System">
<meta name="description" content="Discover our AI-powered lead outreach automation system that integrates with HubSpot and LinkedIn to streamline lead research, scoring, and personalized emailing and call script generation.">
<meta name="keywords" content="AI sales outreach, lead automation, HubSpot integration, LinkedIn lead research, personalized outreach, lead scoring, AI agents, AI tools">
<meta name="author" content="kaymen99">
<meta property="og:title" content="AI-Sales-Outreach: AI HubSpot Lead Outreach Automation System">
<meta property="og:description" content="Streamline your lead outreach with our AI-powered system, integrating with HubSpot and LinkedIn for effective lead research, scoring, and personalized emailing and call script generation.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://github.com/kaymen99/AI-sales-outreach">
    
# AI-Sales-Outreach

I developed an AI-powered lead outreach automation system that integrates with HubSpot and LinkedIn to streamline lead research and outreach. This project includes monitoring Hubspot contacts list, automated lead research, lead scoring, identification of company pain points, and personalized communication via email, video, and call scripts.

- **Integrate with HubSpot CRM to fetch new leads and record contacts updates.**
- **Research leads on LinkedIn and score them based on specified business rules.**
- **Identify key pain points and generate personalized outreach materials.**
- **Create customized emails, videos, and call scripts to engage leads effectively.**

## Key Features

### **AI-Powered Lead Analysis**

- **Monitor HubSpot CRM**: Continuously fetch new leads added into your contacts list.
- **Lead and Company Research**: Scrape LinkedIn for lead and company information, and gather current open positions by scraping the company's website for deeper insights into their needs.
- **Pain Point Identification**: Detect company challenges that align with provided services for more impactful communication.
- **Automated Lead Scoring**: Assess and rank leads based on predefined criteria to prioritize high-value prospects.
- **Categorize Leads**: Categorize leads into qualified or not qualified based on the lead score, and update HubSpot CRM accordingly.
- **Personalized Outreach**: Generate tailored emails, videos, and call scripts to engage qualified leads with relevant solutions and content.

### **System Flowchart**

This is the detailed flow of the system:

[![](https://mermaid.ink/img/pako:eNqFU8tuwjAQ_JWVz_ADHHoJ9CG1qIX21FSWay8kIrGD7YhWwL937ZAEWig5xTM7s7PrZMukUchGbGlFlcHrONVAzxI917jhBQrl3lN2hx6muIHHcIaFNSXc15-uMj5lHzAc3oDMUK74wlhusRS5zvWyUyeBA-Jg1nKNE4lT3XS8qA_uu1tTawXxvAOHwsosslwJL6jDPELRFMYERePrtlMDpbHYGk-m4zbO7x5xRiepOGKhZTjEjl2zno_luWv061oU-SLHoHpwTciXFjtawZ_6mLGr3NGtaLTCI6_QOqNFwcNMRbyfhoHnAwOTwHTJzltPjYd1b19XKpgnsycutOL4lXuyfosoEAqEwoTQo8wXIsX5O06aQnEpioI7afPKHwdOiIOEOJhHrot8UR29-6wnETt1zzc3h2Ggw7LmGOY42U_P__8xt2OfWdU1IRuwEi2Biv62bbBJmc-wxJSN6FUJu0pZqvdUJ2pv5t9aspG3NQ6YNfUyaw9N63Eu6I8t2WghCof7H6waUo0?type=png)](https://mermaid.live/edit#pako:eNqFU8tuwjAQ_JWVz_ADHHoJ9CG1qIX21FSWay8kIrGD7YhWwL937ZAEWig5xTM7s7PrZMukUchGbGlFlcHrONVAzxI917jhBQrl3lN2hx6muIHHcIaFNSXc15-uMj5lHzAc3oDMUK74wlhusRS5zvWyUyeBA-Jg1nKNE4lT3XS8qA_uu1tTawXxvAOHwsosslwJL6jDPELRFMYERePrtlMDpbHYGk-m4zbO7x5xRiepOGKhZTjEjl2zno_luWv061oU-SLHoHpwTciXFjtawZ_6mLGr3NGtaLTCI6_QOqNFwcNMRbyfhoHnAwOTwHTJzltPjYd1b19XKpgnsycutOL4lXuyfosoEAqEwoTQo8wXIsX5O06aQnEpioI7afPKHwdOiIOEOJhHrot8UR29-6wnETt1zzc3h2Ggw7LmGOY42U_P__8xt2OfWdU1IRuwEi2Biv62bbBJmc-wxJSN6FUJu0pZqvdUJ2pv5t9aspG3NQ6YNfUyaw9N63Eu6I8t2WghCof7H6waUo0)

### **Integration with APIs**

- **HubSpot CRM**: To integrate with your HubSpot contacts CRM, you must [sign up](https://www.hubspot.com/) for a HubSpot account, then create a private app and get your API key. [Follow this quick tutorial](https://www.youtube.com/watch?v=hSipSbiwc2s).
- **LinkedIn Data**: Scrape profile information using the RapidAPI LinkedIn Profile Data API. [Get your API key here](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-profile-data).
- **Google Searches**: Perform web searches with the Serper API. [Get your API key here](https://serper.dev).
- **Content Generation**: Use Groq for LLAMA3.1 and LLAMA3 models. [Get your API key here](https://groq.com).

## Future Development

- **Enhanced Personalization**: Improve the system by expanding the dataset of personalized outreach materials and implementing a continuous feedback loop to refine content generation.

## Tech Stack

- **Langgraph**: Utilized for building the AI automation system workflow.
- **Litellm**: Used for connecting and leveraging multiple large language models (LLMs) such as GPT-4, LLAMA3, LLAMA3.1,...
- **HubSpot Python API**: Implemented for interacting with the HubSpot private app.

## How to Run

### Prerequisites

- Python 3.9+
- API keys for RapidAPI (LinkedIn), Serper, HubSpot (private app), and Groq
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
   HUBSPOT_API_KEY=your_hubspot_api_key
   ```

### Running the Application

1. **Start the automation:**

   ```sh
   python main.py
   ```

   The application will connect with your HubSpot CRM to fetch all the new leads, analyze, research, and score them, and generate personalized outreach materials for the qualified leads.

### Customization

To customize the scoring rules or outreach templates, edit the relevant configuration file in `src/prompts`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

### Contact

For questions or suggestions, contact me at `aymenMir1001@gmail.com`.