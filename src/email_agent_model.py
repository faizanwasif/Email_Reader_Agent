import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from email_agent_tool import EmailTool

load_dotenv()

class PersonalAssistantModel:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        self.email_tool = EmailTool()
        self.model = ChatAnthropic(model='claude-3-haiku-20240307', anthropic_api_key=api_key)

    def process_emails(self):
        emails = self.email_tool.run()
        

        prompt = f"""
        You are a personal assistant tasked with processing the following emails. Please analyze them and provide a summary in a professional and easy-to-understand tone. Use simple vocabulary suitable for non-native English speakers.

        Your summary should include the following sections, formatted using simple HTML tags:

        <h2>Important Tasks or Action Items:</h2>
        <ul>
        <li>List important tasks or action items here.</li>
        </ul>

        <h2>Upcoming Meetings or Events:</h2>
        <ul>
        <li>Include any scheduled dates and times.</li>
        </ul>

        <h2>Urgent Matters Needing Immediate Attention:</h2>
        <ul>
        <li>Highlight any issues that require immediate action.</li>
        </ul>

        <h2>General Updates:</h2>
        <ul>
        <li>Include any other relevant information or updates from the emails.</li>
        </ul>

        <h2>Questions or Concerns Raised:</h2>
        <ul>
        <li>List any questions or concerns mentioned in the emails.</li>
        </ul>

        Please strictly follow this structure and format the output without adding unnecessary empty lines or spaces between headings and lists.

        Here are the emails:

        {emails}
        """
        #         prompt = f"""
# You are a personal assistant tasked with processing the following emails. Please analyze them and provide a summary in a professional and easy-to-understand tone. Use simple vocabulary suitable for non-native English speakers.
 
# Your summary should include the following sections, formatted using simple HTML tags for clarity:
 
# <h2>Important Tasks or Action Items:</h2>
# <ul>
# <li>List important tasks or action items here.</li>
# <li>Prioritize them from highest to lowest importance.</li>
# </ul>
# <h2>Upcoming Meetings or Events:</h2>
# <ul>
# <li>Include any scheduled dates and times.</li>
# </ul>
# <h2>Urgent Matters Needing Immediate Attention:</h2>
# <ul>
# <li>Highlight any issues that require immediate action.</li>
# </ul>
#  <h2>General Updates:</h2>
# <ul>
# <li>Include any other relevant information or updates from the emails.</li>
# </ul>
# <h2>Questions or Concerns Raised:</h2>
# <ul>
# <li>List any questions or concerns mentioned in the emails.</li>
# </ul>
 
# Please strictly follow this structure and do not include any example content or additional explanations. Ensure the output is properly formatted in HTML without unnecessary empty lines or spaces.
 
# Here are the emails:
 
# {emails}
# """




         


    

        response = self.model.invoke(prompt)
        return response.content

def run_email_processing():
    assistant = PersonalAssistantModel()
    result = assistant.process_emails()
    return result

if __name__ == "__main__":
    result = run_email_processing()
    print(result)