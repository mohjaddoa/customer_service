import re
from dateutil import parser
from datetime import datetime
import spacy
import streamlit as st


class Extraction:
    def __init__(self):
        self.nlp = None

    def download_spacy_model(self):
        """Ensure the spaCy model is downloaded and load it."""
        status = ""
        try:
            # Attempt to load the model
            self.nlp = spacy.load("en_core_web_sm")
            status = "Model 'en_core_web_sm' is already downloaded and ready to use."
            # st.write("Model 'en_core_web_sm' is already downloaded and ready to use.")
        except OSError:
            # If the model is not found, download it
            status = "Model 'en_core_web_sm' not found. Downloading now..."
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            status ="Model 'en_core_web_sm' has been downloaded successfully."
        return status

    def extract_date_time_day(self,text_list, ai_list):
        # Regular expressions for date, time, and days of the week
        date_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{4})\b'
        time_pattern = r'\b(?:\d{1,2}:\d{2}(?:am|pm)|\d{1,2}(?:am|pm| pm))\b'
        day_pattern = r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b'

        # Extract dates, times, and days from text
        dates_from_text = [re.search(date_pattern, t).group() for t in text_list if re.search(date_pattern, t)]
        times_from_text = [re.search(time_pattern, t).group() for t in text_list if re.search(time_pattern, t)]
        days_from_text = [re.search(day_pattern, t).group() for t in text_list if re.search(day_pattern, t)]

        # Extract dates, times, and days from AI responses
        dates_from_ai = [re.search(date_pattern, a).group() for a in ai_list if re.search(date_pattern, a)]
        times_from_ai = [re.search(time_pattern, a).group() for a in ai_list if re.search(time_pattern, a)]
        days_from_ai = [re.search(day_pattern, a).group() for a in ai_list if re.search(day_pattern, a)]

        # Return the results as a dictionary
        return {
            'dates_from_text': dates_from_text,
            'times_from_text': times_from_text,
            'days_from_text': days_from_text,
            'dates_from_ai': dates_from_ai,
            'times_from_ai': times_from_ai,
            'days_from_ai': days_from_ai
        }


    def extract_names(self, text_list):
        """Extract names from a list of text strings using spaCy's NER."""
        if not self.nlp:
            raise ValueError("SpaCy model is not loaded. Call `download_spacy_model` first.")

        names = []
        for text in text_list:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":  # Look for entities labeled as PERSON
                    names.append(ent.text)
        return list(set(names))  # Remove duplicates
