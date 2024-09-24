from langgraph.graph import END, StateGraph
from typing import List, TypedDict
from pydantic import BaseModel
from colorama import Fore, Style
from .nodes import OutReachAutomationNodes


class LeadData(BaseModel):
    id: int
    name: str
    email: str
    profile: str
    score: int

class CompanyData(BaseModel):
    profile: str
    open_positions: str

class GraphState(TypedDict):
    leads: List[dict]
    lead_data: LeadData
    company_data: CompanyData
    cold_call_script: str
    personal_email: str
    num_leads: int


class OutReachAutomation:
    def __init__(self):
        # Build graph
        self.graph = self.build_graph()

    def build_graph(self):
        # Initializing StateGraph
        graph = StateGraph(GraphState)

        # Adding nodes to the graph
        graph.add_node("get_new_leads", OutReachAutomationNodes.get_new_leads)
        graph.add_node("check_for_remaining_leads", OutReachAutomationNodes.check_for_remaining_leads)
        graph.add_node("search_lead_data", OutReachAutomationNodes.search_lead_data)
        graph.add_node("score_lead", OutReachAutomationNodes.score_lead)
        graph.add_node("generate_outreach_materials", OutReachAutomationNodes.generate_outreach_materials)
        graph.add_node("generate_personal_email", OutReachAutomationNodes.generate_personal_email)
        graph.add_node("generate_cold_call_script", OutReachAutomationNodes.generate_cold_call_script)
        graph.add_node("update_CRM", OutReachAutomationNodes.update_CRM)
        graph.add_node("update_CRM_and_exit", OutReachAutomationNodes.update_CRM_and_exit)

        # edges setup
        graph.set_entry_point("get_new_leads")
        graph.add_edge("get_new_leads", "check_for_remaining_leads")
        graph.add_conditional_edges(
            "check_for_remaining_leads",
            OutReachAutomationNodes.check_if_there_more_leads,
            {
                "Found leads": "search_lead_data",
                "No more leads": END
            }
        )
        graph.add_edge("search_lead_data", "score_lead")
        graph.add_conditional_edges(
            "score_lead",
            OutReachAutomationNodes.check_if_qualified,
            {
                "qualified": "generate_outreach_materials",
                "not qualified": "update_CRM_and_exit"
            }
        )
        graph.add_edge("generate_outreach_materials", "generate_personal_email")
        graph.add_edge("generate_outreach_materials", "generate_cold_call_script")
        graph.add_edge("generate_cold_call_script", "update_CRM")
        graph.add_edge("generate_personal_email", "update_CRM")
        graph.add_edge("update_CRM", "check_for_remaining_leads")
        graph.add_edge("update_CRM_and_exit", "check_for_remaining_leads")

        return graph.compile()

    def invoke(self, inputs):
        print(Fore.GREEN + "----- Running outreach automation -----\n" + Style.RESET_ALL)
        return self.graph.invoke(inputs)
