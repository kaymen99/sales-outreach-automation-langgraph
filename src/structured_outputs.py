from pydantic import BaseModel, Field


class WebsiteData(BaseModel):
    summary: str = Field(description="Summary of the company website content.")
    blog_url: str = Field(description="The main blog URL of the company.")
    youtube: str = Field(description="The company's YouTube profile link.")
    twitter: str = Field(description="The company's Twitter profile link.")
    facebook: str = Field(description="The company's Facebook profile link.")

class EmailResponse(BaseModel):
    subject: str = Field(description="An engaging subject line to encourage the lead to open the email.")
    email: str = Field(description="The personalized email content tailored to the lead's profile and company information.")

class FSBOSellerEmail(BaseModel):
    subject: str = Field(description="Personalized subject line referencing the seller's property.")
    email: str = Field(description="The personalized outreach email for the FSBO seller.")
