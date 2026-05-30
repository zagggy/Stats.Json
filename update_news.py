import json
import requests
import xml.etree.ElementTree as ET

# 1. Clean the Grafana API Error out of your stats file
stats_file = 'plumbing_stats.json'
try:
    with open(stats_file, 'r') as file:
        data = json.load(file)
        
    # Remove the news block that crashed Grafana
    clean_data = [row for row in data if "Industry_News" not in row]

    with open(stats_file, 'w') as file:
        json.dump(clean_data, file, indent=2)
except FileNotFoundError:
    pass

# 2. Fetch the latest plumbing industry news
rss_url = "https://news.google.com/rss/search?q=plumbing+industry"
response = requests.get(rss_url)

news_list = []
if response.status_code == 200:
    root = ET.fromstring(response.content)
    for item in root.findall('.//item')[:5]:
        title = item.find('title').text
        link = item.find('link').text
        news_list.append({"Title": title, "Link": link})

# 3. Save news to its OWN file so it never crashes the chart again
with open('plumbing_news.json', 'w') as file:
    json.dump(news_list, file, indent=2)
