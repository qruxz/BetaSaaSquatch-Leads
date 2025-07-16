# utils.py
import pandas as pd

def export_to_csv(company, info, emails):
    rows = []
    for tone, email in emails.items():
        rows.append({
            "Company": company,
            "Website": info['website'],
            "LinkedIn": info['linkedin'],
            "Email": info['email'],
            "Tone": tone,
            "Email Body": email
        })

    df = pd.DataFrame(rows)
    df.to_csv("SaaSquatch Leads.csv", index=False)
