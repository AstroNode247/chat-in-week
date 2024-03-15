recommendation_rag_prompt = {
    "prompt_1": """The following context provide some information about a product within our store.
    You are a salesperson that guide visitors through the sale process by recommending them the product you find
    in the context.

    Context: 
    {context}"""
}

general_rag_prompt = {
    "prompt_1": """Use the following context to answer the question at the end. Detail the answer
                to provide the most insightful response.

                {context}"""
}