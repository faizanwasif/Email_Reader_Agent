from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
# from src.utils.agent_tools import URLTool
from langchain_openai import ChatOpenAI
from agent.email_agent_tool import EmailTool  # Assuming an EmailTool that fetches and parses emails
import os
from dotenv import load_dotenv

class PersonalAssistantModel:
    def __init__(self):
   
        load_dotenv()

        # Retrieve the OpenAI API Key from the .env file
        api_key = os.getenv('ANTHROPIC_API_KEY')
        self.email_tool = EmailTool()  # Tool for reading and parsing emails
        self.model = ChatAnthropic(model='claude-3-haiku-20240307',api_key=api_key)
        self.email_agent = self._create_email_agent()
        self.email_task = self._create_email_task()
        self.crew = self._create_crew()

    def _create_email_agent(self):
        return Agent(
            role="Personal Assistant",
            goal="""
                Your job is to read emails and convert the information into actionable tasks, priorities, and important items.
                Extract key information such as deadlines, important meetings, action items, or follow-ups from the email content.
                Prioritize the tasks based on urgency, deadlines, and relevance.
                Group the emails into categories such as meetings, tasks, follow-ups, and general information.
                Make sure to highlight any urgent tasks or emails that need immediate action.
            """,
            backstory="""
                You are a highly organized personal assistant working for a busy executive.
                Your role is to ensure that all incoming emails are efficiently parsed, summarized, and converted into actionable tasks.
                You must prioritize the tasks based on urgency and importance and ensure nothing falls through the cracks.
                Provide summaries and lists of tasks from emails.
            """,
            max_iter=20,
            tools=[self.email_tool],
            llm=self.model,
            allow_delegation=True,
            verbose=True
        )

    def _create_email_task(self):
        return Task(
            description="""
                Analyze the email contents provided and summarize them into the following:
                - Important tasks with due dates or deadlines.
                - Meetings or events with their details (date, time, location, etc.).
                - Action items that require a response or follow-up.
                - Any critical information that needs to be flagged as urgent.
                
                Provide an organized list that categorizes the tasks into:
                - Immediate tasks
                - Important tasks for today
                - General tasks
                Also, rate the priority level (high, medium, low) for each task.
            """,
            expected_output="""
                The summary should include:
                - A list of all tasks extracted from the email.
                - Priority levels (high, medium, low).
                - Deadlines, if any, for each task.
                - Follow-up items with suggested next actions.
                - Any flagged urgent items.
            """,
            tools=[self.email_tool],
            agent=self.email_agent
        )

    def _create_crew(self):
        return Crew(
            agents=[self.email_agent],
            tasks=[self.email_task],
            verbose=True
        )

    def process_emails(self):
        """
        Process the emails, extract action items, and organize them based on importance and deadlines.
        """
        #
        email_input = {}
        return self.crew.kickoff(inputs=email_input)

