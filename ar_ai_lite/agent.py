import sys
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Import local modules
from ar_ai_lite.tools import load_invoices, save_email_draft, save_summary
from ar_ai_lite.sub_agents.triage_agent import triage_invoice
from ar_ai_lite.sub_agents.email_agent import generate_email  # <--- NEW IMPORT

init(autoreset=True)
load_dotenv()

def main():
    print(Fore.CYAN + "🤖 AR-AI-Lite Agent Starting...")
    
    # 1. Load Data
    invoices = load_invoices('data/invoices_example.csv')
    if not invoices:
        print(Fore.RED + "No invoices found. Exiting.")
        return

    print(f"Loaded {len(invoices)} invoices.")

    overdue_count = 0
    total_outstanding = 0
    summary_lines = ["# Daily AR Summary\n"]

    for inv in invoices:
        print(f"\nProcessing Invoice #{inv['invoice_id']} for {inv['customer_name']}...")
        
        # 2. Triage (The "Brain")
        status = triage_invoice(inv)
        print(f"Status: {Fore.YELLOW if status == 'DUE_SOON' else Fore.RED if status == 'OVERDUE' else Fore.GREEN}{status}")

        # 3. Action Logic (The "Hands")
        # We now generate emails for OVERDUE *and* DUE_SOON items
        if status in ["OVERDUE", "DUE_SOON"]:
            if status == "OVERDUE":
                overdue_count += 1
                total_outstanding += float(inv['amount'])
            
            print(Fore.MAGENTA + "  Drafting AI email...")
            
            # CALL THE NEW EMAIL AGENT
            email_draft = generate_email(
                customer_name=inv['customer_name'],
                amount=inv['amount'],
                due_date=inv['due_date'],
                status=status
            )
            
            save_result = save_email_draft(inv['customer_name'], email_draft)
            print(Fore.BLUE + f"  -> {save_result}")

    # 4. Generate Summary
    summary_lines.append(f"- Total Overdue Invoices: {overdue_count}")
    summary_lines.append(f"- Total Outstanding Amount: ${total_outstanding}")
    
    save_summary("\n".join(summary_lines))
    print(Fore.CYAN + "\n✅ Process Complete. Summary saved to outputs/daily_summary.md")

if __name__ == "__main__":
    main()