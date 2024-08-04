from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import List
from colorama import Fore, Style
from .nodes import OutReachAutomationNodes


### global graph state
class GraphState(TypedDict):
    leads: List[dict]
    num_leads: int
    lead_id: str
    lead_name: str
    lead_email: str
    lead_profile: str
    lead_score: int
    company_summary: str
    company_open_positions: str
    cold_call_script: str
    personal_email: str
    is_qualified: bool


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
        graph.add_node("is_lead_qualified", OutReachAutomationNodes.is_lead_qualified)
        graph.add_node("generate_personal_email", OutReachAutomationNodes.generate_personal_email)
        graph.add_node("generate_cold_call_script", OutReachAutomationNodes.generate_cold_call_script)
        graph.add_node("send_email", OutReachAutomationNodes.send_email)
        graph.add_node("update_CRM", OutReachAutomationNodes.update_CRM)
        graph.add_node("update_CRM_and_exit", OutReachAutomationNodes.update_CRM_and_exit)

        # Setting the entry point of the graph
        graph.set_entry_point("get_new_leads")
        
        # Adding edges between nodes
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
        graph.add_edge("score_lead", "is_lead_qualified")
        graph.add_conditional_edges(
            "is_lead_qualified",
            OutReachAutomationNodes.check_if_qualified,
            {
                "qualified": "generate_personal_email",
                "not qualified": "update_CRM_and_exit"
            }
        )
        graph.add_edge("generate_personal_email", "generate_cold_call_script")
        graph.add_edge("generate_cold_call_script", "update_CRM")
        graph.add_edge("update_CRM", "send_email")
        graph.add_edge("send_email", "check_for_remaining_leads")
        graph.add_edge("update_CRM_and_exit", "check_for_remaining_leads")

        return graph.compile()

    def run(self):
        print(Fore.GREEN + "----- Running outreach automation -----\n" + Style.RESET_ALL)
        return self.graph.invoke({'leads': []})
