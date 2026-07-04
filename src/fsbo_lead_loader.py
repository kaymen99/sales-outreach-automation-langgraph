from src.tools.leads_loader.lead_loader_base import LeadLoaderBase
from src.tools.fsbo_tools import search_fsbo_listings


class FSBOLeadLoader(LeadLoaderBase):
    """
    Lead loader that discovers FSBO (For Sale By Owner) property listings
    as leads. Extends LeadLoaderBase to integrate with the outreach automation
    workflow.
    """

    available_statuses = [
        "NEW",
        "UNQUALIFIED",
        "ATTEMPTED_TO_CONTACT",
        "CONTACTED_SELLER",
        "SELLER_INTERESTED",
        "SELLER_NOT_INTERESTED",
        "DEAL_CLOSED",
    ]

    def __init__(self, location: str, max_leads: int = 10):
        self.location = location
        self.max_leads = max_leads
        self._cached_records = []

    def fetch_records(self, status_filter="NEW"):
        """
        Fetch FSBO listings for the configured location.
        Ignores status_filter for discovery (all found listings are "NEW").
        """
        listings = search_fsbo_listings(self.location, max_results=self.max_leads)
        self._cached_records = [l.to_lead_record() for l in listings]
        return self._cached_records

    def update_record(self, lead_id, status):
        """
        Update a lead's status. For FSBO leads this is a no-op in-memory
        (no external CRM), but implements the interface contract.
        """
        for record in self._cached_records:
            if record["id"] == lead_id:
                return True
        return False
