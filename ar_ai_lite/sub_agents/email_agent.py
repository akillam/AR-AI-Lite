import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_email(customer_name, amount, due_date, status):
    """
    Generates a context-aware email draft using Gemini.
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Tone instructions based on status
    if status == "OVERDUE":
        tone = "firm but professional. Emphasize that payment is past due."
    elif status == "DUE_SOON":
        tone = "polite and helpful. Just a gentle reminder."
    else:
        tone = "cheerful and appreciative."

    prompt = f"""
    You are an AR (Accounts Receivable) Email Agent.
    Write a short email to {customer_name}.
    
    Context:
    - Invoice Amount: ${amount}
    - Due Date: {due_date}
    - Status: {status}
    
    Instructions:
    - Tone: {tone}
    - Keep it under 100 words.
    - Include the invoice details clearly.
    - Sign off as "The Finance Team".
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ EMAIL AGENT ERROR: {e}")
        return f"Error generating email for {customer_name}"