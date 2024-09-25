import os

from crewai_tools import BaseTool

class EmailTool(BaseTool):
    """
    Tool to read and return all emails from the 'extracted_emails' folder.
    Emails are stored in plain text files in the folder, and the tool will parse them into structured data.
    """
    name: str = "Email extractor tool"
    description: str = "This tool will extract and return emails from the 'extracted_emails' folder."

    def _run(self, query: str = None) -> list:
        """
        Reads emails from the 'extracted_emails' folder, parses them, and returns them as a list of dictionaries.
        
        Args:
            query: An optional filter (e.g., by subject, sender), but for now, it reads all files.

        Returns:
            A list of dictionaries, where each dictionary contains:
            - 'sender': The email sender.
            - 'subject': The email subject.
            - 'date': The email date.
            - 'body': The email content.
        """
        email_folder = "extracted_emails"
        emails = []

        if not os.path.exists(email_folder):
            print(f"The folder {email_folder} does not exist.")
            return emails

        # Iterate through each email file in the folder
        for file_name in os.listdir(email_folder):
            file_path = os.path.join(email_folder, file_name)
            
            # Only process .txt files
            if file_name.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read and parse the email contents
                    email_data = self._parse_email_file(f.read())
                    emails.append(email_data)

        return emails

    def _parse_email_file(self, file_content: str) -> dict:
        """
        Parses the content of an email file and returns structured email data.
        
        Args:
            file_content: The raw content of the email file.

        Returns:
            A dictionary with the structured data, including sender, subject, date, and body.
        """
        lines = file_content.split("\n")
        sender = self._extract_field(lines, "From:")
        date = self._extract_field(lines, "Date:")
        subject = self._extract_field(lines, "Subject:")
        
        # The body starts after the subject, skip empty lines
        body_index = lines.index("") + 1 if "" in lines else len(lines)
        body = "\n".join(lines[body_index:]).strip()

        return {
            'sender': sender,
            'date': date,
            'subject': subject,
            'body': body
        }

    def _extract_field(self, lines: list, field_name: str) -> str:
        """
        Extracts a specific field (e.g., "From:", "Date:") from the email content.

        Args:
            lines: List of lines in the email file.
            field_name: The field name to extract (e.g., "From:", "Date:").

        Returns:
            The extracted field value, or an empty string if not found.
        """
        for line in lines:
            if line.startswith(field_name):
                return line.replace(field_name, "").strip()
        return ""

