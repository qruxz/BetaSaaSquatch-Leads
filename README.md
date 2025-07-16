# 🦄 SaaSquatch Leads – Smart Company Signals + Cold Outreach

**SaaSquatch Leads** is a lightweight AI-powered prospecting tool that scrapes key company data, analyzes momentum signals, and auto-generates 3 customized cold emails — all using free APIs and open models. Built in under 5 hours as part of the Caprae Capital Internship Challenge 2025.

---

## 🚀 Features

- 🔍 **Company Info Extractor**  
  Gets company name, website, LinkedIn, email (real or fallback), location, and logo  
  → Uses `DuckDuckGo`, `Clearbit`, `WHOIS`, and heuristic scraping

- ✍️ **Cold Email Writer (via Mixtral)**  
  Uses the **Groq API** to generate 3 short cold emails in different tones:  
  - Friendly 🤝  
  - Professional 🧑‍💼  
  - Casual 😎

- 📊 **Momentum Score Engine**  
  Computes a 0–100 score using:  
  - Hiring signals (mock/randomized)  
  - Funding mentions (NewsAPI)  
  - Traffic guess (mocked)  
  - News sentiment (TextBlob NLP)  
  - LinkedIn interest (mocked)

  → Outputs a smart badge: 🟢 Surging / 🟡 Growing / 🔴 Flat

- 📰 **Live News Headlines + Sentiment**  
  Pulls the 5 latest articles using NewsAPI and tags sentiment using TextBlob  
  → Labels each as Positive / Neutral / Negative

- 💅 **Beautiful UI (Psych Palette)**  
  Clean white Streamlit theme with soft blues and neutrals  
  → Intuitive design that builds trust and reduces bounce

- 📥 **One-Click CSV Export**  
  Downloads company info + all generated emails for sharing or saving

---

## 🧠 Tech Stack

| Layer           | Details                                           |
|------------------|----------------------------------------------------|
| Frontend         | Streamlit (custom CSS for design)                  |
| Scraping         | DuckDuckGo, WHOIS RDAP, requests, Clearbit logos   |
| Email Generator  | Groq API with Mixtral-8x7B                         |
| Sentiment NLP    | TextBlob (headline analysis)                       |
| Data Handling    | pandas, dotenv                                     |

---

## 🗂 Project Structure

## 🗂 Project Structure

SaaSquatch-Leads/
├── app.py ← Main Streamlit interface
├── company_scraper.py ← Scrapes website/email/logo/location
├── email_writer.py ← Generates emails using Groq
├── momentum_score.py ← Analyzes startup momentum signals
├── utils.py ← CSV exporting
├── requirements.txt ← Dependencies
└── README.md ← You’re reading it

yaml
Copy
Edit

---

## ⚙️ Run Locally

```bash
git clone https://github.com/yourusername/saasquatch-leads.git
cd saasquatch-leads

# Install dependencies
pip install -r requirements.txt

# Add your API key(s)
echo NEWSAPI_KEY=your_newsapi_key > .env

# Launch the app
streamlit run app.py
💡 Why This Project?
In fast-paced startup research or VC work, time = edge.
The typical researcher opens 4–6 tabs and spends 10+ minutes per lead.

With SaaSquatch Leads, everything — scraping, scoring, and messaging — happens in seconds.

This isn’t just automation — it’s smart intuition:

✅ Am I reaching out to the right company?

📈 Are they growing? Hiring? Trending?

✉️ What’s the best tone for a cold email?

🧠 All answered. In a few clicks.

📬 Sample Output
json
Copy
Edit
{
  "name": "Figma",
  "website": "https://figma.com",
  "email": "contact@figma.com",
  "location": "USA",
  "linkedin": "https://linkedin.com/search/results/all/?keywords=Figma",
  "momentum_score": 84,
  "badge": "🟢 Surging"
}
📸 Screenshots (optional)
Create a /demo/ folder with:

company_info.png

emails.png
to show output on GitHub

🙌 Built For
Caprae Capital Internship Challenge 2025
By [Your Name]
Powered by Groq + NewsAPI + Streamlit + Free Web Intelligence
