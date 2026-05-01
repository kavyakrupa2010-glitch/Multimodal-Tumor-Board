import os
from crewai import Agent, Task, Crew

def run_tumor_board(vision_description: str, patient_history: str) -> str:
    """
    Orchestrates the Multimodal Tumor Board using CrewAI.
    Passes the textual analysis and patient history to specialized agents.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    # CrewAI uses LiteLLM integration. By specifying 'gemini/...', it routes directly via the GEMINI_API_KEY.
    llm_string = "gemini/gemini-2.5-flash" 

    # 1. Define the Agents
    pathologist = Agent(
        role='Chief Pathologist',
        goal='Analyze the raw visual description of the pathology slide and identify specific disease markers.',
        backstory='You are a world-renowned pathologist. You receive visual analysis descriptions of slides and translate them into clinical pathology findings.',
        llm=llm_string,
        verbose=True,
        allow_delegation=False
    )
    
    radiologist = Agent(
        role='Lead Radiologist',
        goal='Evaluate the patient history and correlate with the pathology findings for any cross-modal indicators.',
        backstory='An expert radiologist who looks at the whole patient picture to ensure no systemic spread or imaging correlations are missed.',
        llm=llm_string,
        verbose=True,
        allow_delegation=False
    )
    
    oncologist = Agent(
        role='Chief Medical Oncologist',
        goal='Synthesize the pathology and radiology assessments with the patient history to formulate a final Tumor Board Verdict and Treatment Plan.',
        backstory='You lead the Tumor Board. You combine inputs from various specialists to create actionable, safe, and effective treatment plans.',
        llm=llm_string,
        verbose=True,
        allow_delegation=False
    )

    # 2. Define the Tasks
    task1 = Task(
        description=f'Review the following pathology slide description: "{vision_description}". Also review the patient history: "{patient_history}". Formulate a detailed pathology report.',
        expected_output='A detailed pathology report summarizing the findings.',
        agent=pathologist
    )
    
    task2 = Task(
        description='Review the pathology report and the patient history. Identify if the current findings suggest localized or systemic disease that would require specific imaging or correlates with common radiological profiles.',
        expected_output='A radiology and systemic risk assessment report.',
        agent=radiologist
    )
    
    task3 = Task(
        description='Based on the pathology report and the radiology assessment, create a comprehensive Tumor Board Verdict. Define the final diagnosis and propose a multi-stage recommended treatment plan.',
        expected_output='A final, highly professional Tumor Board Verdict document (Markdown format) including Diagnosis, Staging Context, and Recommended Treatment Plan.',
        agent=oncologist
    )

    # 3. Form the Crew and Kickoff
    tumor_board_crew = Crew(
        agents=[pathologist, radiologist, oncologist],
        tasks=[task1, task2, task3],
        verbose=True
    )

    try:
        # Start the discussion
        result = tumor_board_crew.kickoff()
        # Crew output object to string resolves to the final output of the last task
        return str(result)
    except Exception as e:
        return f"Error during standard Tumor Board execution: {str(e)}"
