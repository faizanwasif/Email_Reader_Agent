import os

class EmailTool:
    def run(self, query: str = None) -> str:
        email_folder = "extracted_emails"
        emails = []

        if not os.path.exists(email_folder):
            return "No extracted emails found."

        for file_name in os.listdir(email_folder):
            if file_name.endswith('.txt'):
                with open(os.path.join(email_folder, file_name), 'r', encoding='utf-8') as f:
                    emails.append(f.read())

        return "\n\n".join(emails)