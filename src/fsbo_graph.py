from langgraph.graph import END, StateGraph
from .fsbo_nodes import FSBOAutomationNodes
from .state import FSBOGraphState


class FSBOAutomation:
    """
    LangGraph workflow for FSBO (For Sale By Owner) real estate lead generation.
    Discovers FSBO property listings, analyzes seller motivation, scores leads,
    and generates personalized outreach materials for real estate agents.
    """

    def __init__(self, location: str, max_leads: int = 10):
        self.app = self.build_graph(location, max_leads)

    def build_graph(self, location: str, max_leads: int):
        graph = StateGraph(FSBOGraphState)
        nodes = FSBOAutomationNodes(location, max_leads)

        # Discovery phase
        graph.add_node("discover_fsbo_listings", nodes.discover_fsbo_listings)
        graph.add_node("check_for_remaining_leads", nodes.check_for_remaining_leads)

        # Analysis phase
        graph.add_node("analyze_property", nodes.analyze_property)
        graph.add_node("score_seller_lead", nodes.score_seller_lead)

        # Outreach phase
        graph.add_node("generate_seller_outreach_email", nodes.generate_seller_outreach_email)
        graph.add_node("generate_seller_interview_script", nodes.generate_seller_interview_script)

        # Save phase
        graph.add_node("save_reports", nodes.save_reports)

        # Entry point
        graph.set_entry_point("discover_fsbo_listings")

        # Discovery → check for leads
        graph.add_edge("discover_fsbo_listings", "check_for_remaining_leads")

        # Conditional: more leads or done?
        graph.add_conditional_edges(
            "check_for_remaining_leads",
            nodes.check_if_more_leads,
            {
                "Found leads": "analyze_property",
                "No more leads": END,
            },
        )

        # Analysis pipeline
        graph.add_edge("analyze_property", "score_seller_lead")

        # Qualification gate
        graph.add_conditional_edges(
            "score_seller_lead",
            nodes.check_if_qualified,
            {
                "qualified": "generate_seller_outreach_email",
                "not qualified": "save_reports",
            },
        )

        # Outreach materials (parallel)
        graph.add_edge("generate_seller_outreach_email", "generate_seller_interview_script")

        # Save and loop back
        graph.add_edge("generate_seller_interview_script", "save_reports")
        graph.add_edge("save_reports", "check_for_remaining_leads")

        return graph.compile()


def run_fsbo_workflow(location: str, max_leads: int = 10) -> dict:
    """
    Convenience function to run the FSBO lead generation workflow.

    Args:
        location: City, state, or ZIP to search for FSBO listings
        max_leads: Maximum number of FSBO leads to process

    Returns:
        Final graph state dictionary
    """
    automation = FSBOAutomation(location=location, max_leads=max_leads)
    app = automation.app
    inputs = {"fsbo_leads": [], "number_leads": 0}
    config = {"recursion_limit": 100}
    output = app.invoke(inputs, config)
    return output
