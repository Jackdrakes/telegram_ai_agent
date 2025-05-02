import os

from dotenv import load_dotenv
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq

from textwrap import dedent
from pprint import pprint

load_dotenv()
# Load the Groq API key from an environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Initialize the Groq model with the API key
Groq.api_key = groq_api_key

agent = Agent(
    role="persona",
    description="you are a california conversationalist, message in a casual, relaxed, and modern american accent.",
    model=Groq(id="llama-3.1-8b-instant"),
    instructions=dedent("""
        Persona: office mail or text reply agent 
    """),
    monitoring=True,
    # markdown=True
)

# Define a function to run the agent
def run_agent(prompt):
    # Check if the prompt is a question
    is_question = prompt.strip().endswith('?')
    
    # Rewrite the message in the specified persona
    # rewritten_message = agent.run(f"write a text message, if it's a question , don't reply instead reframe or rephrase question into better way {prompt})").content

    rewritten_message = agent.run(f"""Rephrase the following as a casual, semi-formal text message. 
    If the input is a question, do not answer it. Instead, reframe or reword the question to make it clearer or more effective. Input: {prompt}""").content
    
    if is_question:
        # Generate a response in the specified persona
        # response = agent.run(f"Give positive and negative responses {prompt}").content
        
        response = agent.run(
            f"""
            You are a friendly assistant who writes casual,if the prompt is a question, then 
            give one positive and also one negative response {prompt}. Keep both responses polite, clear, and natural. 
            Format them as plain text messages.
            """
        ).content

        return f"** Message:** {rewritten_message}\n\n**Response:** {response}"
    else:
        return f"**Rewritten Message:** {rewritten_message}"
    
def handle_american_accent_command(user_message):    
        
    # Run the agent with the user's message
    response = agent.run(f"{user_message}")
        
    return response.content

def test_agent_response():
    
    # Test rewriting and responding to a question
    rewritten_response = run_agent("can we connect now?")
    print(rewritten_response)
    
if __name__ == "__main__":
    test_agent_response()
    print("All tests passed.")