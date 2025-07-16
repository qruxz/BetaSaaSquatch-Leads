# company_scraper.py

from duckduckgo_search import ddg
import requests
from bs4 import BeautifulSoup
import re
import socket
from ipwhois import IPWhois

def scrape_email_from_website(website_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        # Try homepage first
        response = requests.get(website_url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        if emails:
            return emails[0]

        # 🔁 Fallback: try common paths
        fallback_paths = ["/contact", "/contact-us", "/about", "/about-us", "/team", "/support", "/help", "/get-in-touch", "/customer-support"]
        for path in fallback_paths:
            full_url = website_url.rstrip("/") + path
            try:
                res = requests.get(full_url, headers=headers, timeout=8)
                soup = BeautifulSoup(res.text, "html.parser")
                text = soup.get_text()
                emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
                if emails:
                    return emails[0]
            except:
                continue

        # 🔚 Final fallback: guess email from domain
        domain = website_url.replace("http://", "").replace("https://", "").split("/")[0]
        return f"contact@{domain}"
    except Exception as e:
        print("Email scraping error:", e)
        return "Not found"


def get_location_from_website(url, description=""):
    try:
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]
        ip = socket.gethostbyname(domain)
        whois = IPWhois(ip).lookup_rdap()
        country = whois['network'].get('country', None)
        if country:
            return country
    except:
        pass

    # Fallback: try from description
    if "India" in description:
        return "India"
    elif "USA" in description:
        return "USA"
    elif "UK" in description:
        return "UK"

    # 🔚 Final fallback: Default to USA
    return "USA"


# ✅ 3. COMPANY LOGO

def get_logo_from_website(url):
    try:
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]
        return f"https://logo.clearbit.com/{domain}"
    except:
        return ""

# ✅ 4. MAIN FUNCTION

def get_company_info(company_name):
    results = ddg(company_name + " official site", max_results=5)
    if not results:
        return None

    # Pick the best non-junk result
    main_result = next((r for r in results if "example.com" not in r['href']), results[0])
    website = main_result.get('href')

    # Clean URLs if needed
    if website.startswith("https://www.google.com/url?q="):
        website = website.split("q=")[-1].split("&")[0]

    title = main_result.get('title', company_name)
    description = main_result.get('body', f"{company_name} is a growing business.")

    email = scrape_email_from_website(website)
    location = get_location_from_website(website, description)
    logo = get_logo_from_website(website)

    return {
        "name": title,
        "website": website,
        "linkedin": f"https://www.linkedin.com/search/results/all/?keywords={company_name.replace(' ', '%20')}",
        "location": location,
        "email": email,
        "logo": logo,
        "description": description
    }
