from langchain_core.tools import tool
from tools import *
from config import GROQ_API_KEY
from test_location import *
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Calls Groq LLM with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """

    system_prompt = """
    You are Dr. Emily Hartman, a warm and experienced clinical psychologist.

    Respond to patients with:
    - Emotional attunement ("I can sense how difficult this must be...")
    - Gentle normalization ("Many people feel this way when...")
    - Practical guidance ("What sometimes helps is...")
    - Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open-ended questions
    """

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key = GROQ_API_KEY,
        temperature=0.7
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)
    return response.content


@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()


@tool
def find_nearby_therapists_by_locations(location: str) -> str:
    """
    Finds real therapists near the specified location using Geoapify
    
    Args:
        location (str): The city or area to search.
    
    Returns:
        str: A list of therapist names, addresses, and phone numbers.
    """
    return find_nearby_therapists_by_location(location)


## Step1: Create an AI Agent & link it to the backend

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY

tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_locations]
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, api_key=GROQ_API_KEY)
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_locations`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response


