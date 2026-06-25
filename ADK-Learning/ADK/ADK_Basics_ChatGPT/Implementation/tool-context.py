'''
import os
import asyncio
from typing import Optional, Any, Dict
from dotenv import load_dotenv

# Import ADK modules
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.tools.tool_context import ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types

# ---------------------------------------------------------------------
# SETUP & CONFIGURATION
# ---------------------------------------------------------------------
# Load environment variables from .env file (for GEMINI_API_KEY/GOOGLE_API_KEY)
load_dotenv()

APP_NAME = "ResumeBuilderApp"
USER_ID = "swapnil_student"
SESSION_ID = "session_tool_context_demo"

# Initialize in-memory session and artifact services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# ---------------------------------------------------------------------
# CALLBACKS FOR VISIBILITY
# ---------------------------------------------------------------------
def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Runs before any model call to let us inspect the final instructions/prompts sent to Gemini."""
    print("\n" + "=" * 60)
    print(f"🤖 [Callback] Agent '{callback_context.agent_name}' is calling Gemini...")
    
    # Extract and format the system instructions showing the variable substitutions
    config = getattr(llm_request, 'config', None)
    system_instruction = getattr(config, 'system_instruction', None)
    inst_text = ""
    if isinstance(system_instruction, str):
        inst_text = system_instruction
    elif hasattr(system_instruction, 'parts') and system_instruction.parts:
        inst_text = "".join(p.text for p in system_instruction.parts if hasattr(p, 'text') and p.text)
    
    print("-" * 60)
    print("📋 [Instructions Sent to Model]:")
    print(inst_text.strip())
    print("-" * 60)
    
    return None

# ---------------------------------------------------------------------
# TOOL DEFINITIONS (State & Artifact Modification via ToolContext)
# ---------------------------------------------------------------------
def remember_name(name: str, tool_context: ToolContext) -> dict:
    """Saves the user's name to the session state. Call this tool when the user introduces themselves or shares their name.

    Args:
        name: The name of the user.
    """
    print(f"\n⚙️ [Tool: remember_name] Updating state: name = {name!r}")
    tool_context.state["name"] = name
    return {"status": "success", "message": f"Successfully remembered name: {name}"}


def remember_experience(years: int, tool_context: ToolContext) -> dict:
    """Saves the user's years of experience to the session state. Call this tool when the user shares their years of experience.

    Args:
        years: The number of years of professional experience.
    """
    print(f"\n⚙️ [Tool: remember_experience] Updating state: experience = {years}")
    tool_context.state["experience"] = years
    return {"status": "success", "message": f"Successfully remembered experience: {years} years"}


async def generate_resume_artifact(content: str, tool_context: ToolContext) -> dict:
    """Generates and saves the resume content as a Markdown document named 'resume.md'.
    Call this tool when you have collected the user's details and are ready to create their resume.

    Args:
        content: The complete markdown content of the resume.
    """
    print(f"\n⚙️ [Tool: generate_resume_artifact] Saving resume.md as an artifact...")
    # Wrap content in a types.Part as required by save_artifact
    part = types.Part(text=content)
    version = await tool_context.save_artifact("resume.md", part)
    return {"status": "success", "message": f"Saved resume.md version {version} as an artifact"}


async def read_resume_artifact(tool_context: ToolContext) -> dict:
    """Loads the user's saved resume artifact ('resume.md') so you can read it.
    Call this tool when you need to read the resume to generate a cover letter or view details.
    """
    print(f"\n⚙️ [Tool: read_resume_artifact] Loading resume.md from artifacts...")
    part = await tool_context.load_artifact("resume.md")
    if part and part.text:
        return {"status": "success", "content": part.text}
    return {"status": "error", "message": "No resume artifact found. Please generate one first."}

# ---------------------------------------------------------------------
# AGENT DEFINITIONS
# ---------------------------------------------------------------------
# Specialist Agent 1: Resume Agent
resume_agent = Agent(
    name="resume_agent",
    model="gemini-2.0-flash",
    description="Specialist for collecting details and generating resume markdown artifacts.",
    instruction="""
    You are a professional Resume Specialist.
    Your goals:
    - Welcome the user.
    - If you do not know the user's name, ask for it and call the `remember_name` tool.
    - If you do not know the user's years of experience, ask for it and call the `remember_experience` tool.
    - Note: You can check if they are already in the session state. If they are, they will be substituted below:
      Current User Name: {name}
      Current Experience: {experience}
    - Once you have both the name and experience, write a professional resume and call the `generate_resume_artifact` tool to save it. Tell the user you saved it!
    """,
    tools=[remember_name, remember_experience, generate_resume_artifact],
    before_model_callback=before_model_callback,
)

# Specialist Agent 2: Cover Letter Agent
cover_letter_agent = Agent(
    name="cover_letter_agent",
    model="gemini-2.0-flash",
    description="Specialist for reading resumes and writing custom cover letters.",
    instruction="""
    You are a professional Cover Letter Specialist.
    Your goals:
    - Write a tailored cover letter for the user.
    - You MUST load the user's resume first by calling the `read_resume_artifact` tool.
    - If the tool returns an error saying no resume is found, explain to the user that they must create their resume with the resume specialist first.
    - Once the resume is successfully read, use its details to write a highly professional, customized cover letter.
    """,
    tools=[read_resume_artifact],
    before_model_callback=before_model_callback,
)

# Manager/Root Agent: Coordinates routing
root_agent = Agent(
    name="career_assistant_manager",
    model="gemini-2.0-flash",
    description="Manager agent coordinating resume building and cover letter generation.",
    instruction="""
    You are a career assistant manager.
    Route the user's request to the correct specialist:
    - If the user wants to build/create/update their resume or tells you about their name/experience, route them to the `resume_agent`.
    - If the user wants to write a cover letter, route them to the `cover_letter_agent`.
    """,
    sub_agents=[resume_agent, cover_letter_agent],
    tools=[AgentTool(resume_agent), AgentTool(cover_letter_agent)],
    before_model_callback=before_model_callback,
)

# ---------------------------------------------------------------------
# INTERACTIVE RUNNER LOOP
# ---------------------------------------------------------------------
async def main():
    print("🚀 Initializing Session...")
    # Create the session with an empty initial state
    session = await session_service.create_session(
        session_id=SESSION_ID,
        user_id=USER_ID,
        app_name=APP_NAME,
        state={}
    )
    
    # Initialize the Runner with the root agent and services
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        artifact_service=artifact_service,
        app_name=APP_NAME
    )
    
    print("\n✨ Career Assistant is ready!")
    print("Type your message to chat, or type 'exit' / 'quit' to end.")
    print("Example messages to try:")
    print("  1. 'Hi, my name is Swapnil'"
          "\n  2. 'I have 7 years of experience'"
          "\n  3. 'Can you build my resume?'"
          "\n  4. 'Now write a cover letter for me'")
    
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            
            # Format the user message as a types.Content object
            new_message = types.Content(
                role='user',
                parts=[types.Part(text=user_input)]
            )
            
            # Run the runner and iterate over emitted events
            final_response = ""
            for event in runner.run(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=new_message,
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response = event.content.parts[0].text
            
            print(f"\n🤖 Assistant: {final_response}")
            
            # Retrieve updated session state to display it
            updated_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID
            )
            print("\n📈 [Session State]:", updated_session.state)
            
            # Retrieve list of saved artifacts to display them
            artifacts = await artifact_service.list_artifact_keys(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID
            )
            print("📦 [Saved Artifacts]:", list(artifacts))
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
'''

from google.adk.tools.tool_context import ToolContext

def remeber_name(
    name: str,
    tool_context: ToolContext,
) -> dict:
    '''
    Saves name in the session state
    '''
    tool_context.state["name"] = name
    return {
        "status":"Success",
        "message":f"I'll remember your name is {name}"
    }


