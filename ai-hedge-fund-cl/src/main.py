import json

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from colorama import init

from src.agents.portfolio_manager import portfolio_management_agent
from src.agents.risk_manager import risk_management_agent
from src.graph.state import AgentState
from src.utils.display import print_trading_output
from src.utils.analysts import get_analyst_nodes
from src.utils.progress import progress
from src.cli.input import parse_cli_inputs

# Load environment variables from .env file
load_dotenv()
init(autoreset=True)


def parse_hedge_fund_response(response):
    """Parses a JSON string and returns a dictionary."""
    try:
        return json.loads(response)
    except (json.JSONDecodeError, TypeError, Exception) as e:
        print(f"Error parsing response: {e}\nResponse: {repr(response)}")
        return None


def run_hedge_fund(
    tickers: list[str],
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
    model_name: str = "gpt-4o",
    model_provider: str = "OpenAI",
):
    progress.start()
    try:
        workflow = create_workflow()
        agent = workflow.compile()

        final_state = agent.invoke(
            {
                "messages": [HumanMessage(content="Make trading decisions based on the provided data.")],
                "data": {
                    "tickers": tickers,
                    "portfolio": portfolio,
                    "start_date": start_date,
                    "end_date": end_date,
                    "analyst_signals": {},
                },
                "metadata": {
                    "show_reasoning": show_reasoning,
                    "model_name": model_name,
                    "model_provider": model_provider,
                },
            },
        )

        return {
            "decisions": parse_hedge_fund_response(final_state["messages"][-1].content),
            "analyst_signals": final_state["data"]["analyst_signals"],
        }
    finally:
        progress.stop()


def start(state: AgentState):
    """Initialize the workflow."""
    return state


def create_workflow():
    """Build the agent workflow: Warren Buffett + Peter Lynch -> Risk Manager -> Portfolio Manager."""
    workflow = StateGraph(AgentState)
    workflow.add_node("start_node", start)

    # Add the two analyst agents
    analyst_nodes = get_analyst_nodes()
    for analyst_key, (node_name, node_func) in analyst_nodes.items():
        workflow.add_node(node_name, node_func)
        workflow.add_edge("start_node", node_name)

    # Risk management and portfolio manager
    workflow.add_node("risk_management_agent", risk_management_agent)
    workflow.add_node("portfolio_manager", portfolio_management_agent)

    # Both analysts feed into risk management
    for analyst_key, (node_name, _) in analyst_nodes.items():
        workflow.add_edge(node_name, "risk_management_agent")

    workflow.add_edge("risk_management_agent", "portfolio_manager")
    workflow.add_edge("portfolio_manager", END)

    workflow.set_entry_point("start_node")
    return workflow


if __name__ == "__main__":
    inputs = parse_cli_inputs(
        description="AI Hedge Fund — Warren Buffett + Peter Lynch agents",
        require_tickers=True,
        default_months_back=None,
        include_reasoning_flag=True,
    )

    portfolio = {
        "cash": inputs.initial_cash,
        "margin_requirement": inputs.margin_requirement,
        "margin_used": 0.0,
        "positions": {
            ticker: {
                "long": 0,
                "short": 0,
                "long_cost_basis": 0.0,
                "short_cost_basis": 0.0,
                "short_margin_used": 0.0,
            }
            for ticker in inputs.tickers
        },
        "realized_gains": {
            ticker: {"long": 0.0, "short": 0.0}
            for ticker in inputs.tickers
        },
    }

    result = run_hedge_fund(
        tickers=inputs.tickers,
        start_date=inputs.start_date,
        end_date=inputs.end_date,
        portfolio=portfolio,
        show_reasoning=inputs.show_reasoning,
        model_name=inputs.model_name,
        model_provider=inputs.model_provider,
    )
    print_trading_output(result)
