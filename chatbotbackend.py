from mistralai import Mistral
from dotenv import load_dotenv
from datetime import date
import os
import requests
import PyPDF2
import io


load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
RESUME_URL = "https://abhay-spring.vercel.app/resume.pdf"

client = Mistral(api_key=MISTRAL_API_KEY)

def get_resume_text() -> str:
    response = requests.get(RESUME_URL)
    pdf_file = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdf_file)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text

def get_chat_response(conversation_history: list) -> str:
    resume_text = get_resume_text()
    today = date.today().strftime("%B %d, %Y")
    
    system_message = {
        "role": "system",
        "content": f"""You are Abhay's personal portfolio assistant chatbot.
        Today's date is {today}. Use this to calculate age or any time related questions accurately.
        You answer questions based strictly on the following resume content:
        
        {resume_text}
        
        Guidelines:
        - Only answer questions related to Abhay's skills, experience, projects, education, age, phone number and other details such as github link, linkedin link, leetcode link or any particular project link
        - If someone asks something not related to Abhay, politely redirect them
        - Keep answers concise, friendly and professional
        - If information is not found in the resume, say you don't have that information
        - GitHub: https://github.com/abhayk2
        - LinkedIn: https://www.linkedin.com/in/abhayk176/
        - Portfolio: https://abhay-spring.vercel.app
        - LeetCode: https://leetcode.com/u/abhaykum222/
        - Date of Birth: 7th December 2000
        """
    }
    
    messages = [system_message] + conversation_history
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages
    )
    
    return response.choices[0].message.content
