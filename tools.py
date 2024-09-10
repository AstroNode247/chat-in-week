import requests
from langchain_core.tools import BaseTool


class OrderTool(BaseTool):
    name = "Get Order ID"
    description = """Useful for when you need to get a specific order. 
    If there is a mistake on the order status in other words if it's returned to seller or lost or something else
    you have to propose a solution. 
    If encounter an error in requesting the orderID, tell that you are unable to find the order id."""

    def _run(self, id: str):
        try:
            # Send the GET request and store the response
            response = requests.get(f"http://localhost:8000/orders/{id}")

            # Check for successful response (status code 200)
            if response.status_code == 200:
                # Get the response content
                data = response.json()  # Assuming the response is JSON format
                if data is None:
                    raise ValueError("No data available")
                return data
            else:
                print(f"Error: {response.status_code}")  # Print error message with status code
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")


class OrderIdIncompleteTool(BaseTool):
    name = "Ask Order ID"
    description = """Useful for when you want to solve a specific problem about an order.
    Present yourself first and tell that you are there to help him/her, be empathic."""

    def _run(self):
        pass

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
    

class RecommendTools(BaseTool):
    name = "Recommend stuff"
    description = """Use this tool to recommend new products to user, only if you know the user ID.
    It uses the recommendation already done by the json response. You don't have do any recommenndation,
    you all have to do is to use show the JSON. Add some description to your recommendation"""

    def _run(self, user_id: str):
        try:
            # Send the GET request and store the response
            response = requests.get(f"http://localhost:8000/content_retail?user_id={user_id}")

            # Check for successful response (status code 200)
            if response.status_code == 200:
                # Get the response content
                data = response.json()  # Assuming the response is JSON format
                if data is None:
                    raise ValueError("No data available")
                return data
            else:
                print(f"Error: {response.status_code}")  # Print error message with status code
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
