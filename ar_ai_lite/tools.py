import pandas as pd
import os

def load_invoices(filepath: str):
    """Loads invoices from a CSV file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return []
    df = pd.read_csv(filepath)
    return df.to_dict(orient='records')

def save_email_draft(customer_name: str, email_content: str):
    """Saves a generated email draft to the outputs folder."""
    filename = f"outputs/email_{customer_name.replace(' ', '_')}.txt"
    with open(filename, "w") as f:
        f.write(email_content)
    return f"Saved email for {customer_name} to {filename}"

def save_summary(summary_text: str):
    """Saves the daily summary."""
    with open("outputs/daily_summary.md", "w") as f:
        f.write(summary_text)