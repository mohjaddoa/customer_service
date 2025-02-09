import re

class cleaning:
    def __init__(self):
        self.word_list = ["bye", "exit", "no", "stop"]
        
    def check_words_in_text(self, text):
        """
        Checks if certain keywords are present in the text and returns appropriate action.
        """
        # Convert text to lowercase to ensure case-insensitive matching
        text_lower = text.lower()
        words = text_lower.split()
        if "stop" in words or "exit" in words:
            return "break"
        else:
            return "continue"

    def clean_text(self, text):
        """
        Cleans the input text by removing unwanted characters and leading/trailing spaces.
        """
        text = text.strip()
        filtered_text = re.sub('[^a-zA-Z]', ' ', text)
        return filtered_text
