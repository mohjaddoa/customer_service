from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from text_processing import cleaning
from info_extraction import Extraction
import datetime
import myvoice_text
import re

user_response=[]
AI_response=[]

voice_text_instance = myvoice_text.myvoice_text()
using_text = cleaning()
extractor = Extraction()
extractor.download_spacy_model()
# Initialize OpenAI Chat Model and Memory
llm = ChatOpenAI(temperature=0, openai_api_key="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")

memory = ConversationBufferMemory()


# Example usage


# Main function to handle user interaction
def handle_booking():
    print("Hello, this is Sara from Dr. John Macrethy's clinic. How can I help you?")
    voice_text_instance.text_to_speech("Hello, this is Sara from Dr. John Macrethy's clinic. How can I help you?")
    while True:
        # Get user input as text
        # user_query = input("\nYour response: ")        
        # convert voice to text
        user_query = voice_text_instance.transcribe_audio()
        user_response.append(using_text.clean_text(user_query))
        status = using_text.check_words_in_text(using_text.clean_text(user_query))
        # if "bye" or "no thank you" in user_query.lower():
        #     print("Goodbye!")
        if status == "break":
            # voice_text_instance.text_to_speech("Goodbye")
            print("Goodbye!")
            break
        else:
            # Add user message to memory
            memory.chat_memory.add_user_message(user_query)

            # Define the system prompt
            system_prompt = """
            You are a professional and polite assistant dedicated to booking appointments for patients.
            You assist Dr. John Macrethy, who is available for appointments on weekdays (Monday to Friday) from 9:00 AM to 5:00 PM.

            Your responsibilities include:
            1- Recording the patient's name.
            2- Recording the appointment details, including the year, month, day, and time.
            3- Ensuring a smooth and efficient booking process while maintaining politeness and professionalism.

            Use the conversation history to maintain context and provide a cohesive experience.
            """

            # Add the system prompt to memory
            memory.chat_memory.add_ai_message(system_prompt)
            response = llm(memory.chat_memory.messages + [HumanMessage(content=user_query)])  
            response_text = response.content.strip()
            # Add AI response to memory
            memory.chat_memory.add_ai_message(response_text)
            print(f"AI response: {response_text}")
            voice_text_instance.text_to_speech(response_text)
            AI_response.append(response_text)

# Run the program
if __name__ == "__main__":
    voice_text_instance.text_to_speech("This is a voice system for booking appointments. After completing your booking, please remember to say STOP or EXIT at any time to end the conversation.")
    handle_booking()
    results = extractor.extract_date_time_day(user_response,AI_response)
    unique_values = set()
    for values in results.values():
        unique_values.update(values)
    unique_values = list(unique_values)
    combind_list = AI_response + user_response
    names = extractor.extract_names(combind_list)
    names = set(names)
    names = list(names)
    for name in names:
        if name not in ["John","john","dr","Dr","Macrethy","macrethy","Sarah","sarah"]:
            #   print(name)
            customer_name=name
    print("names :",customer_name)
    print("date and time :",unique_values)
    # print(user_response)
    # print(AI_response)

