# Multi-agent system: Agent classes and routing

from services import generate_response, get_context_from_perplexity
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def process(self, customer_message: str, context: str) -> str:
        response = generate_response(self.role, customer_message, context)
        logger.info(f"{self.name} processed message")
        return response


class BillingAgent(Agent):
    def __init__(self):
        super().__init__("BillingAgent", "billing")


class SalesAgent(Agent):
    def __init__(self):
        super().__init__("SalesAgent", "sales")


class TechSupportAgent(Agent):
    def __init__(self):
        super().__init__("TechSupportAgent", "technical_support")


class GeneralAgent(Agent):
    def __init__(self):
        super().__init__("GeneralAgent", "other")


class AgentRouter:
    def __init__(self):
        self.agents = {
            "billing": BillingAgent(),
            "sales": SalesAgent(),
            "technical_support": TechSupportAgent(),
            "other": GeneralAgent()
        }
        logger.info("AgentRouter initialized with all agents")
    
    def route(self, intent: str, customer_message: str) -> tuple:
        agent = self.agents.get(intent, self.agents["other"])
        context = get_context_from_perplexity(customer_message)
        response = agent.process(customer_message, context)
        logger.info(f"Routed to {agent.name}")
        return agent.name, response
