import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def triage_invoice(invoice_data):
    """
    Analyzes an invoice and returns a status: OVERDUE, DUE_SOON, or OK.
    """
    # Use the stable 1.5-flash model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    You are an AR (Accounts Receivable) Triage Agent.
    Analyze the following invoice data:
    {invoice_data}
    
    Current Date: 2024-12-01 (Assume this is today)
    
    Rules:
    - If Due Date is before Today, it is OVERDUE.
    - If Due Date is within the next 7 days, it is DUE_SOON.
    - Otherwise, it is OK.
    
    Return ONLY one word: OVERDUE, DUE_SOON, or OK.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Print the actual error so we can see what's wrong
        print(f"❌ GEMINI ERROR: {e}")
        return "ERROR"