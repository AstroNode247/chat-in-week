import requests
from langchain_core.tools import BaseTool


class OrderTool(BaseTool):
    name = "Get Order"
    description = """Useful for when you need to get a specific order. But the order 
    is not specified ask to the user what is the order ID. If the user does not provide order ID, ask for it.
    If there is a mistake on the order status in other words if it's returned to seller or lost or something else
    you have to propose a solution"""

    def _run(self, id: str):
        try:
            # Send the GET request and store the response
            response = requests.get(f"http://localhost:8000/orders/{id}")

            # Check for successful response (status code 200)
            if response.status_code == 200:
                # Get the response content
                data = response.json()  # Assuming the response is JSON format
                print(data)  # Print the data
            else:
                print(f"Error: {response.status_code}")  # Print error message with status code
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")


class OrderIdIncompleteTool(BaseTool):
    name = "Ask Order ID"
    description = """Useful for when you need to get a specific order where the order ID is not provided.
    Present yourself first and tell that you are there to help him/her, be empathic. Then ask if her/his order
    number is available."""

    def _run(self):
        pass

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
