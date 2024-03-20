import requests
from langchain_core.tools import BaseTool


class OrderTool(BaseTool):
    name = "Get Order"
    description = """Useful for when you need to get a specific order. Provide all the detail possible to answer to 
    user question."""

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
    You should ask nicely for Order ID."""

    def _run(self):
        pass

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")