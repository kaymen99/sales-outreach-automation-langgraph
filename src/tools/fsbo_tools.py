import os
import json
import requests
from typing import Optional
from src.utils import invoke_llm
from .base.search_tools import google_search
from .base.markdown_scraper_tool import scrape_website_to_markdown

FSBO_LISTING_EXTRACTION_PROMPT = """
You are a real estate data extraction specialist. Given the following web content from an FSBO (For Sale By Owner) or real estate listing page, extract all individual property listings.

For each property found, extract:
1. address: Full street address including city, state, ZIP
2. price: Listing price as a number (remove $ and commas)
3. bedrooms: Number of bedrooms
4. bathrooms: Number of bathrooms
5. sqft: Square footage
6. lot_size: Lot size in acres or sqft
7. days_on_market: How many days the property has been listed
8. seller_name: Name of the seller or listing agent (if visible — leave empty if not found)
9. seller_phone: Contact phone number for the seller
10. seller_email: Contact email for the seller
11. description: A short description of the property
12. listing_url: The URL of the individual listing
13. property_type: e.g. "Single Family", "Condo", "Townhouse", "Land"
14. year_built: Year the property was built
15. source: The website source (e.g. "Zillow", "Realtor.com", "FSBO.com")

Return ONLY a valid JSON array of objects. If no listings are found, return an empty array [].
Do NOT include any additional text, markdown formatting, or preamble.
"""


class FSBOSearchResult:
    def __init__(self, raw: dict):
        self.address = raw.get("address", "")
        self.price = raw.get("price", 0)
        self.bedrooms = raw.get("bedrooms", 0)
        self.bathrooms = raw.get("bathrooms", 0)
        self.sqft = raw.get("sqft", 0)
        self.lot_size = raw.get("lot_size", "")
        self.days_on_market = raw.get("days_on_market", 0)
        self.seller_name = raw.get("seller_name", "")
        self.seller_phone = raw.get("seller_phone", "")
        self.seller_email = raw.get("seller_email", "")
        self.description = raw.get("description", "")
        self.listing_url = raw.get("listing_url", "")
        self.property_type = raw.get("property_type", "")
        self.year_built = raw.get("year_built", 0)
        self.source = raw.get("source", "")

    def to_lead_record(self) -> dict:
        return {
            "id": self.listing_url or self.address,
            "First Name": self.seller_name.split()[0] if self.seller_name else "",
            "Last Name": " ".join(self.seller_name.split()[1:]) if self.seller_name and len(self.seller_name.split()) > 1 else self.seller_name,
            "Email": self.seller_email,
            "Phone": self.seller_phone,
            "Address": self.address,
            "Price": self.price,
            "Bedrooms": self.bedrooms,
            "Bathrooms": self.bathrooms,
            "Sqft": self.sqft,
            "Property Type": self.property_type,
            "Days on Market": self.days_on_market,
            "Description": self.description,
            "Listing URL": self.listing_url,
            "Source": self.source,
        }


def search_fsbo_listings(location: str, max_results: int = 10) -> list[FSBOSearchResult]:
    """
    Search for FSBO (For Sale By Owner) property listings in a given location.
    Uses Serper API to find listings, then extracts structured data via LLM.

    Args:
        location: City, state, or ZIP code to search in
        max_results: Maximum number of listings to return

    Returns:
        List of FSBOSearchResult objects
    """
    queries = [
        f"FSBO for sale by owner {location} real estate",
        f"for sale by owner {location} homes no agent",
        f"FSBO listings {location} by owner",
        f"homes for sale by owner {location} flat fee",
    ]

    all_listings = []

    for query in queries:
        if len(all_listings) >= max_results:
            break

        search_results = google_search(query)
        for result in search_results[:5]:
            url = result.get("link", "")
            snippet = result.get("snippet", "")
            title = result.get("title", "")

            if not url:
                continue

            try:
                page_content = scrape_website_to_markdown(url)
            except Exception:
                page_content = f"{title}\n\n{snippet}"

            combined_content = f"Source URL: {url}\n\nTitle: {title}\n\nSnippet: {snippet}\n\n{page_content[:8000]}"

            try:
                raw_output = invoke_llm(
                    system_prompt=FSBO_LISTING_EXTRACTION_PROMPT,
                    user_message=combined_content,
                    model="gemini-1.5-flash",
                )
                raw_output = raw_output.strip()
                if raw_output.startswith("```json"):
                    raw_output = raw_output[7:]
                if raw_output.startswith("```"):
                    raw_output = raw_output[3:]
                if raw_output.endswith("```"):
                    raw_output = raw_output[:-3]
                raw_output = raw_output.strip()

                parsed = json.loads(raw_output)
                if isinstance(parsed, list):
                    for item in parsed:
                        if item.get("address"):
                            item["source"] = item.get("source") or _detect_source(url)
                            fsbo = FSBOSearchResult(item)
                            if not any(
                                existing.address.lower() == fsbo.address.lower()
                                for existing in all_listings
                            ):
                                all_listings.append(fsbo)
            except (json.JSONDecodeError, Exception):
                continue

    return all_listings[:max_results]


def _detect_source(url: str) -> str:
    url_lower = url.lower()
    if "zillow" in url_lower:
        return "Zillow"
    elif "realtor" in url_lower:
        return "Realtor.com"
    elif "fsbo" in url_lower:
        return "FSBO.com"
    elif "redfin" in url_lower:
        return "Redfin"
    elif "trulia" in url_lower:
        return "Trulia"
    elif "forsalebyowner" in url_lower:
        return "ForSaleByOwner.com"
    return "Unknown"


def get_fsbo_market_stats(location: str) -> dict:
    """
    Get market statistics for FSBO listings in a location.
    """
    listings = search_fsbo_listings(location, max_results=25)

    if not listings:
        return {
            "location": location,
            "total_listings": 0,
            "avg_price": 0,
            "avg_bedrooms": 0,
            "avg_bathrooms": 0,
            "avg_sqft": 0,
            "avg_days_on_market": 0,
            "sources": {},
        }

    prices = [l.price for l in listings if l.price]
    bedrooms = [l.bedrooms for l in listings if l.bedrooms]
    bathrooms = [l.bathrooms for l in listings if l.bathrooms]
    sqfts = [l.sqft for l in listings if l.sqft]
    doms = [l.days_on_market for l in listings if l.days_on_market]

    sources = {}
    for l in listings:
        s = l.source or "Unknown"
        sources[s] = sources.get(s, 0) + 1

    return {
        "location": location,
        "total_listings": len(listings),
        "avg_price": round(sum(prices) / len(prices)) if prices else 0,
        "avg_bedrooms": round(sum(bedrooms) / len(bedrooms), 1) if bedrooms else 0,
        "avg_bathrooms": round(sum(bathrooms) / len(bathrooms), 1) if bathrooms else 0,
        "avg_sqft": round(sum(sqfts) / len(sqfts)) if sqfts else 0,
        "avg_days_on_market": round(sum(doms) / len(doms)) if doms else 0,
        "sources": sources,
    }
