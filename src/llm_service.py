"""
LLM service module for nutritional analysis chat.

This module provides an interface to the Groq LLM API for generating
AI-powered responses to nutritional queries. The LLM is configured as
a nutritional analysis expert.

Classes:
    LLMService: Manages LLM API interactions for nutritional insights
"""

import os
from groq import Groq

class LLMService:
    """
    Manages interactions with Groq LLM API for nutritional analysis.
    
    Configures the LLM with a system prompt for nutritional expertise and
    provides methods for generating data-driven responses to user queries.
    
    Attributes:
        client (Groq): Initialized Groq API client
        model (str): Model identifier for LLM completions
    """
    
    def __init__(self):
        """
        Initialize LLM service with Groq API.
        
        Loads API key from environment variables and initializes the Groq client
        with the llama-3.3-70b-versatile model.
        
        Raises:
            ValueError: If GROQ_API_KEY is not found in environment variables
        """

        # load the api key from .env file
        api_key=os.environ.get("GROQ_API_KEY")
        if not api_key: 
            raise ValueError("Groq API key not found in .end file")
        
        # initialize the groq client and model
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"


    def generate_response(self, prompt, context):
        """
        Generate LLM response to a nutritional query.
        
        Sends the user's question along with dataset context to the LLM and
        retrieves an AI-generated response focused on nutritional analysis.
        
        Args:
            prompt (str): User's question or query
            context (str): Dataset information to provide to the LLM.
                Typically includes string representations of DataFrames.
                
        Returns:
            str: LLM-generated response with nutritional insights
            
        Note:
            The LLM is configured with a system prompt that defines it as a
            nutritional analysis expert focused on providing clear, data-driven
            insights about Starbucks menu items.
        """
        
        # create the system prompt to define the AI's role
        system_prompt = """You are a nutritional analysis expert that provides clear, data-driven insights about Starbucks's food and drink items. 

Guidelines:
- Analyze the provided dataset to answer user questions about nutritional content
- Provide specific statistics and comparisons when available
- Use simple language that general users can understand
- If the data doesn't contain the requested information, politely inform the user
- Keep responses concise and focused on the user's question
- When comparing items or categories, highlight key differences clearly """

        # phrase the full message for the AI to generate response based on it
        if context: 
            full_message = f"""Based on the provided data: {context}, answer the following question: {prompt}"""
        else:
            full_message = context

        # generate the response from the ai
        # with the stated roles and content
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_message}
            ]
        )

        return response.choices[0].message.content