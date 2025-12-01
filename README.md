**Problem: The "Awkward Ask" of Accounts Receivable**

Cash flow is the lifeblood of any business, yet the process of collecting payments (Accounts Receivable) is notoriously inefficient. For small business owners and finance teams, chasing invoices is a "death by a thousand cuts" problem:

- It is tedious: Manually checking due dates against calendars takes hours.
- It requires context-switching: One minute you are analyzing data, the next you are trying to write a polite email.
- It is emotionally draining: Asking for money is awkward. It requires striking a delicate balance between maintaining a customer relationship (polite) and ensuring the business gets paid (firm).

I wanted to solve the friction between identifying a late payment and taking action on it.

**Why Agents**

From Hard-Coded Logic to Contextual Reasoning

Traditional automation (like Excel macros or simple Python scripts) fails at this task because it lacks nuance. A standard script sends the exact same robotic template to a loyal customer who is one day late as it does to a chronic non-payer who is a month late.

AI Agents are the right solution because they introduce reasoning into the loop.

Decision Making: An agent can look at a date and "reason" about the severity (e.g., "This is due soon, so we shouldn't be aggressive").

Adaptive Communication: An agent can dynamically adjust the tone of an email based on the context, ensuring the business maintains relationships while still being effective.

**What I Created**

Architecture: The "Hub and Spoke" Orchestrator

I built a modular multi-agent system using a Central Orchestrator pattern. The system does not just run a single prompt; it coordinates specialized sub-agents to perform distinct roles.

The Architecture:

The Orchestrator (agent.py): The main controller. It loads the invoice data, manages the workflow, and delegates tasks to sub-agents.

The Triage Agent (triage_agent.py): The "Analyst." It receives raw invoice data and uses LLM reasoning to classify the status as OVERDUE, DUE_SOON, or OK. It handles the logic of dates and severity.

The Email Agent (email_agent.py): The "Copywriter." It receives the status from the Triage Agent and drafts a custom email.

Input: Status: OVERDUE → Output: Firm, professional tone.

Input: Status: DUE_SOON → Output: Polite, helpful reminder.

Tools & IO (tools.py): Handles the "hands" of the agent—reading CSVs and saving the resulting drafts to the file system.

**Demo**

Input Data (invoices.csv)

The system processes a dataset containing mixed scenarios:
Acme Corp: Due last month (High urgency).
Globex Inc: Due next week (Low urgency).

The Process (Terminal Output)
The Orchestrator loops through the data, calls the Triage Agent to determine status, and conditionally calls the Email Agent.
code

Text
🤖 AR-AI-Lite Agent Starting...
Processing Invoice #101 for Acme Corp...
Status: OVERDUE
  Drafting AI email...
  -> Saved email for Acme Corp to outputs/email_Acme_Corp.txt

Processing Invoice #102 for Globex Inc...
Status: DUE_SOON
  Drafting AI email...
  -> Saved email for Globex Inc to outputs/email_Globex_Inc.txt

The Output (Generated Drafts)

The system produces distinct outputs based on context:
Output 1 (Overdue): "Dear Acme Corp, This is a reminder that invoice #101 was due on 2024-11-01. Please remit payment immediately..." (Firm tone).

Output 2 (Due Soon): "Hi Globex team, Just a friendly note that invoice #102 is coming up due next week..." (Polite tone).

**The Build**

Tech Stack & Tools

IDE: Cursor. I used Cursor’s AI-native features (Composer) to rapidly scaffold the directory structure and generate the initial boilerplate for the sub-agents. I also used Cursor because I am a non-coder who is learning AI coding tools like Cursor and Replit. 

Language: Python 3.12. 

Model: Google Gemini 2.0 Flash. I chose this model for its speed and low latency, which is critical when running an agent loop over hundreds of rows of data.

Libraries:

google-generativeai: To interface with the LLM.
pandas: For robust CSV data handling.
colorama: To create a readable CLI (Command Line Interface) experience.

Workflow:

I started by defining the Tooling Layer (getting data in and out). Once that was robust, I built the Triage Agent to ensure the logic was sound before connecting the Email Agent. This modular approach made debugging easy—if an email tone was off, I knew exactly which file to fix without breaking the rest of the application.

**If I had more time:**

This project is a functional "Lite" version, but the architecture is ready to scale. With more time, I would implement:

Long-term Memory: A memory.py module to track customer history. If a customer always pays late, the agent should know that context and not be too aggressive immediately.

Human-in-the-Loop UI: Instead of saving to text files, I would build a simple Streamlit interface where a finance manager can review and "One-Click Send" the emails via the Gmail API.

A nice web based UI

Dunning settings and email templates so users could decide the follow up schedule and look and feel of emails. 

Integration with Resend for email functionality. 

An aging report showing users a quick overview of their receivables and upcoming invoices that will likely be paid. 

Summary Agent: A third sub-agent that reads all the generated actions and writes a "Morning Briefing" for the CFO, highlighting which accounts are most at risk.
