# Specialized Sales Agent classes

from services import generate_sales_response, get_sales_context
import logging

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def process(self, customer_message: str, context: str) -> str:
        response = generate_sales_response(self.role, customer_message, context)
        logger.info(f"{self.name} processed message")
        return response


class NewCustomerAgent(Agent):
    def __init__(self):
        super().__init__("NewCustomerAgent", "new_customer")


class UpgradeAgent(Agent):
    def __init__(self):
        super().__init__("UpgradeAgent", "upgrade")


class DeviceAgent(Agent):
    def __init__(self):
        super().__init__("DeviceAgent", "device_inquiry")


class PromotionAgent(Agent):
    def __init__(self):
        super().__init__("PromotionAgent", "promotion")


class GeneralSalesAgent(Agent):
    def __init__(self):
        super().__init__("GeneralSalesAgent", "other")


class SalesRouter:
    def __init__(self):
        self.agents = {
            "new_customer": NewCustomerAgent(),
            "upgrade": UpgradeAgent(),
            "device_inquiry": DeviceAgent(),
            "promotion": PromotionAgent(),
            "other": GeneralSalesAgent()
        }
        logger.info("SalesRouter initialized with all sub-agents")
    
    def route(self, intent: str, customer_message: str) -> tuple:
        agent = self.agents.get(intent, self.agents["other"])
        context = get_sales_context(customer_message)
        response = agent.process(customer_message, context)
        logger.info(f"Routed to {agent.name}")
        return agent.name, response
