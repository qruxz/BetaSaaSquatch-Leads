import requests
import streamlit as st
from company_scraper import get_company_info
from email_writer import generate_emails
from utils import export_to_csv
from dotenv import load_dotenv
import time
from momentum_score import get_momentum_score
from textblob import TextBlob
import os

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # Make sure this is set in your .env



def local_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #ffffff;
            color: #1C1C1E;
            font-family: 'Segoe UI', sans-serif;
        }

        .stButton>button {
            background-color: #4A90E2;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
            transition: 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #357ABD;
        }

        .stTextInput>div>div>input {
            background-color: #f9f9f9;
            color: #1C1C1E;
            border-radius: 6px;
            border: 1px solid #cccccc;
            padding: 8px;
        }

        .stMarkdown, .stExpander, .stImage, .stHeader, .stSubheader,
        .stText, .stTextInput label, .stTextInput div, .stTextArea label,
        .stSelectbox label, .stSelectbox div {
            color: #1C1C1E !important;
        }

        code {
            background-color: #f1f1f1;
            color: #00796B;
            font-size: 90%;
        }

        .signal-box {
            background-color: #E0F7FA;
            border-left: 5px solid #00796B;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 10px 0;
            color: #1C1C1E;
            font-weight: 500;
        }

        .news-box {
            background-color: #F5F5F5;
            padding: 10px 14px;
            border-left: 4px solid #90CAF9;
            border-radius: 6px;
            margin: 8px 0;
            font-size: 0.95rem;
        }
        </style>
    """, unsafe_allow_html=True)

# ✅ Load custom CSS
local_css()

# ✅ Set page config
st.set_page_config(page_title="SaaSquatch Leads", layout="centered")

st.markdown("""
    <div style="
        background-color: #E3F2FD;
        padding: 28px 32px;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        margin-bottom: 25px;
        border: 1px solid #BBDEFB;
    ">
        <h1 style="
            color: #0D47A1;
            font-family: 'Segoe UI', sans-serif;
            font-size: 2.8rem;
            margin: 0 0 14px 0;
        ">
            🤖 SaaSquatch Leads  <span style="font-weight: 400;">– Smart Company Insights & Outreach Emails</span>
        </h1>


            🔍 Type a company name and instantly get:

                ✔ Website & Email
                ✔ LinkedIn & Location 
                ✔ 3 Cold Emails (Friendly, Professional, Casual)


    </div>
""", unsafe_allow_html=True)



def classify_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return "🟢 Positive"
        elif polarity < -0.1:
            return "🔴 Negative"
        else:
            return "🟡 Neutral"
    except:
        return "Unknown"

def get_news_articles(company_name):
    try:
        url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=5&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
        res = requests.get(url)
        data = res.json()
        return data.get("articles", [])
    except:
        return []
local_css()
if "emails" not in st.session_state:
    st.session_state.emails = {}
if "info" not in st.session_state:
    st.session_state.info = {}

company_name = st.text_input("🔍 Enter a company name:", placeholder="e.g. Zoho, Figma, KraftBuddy")

col1, col2 = st.columns(2)
with col1:
    search = st.button("🚀 Fetch Info + Generate Emails")
with col2:
    regen = st.button("🔁 Regenerate Emails")

if search and company_name:
    with st.spinner("🔎 Finding company info..."):
        info = get_company_info(company_name)
        if info:
            st.success("✅ Company info found!")
            st.session_state.info = info

            domain = info["website"].replace("https://", "").replace("http://", "").split('/')[0]
            logo_url = f"https://logo.clearbit.com/{domain}"
            st.image(logo_url, width=100, caption="Company Logo")

            # 🚦 Momentum Score
            with st.spinner("📊 Analyzing company momentum..."):
                score, badge = get_momentum_score(company_name)
                st.markdown(f"""
                    <div class="signal-box">
                        <strong>📊 Momentum Score:</strong> {score}/100 &nbsp; {badge}
                    </div>
                """, unsafe_allow_html=True)

            # 📰 News Headlines with Sentiment
            with st.spinner("🧠 Analyzing recent news..."):
                articles = get_news_articles(company_name)
                if articles:
                    st.subheader("📰 Recent News Sentiment")
                    for article in articles:
                        title = article.get("title", "")
                        url = article.get("url", "")
                        sentiment = classify_sentiment(title)
                        st.markdown(f"""
                            <div class="news-box">
                                <strong>{sentiment}</strong><br>
                                <a href="{url}" target="_blank">{title}</a>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No news articles found.")

            # 🏢 Company Info Section
            st.subheader("🏢 Company Details")
            st.markdown(f"""
            - 🌐 **Website:** [{info['website']}]({info['website']})
            - 📧 **Email:** {info['email']}
            - 🧭 **Location:** {info['location']}
            - 💼 **LinkedIn:** [View Profile]({info['linkedin']})
            - 📝 **About:** {info['description']}
            """)

            with st.spinner("✍️ Generating emails..."):
                st.session_state.emails = generate_emails(company_name, info)
                time.sleep(1)
                st.success("📨 Emails generated!")
        else:
            st.error("❌ Couldn’t find company info. Try another name.")

if regen and st.session_state.info:
    with st.spinner("🔁 Re-generating emails..."):
        st.session_state.emails = generate_emails(company_name, st.session_state.info)
        time.sleep(1)
        st.success("✨ Emails refreshed!")

if st.session_state.emails:
    st.header("📬 Outreach Emails")
    for tone, content in st.session_state.emails.items():
        with st.expander(f"✉️ {tone.capitalize()} Email"):
            st.code(content)

    if st.button("📥 Download as CSV"):
        export_to_csv(company_name, st.session_state.info, st.session_state.emails)
        st.success("✅ CSV downloaded!")
