import json
import requests
import xml.etree.ElementTree as ET

# Targeting the exact file from your screenshot
json_file = 'plumbing_stats.json'

# 1. Fetch the latest plumbing industry news via Google News RSS
rss_url = "https://news.google.com/rss/search?q=plumbing+industry"
response = requests.get(rss_url)

news_list = []
if response.status_code == 200:
    root = ET.fromstring(response.content)
    # Grab the top 5 articles
    for item in root.findall('.//item')[:5]:
        title = item.find('title').text
        link = item.find('link').text
        news_list.append(f"{title} - {link}")

# 2. Read your current stats array
with open(json_file, 'r') as file:
    data = json.load(file)

# 3. Clean out any old news entries so the file doesn't duplicate every day
data = [row for row in data if "Industry_News" not in row]

# 4. Append the fresh news as a new item at the bottom of your list
if news_list:
    data.append({
        "Industry_News": "Latest Updates",
        "Articles": news_list
    })

# 5. Save it perfectly formatted back to your file
with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)
