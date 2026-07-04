from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from typing_extensions import TypedDict
from operator import add
    
class SocialMediaLinks(BaseModel):
    blog: str = ""
    facebook: str = ""
    twitter: str = ""
    youtube: str = ""
    
class Report(BaseModel):
    title: str = ""
    content: str = ""
    is_markdown: bool = False

class LeadData(BaseModel):
    id: str = Field(..., description="The unique identifier for the lead being processed")
    name: str = Field(..., description="The full name of the lead")
    address: str = Field(..., description="The address of the lead")
    email: str = Field(..., description="The email address of the lead")
    phone: str = Field(..., description="The phone number of the lead")
    profile: str = Field(..., description="The lead profile summary from LinkedIn data")

class CompanyData(BaseModel):
    name: str = ""
    profile: str = ""
    website: str = ""
    social_media_links: SocialMediaLinks = SocialMediaLinks()
    
class GraphInputState(TypedDict):
    leads_ids: List[str]

class GraphState(TypedDict):
    leads_ids: List[str]
    leads_data: List[dict]
    current_lead: LeadData
    lead_score: str = ""
    company_data: CompanyData
    reports: Annotated[list[Report], add]
    reports_folder_link: str
    custom_outreach_report_link: str
    personalized_email: str
    interview_script: str
    number_leads: int

# ─── FSBO / Real Estate Data Models ───────────────────────────────────────────

class FSBOLeadData(BaseModel):
    id: str = Field(default="")
    address: str = ""
    price: float = 0.0
    bedrooms: int = 0
    bathrooms: int = 0
    sqft: int = 0
    lot_size: str = ""
    days_on_market: int = 0
    seller_name: str = ""
    seller_phone: str = ""
    seller_email: str = ""
    description: str = ""
    listing_url: str = ""
    property_type: str = ""
    year_built: int = 0
    source: str = ""

class FSBOPropertyData(BaseModel):
    address: str = ""
    analysis: str = ""
    market_position: str = ""
    seller_motivation: str = ""
    outreach_approach: str = ""

class FSBOReport(BaseModel):
    title: str = ""
    content: str = ""
    is_markdown: bool = False

class FSBOGraphState(TypedDict):
    location: str
    fsbo_leads: List[FSBOLeadData]
    current_lead: Optional[FSBOLeadData]
    lead_score: str
    property_analysis: str
    personalized_email: str
    interview_script: str
    reports: Annotated[list[FSBOReport], add]
    number_leads: int