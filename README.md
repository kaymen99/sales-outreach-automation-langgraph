# AI-Sales-Outreach-Langgraph

I developed an AI-powered lead outreach automation system using Langgraph that integrates with HubSpot and LinkedIn to streamline lead research and outreach. This project includes monitoring Hubspot contacts list, automated lead research, lead scoring, identification of company pain points, and personalized communication via email, video, and call scripts.

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

[![](https://mermaid.ink/img/pako:eNqtlW1v2jAQx7-K5ap7FaqEtBnNpE0t0L3ZWFe2N1umyIoPsGrizHYElPLdd3kgQFa6amqQUO7-9u_OZ_uyponiQEM61SybkW-DKCX4nJ6SvpJKG_KGjO1KgkFXJSWSGTOACTGWaRtDyslESBmeDIPi5xir1T2EJ77v1--dheB2FnrZ0kkKaKVNVGo7RjxA2HWz5bsWPNMqAWNq9HWv7w37r4TmkAgjVFqzby6uuheDV2Kr3Ga5rcmX3evg2vt_crMVN1ItmvpPwcYpLGIJjJufEf0IloxgQT4VdkR_kU7nPUlmkNzHE6VjDXMmUpFOqwnriPYLjaBG7rZaNflDRDdVjHpVxyBFiMcblePWl_YjMcB0MivVmDPLMK9x6SrJZIAuTO0l2JEic6VhCx6OBsgaYqTb6kQ0mOq_HbhcvUmQUPqKPAqjTKM9tRlVBv6aMykmAvgjljgFzSzEuJ0aGPLnaGnBZFXwSiVfapV83qpNhBZ7pCz5vePnGS_o_bvPMUt5DEthkfu99BL0EvSSIXpbGT-TV7nuRs9AG5UyGRcFlvs539YKGRZKw38xGc8rjxMmZWwSLTK7z8aOwUkfNTIutWPZH2ZX8ncVOSjE3_m147dm78fbeZ-_Eu3RzZ78a1pzP6-yTK6e7JOHt9XB07xrm_u943gYZ3eUnF2OzlPpbhvbAbh9QZwj2-AcLbHz3OGo-zSGpA6dg0YUx6_JukghonYGc4hoiK-c6fuIRukGx7HcqvEqTWhodQ4O1Sqfzmg4QSBa1dIGguEnad54M5b-UOrApuGaLil2y95ZcBG43V5wHriXl0HPoSsadtwzFx_PPw88L3jr-57ru763cehDyfE2fwBG62D1?type=png)](https://mermaid.live/edit#pako:eNqtlW1v2jAQx7-K5ap7FaqEtBnNpE0t0L3ZWFe2N1umyIoPsGrizHYElPLdd3kgQFa6amqQUO7-9u_OZ_uyponiQEM61SybkW-DKCX4nJ6SvpJKG_KGjO1KgkFXJSWSGTOACTGWaRtDyslESBmeDIPi5xir1T2EJ77v1--dheB2FnrZ0kkKaKVNVGo7RjxA2HWz5bsWPNMqAWNq9HWv7w37r4TmkAgjVFqzby6uuheDV2Kr3Ga5rcmX3evg2vt_crMVN1ItmvpPwcYpLGIJjJufEf0IloxgQT4VdkR_kU7nPUlmkNzHE6VjDXMmUpFOqwnriPYLjaBG7rZaNflDRDdVjHpVxyBFiMcblePWl_YjMcB0MivVmDPLMK9x6SrJZIAuTO0l2JEic6VhCx6OBsgaYqTb6kQ0mOq_HbhcvUmQUPqKPAqjTKM9tRlVBv6aMykmAvgjljgFzSzEuJ0aGPLnaGnBZFXwSiVfapV83qpNhBZ7pCz5vePnGS_o_bvPMUt5DEthkfu99BL0EvSSIXpbGT-TV7nuRs9AG5UyGRcFlvs539YKGRZKw38xGc8rjxMmZWwSLTK7z8aOwUkfNTIutWPZH2ZX8ncVOSjE3_m147dm78fbeZ-_Eu3RzZ78a1pzP6-yTK6e7JOHt9XB07xrm_u943gYZ3eUnF2OzlPpbhvbAbh9QZwj2-AcLbHz3OGo-zSGpA6dg0YUx6_JukghonYGc4hoiK-c6fuIRukGx7HcqvEqTWhodQ4O1Sqfzmg4QSBa1dIGguEnad54M5b-UOrApuGaLil2y95ZcBG43V5wHriXl0HPoSsadtwzFx_PPw88L3jr-57ru763cehDyfE2fwBG62D1)

### **Integration with APIs**

- **HubSpot CRM**: To integrate with your HubSpot contacts CRM, you must [sign up](https://www.hubspot.com/) for a HubSpot account, then create a private app and get your API key. [Follow this quick tutorial](https://www.youtube.com/watch?v=hSipSbiwc2s).
- **LinkedIn Data**: Scrape profile information using the RapidAPI LinkedIn Profile Data API. [Get your API key here](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-profile-data).
- **Google Searches**: Perform web searches with the Serper API. [Get your API key here](https://serper.dev).
- **Content Generation**: Use Groq for LLAMA3.1 and LLAMA3 models. [Get your API key here](https://groq.com).

## Future Development

- **Enhanced Personalization**: Improve the system by expanding the dataset of personalized outreach materials and implementing a continuous feedback loop to refine content generation.

## Tech Stack

- **[Langgraph](https://langchain-ai.github.io/langgraph/)**: Utilized for building the AI automation workflow.
- **[Litellm](https://www.litellm.ai/)**: Used for connecting and leveraging multiple large language models (LLMs) such as GPT-4, LLAMA3, LLAMA3.1,...
- **HubSpot Python API**: Implemented for interacting with the HubSpot private app.

## How to Run

### Prerequisites

- Python 3.9+
- API keys for RapidAPI (LinkedIn [see](https://rapidapi.com/freshdata-freshdata-default/api/fresh-linkedin-profile-data)), Serper, HubSpot (private app), and Groq
- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen99/sales-outreach-automation-langgraph.git
   cd sales-outreach-automation-langgraph
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