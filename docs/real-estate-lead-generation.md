# Real Estate Lead Generation (FSBO Mode)

This extension adds **FSBO (For Sale By Owner) real estate lead generation** to the sales outreach automation system. It discovers homeowners selling without a real estate agent, analyzes their motivation, and generates personalized outreach materials for real estate professionals.

## Architecture

The FSBO module follows the same LangGraph pattern as the core outreach automation:

```
discover_fsbo_listings
        │
        ▼
check_for_remaining_leads ────► END (no more leads)
        │
        ▼
  analyze_property
        │
        ▼
  score_seller_lead
        │
        ├── qualified ────► generate_seller_outreach_email
        │                          │
        │                          ▼
        │                   generate_seller_interview_script
        │                          │
        │                          ▼
        └── not qualified ────► save_reports ────► check_for_remaining_leads
```

## File Reference

| File | Purpose |
|------|---------|
| `src/fsbo_graph.py` | LangGraph workflow definition |
| `src/fsbo_nodes.py` | Processing nodes (discovery, analysis, scoring, outreach) |
| `src/prompts_fsbo.py` | LLM prompts for real estate analysis |
| `src/fsbo_lead_loader.py` | LeadLoader implementation for FSBO leads |
| `src/tools/fsbo_tools.py` | Web search & scraping for FSBO listings |
| `src/state.py` (extended) | FSBO data models (`FSBOLeadData`, `FSBOGraphState`, etc.) |
| `src/structured_outputs.py` (extended) | `FSBOSellerEmail` structured output model |

## How It Works

### 1. FSBO Discovery
Uses the Serper API (already in the project) to search multiple real estate sources for FSBO listings in a target location. The system searches across:
- Zillow FSBO listings
- Realtor.com for-sale-by-owner
- FSBO.com
- Redfin, Trulia, and other sources

### 2. Property Analysis
For each discovered listing, the LLM generates a detailed analysis:
- Property overview and market position
- Seller motivation assessment (based on days on market, price reductions, etc.)
- Outreach opportunity evaluation

### 3. Seller Scoring
Each FSBO seller is scored on a 0-10 scale based on:
- **Seller Contactability** (2x weight): Can we reach them?
- **Seller Motivation** (3x weight): How motivated are they to sell?
- **Property Value** (1x weight): Is it worth pursuing?
- **Market Opportunity** (2x weight): Can we add value?
- **Competition Risk** (1x weight): Are other agents chasing them?

Only sellers scoring 5.0+ proceed to outreach generation.

### 4. Outreach Generation
For qualified leads, the system generates:
- **Personalized email** to the FSBO seller
- **Interview/call script** for the agent to use when contacting the seller

## Usage

### Quick Start (Standalone)

```python
from src.fsbo_graph import run_fsbo_workflow

output = run_fsbo_workflow(
    location="Miami, FL",
    max_leads=10
)
print(output)
```

### Combined Workflow (main.py)

```python
from src.fsbo_lead_loader import FSBOLeadLoader

# Use FSBOLeadLoader as a lead source
lead_loader = FSBOLeadLoader(
    location="Austin, TX",
    max_leads=15
)

# Then use with OutReachAutomation (or standalone FSBOAutomation)
from src.fsbo_graph import FSBOAutomation
automation = FSBOAutomation(location="Austin, TX", max_leads=15)
app = automation.app
result = app.invoke({
    "fsbo_leads": [],
    "number_leads": 0,
    "location": "Austin, TX"
}, {"recursion_limit": 100})
```

### Command Line

```bash
# Run the FSBO workflow from the command line
python -c "
from src.fsbo_graph import run_fsbo_workflow
result = run_fsbo_workflow('Miami, FL', 5)
for lead in result.get('fsbo_leads', []):
    print(f\"  {lead.address} — \${lead.price:,.0f} — Score: {result.get('lead_score', 'N/A')}\")
"
```

### Market Statistics

```python
from src.tools.fsbo_tools import get_fsbo_market_stats

stats = get_fsbo_market_stats("Denver, CO")
print(f"Total FSBO listings: {stats['total_listings']}")
print(f"Average price: \${stats['avg_price']:,}")
print(f"Average days on market: {stats['avg_days_on_market']}")
```

## Example Output

After processing, reports are saved to `reports/fsbo/`:

```
reports/fsbo/
├── Property Analysis — 123 Main St, Austin, TX.txt
├── Property Analysis — 456 Oak Ave, Austin, TX.txt
├── Outreach Email — 123 Main St, Austin, TX.txt
├── Outreach Email — 456 Oak Ave, Austin, TX.txt
├── Interview Script — 123 Main St, Austin, TX.txt
└── Interview Script — 456 Oak Ave, Austin, TX.txt
```

## Customization

### Adding Real Estate Sources
Edit `src/tools/fsbo_tools.py` queries list in `search_fsbo_listings()` to target specific sites or regions.

### Adjusting Scoring Weights
Modify `SCORE_FSBO_LEAD_PROMPT` in `src/prompts_fsbo.py` to change scoring criteria weights.

### Customizing Outreach Templates
Edit prompts in `src/prompts_fsbo.py` to match your agency's voice and value proposition.

## Dependencies
All dependencies are already in `requirements.txt`:
- `langgraph` — Workflow orchestration
- `langchain-*` — LLM interaction
- `requests` — HTTP calls for Serper API
- `beautifulsoup4` / `unstructured` — Web scraping

No additional packages required.
