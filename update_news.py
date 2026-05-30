import os
import json
import requests
import xml.etree.ElementTree as ET

def fetch_and_inject():
    # 1. Fetch the plumbing RSS feed
    rss_url = "https://www.pmmag.com/rss"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(rss_url, headers=headers, timeout=15)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except Exception as e:
        print(f"Failed to fetch RSS data: {e}")
        return

    # 2. Build Markdown text from the latest 7 articles
    markdown_content = "### 📰 Latest Plumbing Industry News\n\n"
    items = root.findall(".//item")
    
    if not items:
        print("No items found in RSS feed.")
        return

    for item in items[:7]:
        title_tag = item.find("title")
        link_tag = item.find("link")
        
        title = title_tag.text.strip() if title_tag is not None else "No Title"
        link = link_tag.text.strip() if link_tag is not None else "#"
        markdown_content += f" * [{title}]({link})\n"

    # 3. Target your dashboard file.
    dashboard_path = "stat.json" 

    if not os.path.exists(dashboard_path):
        print(f"Error: Dashboard file not found at {dashboard_path}")
        return

    with open(dashboard_path, "r") as f:
        dashboard_data = json.load(f)

    # 4. Search and update the target text panel
    updated = False
    for panel in dashboard_data.get("panels", []):
        if panel.get("type") == "text" and panel.get("title") == "Industry News":
            panel["options"]["content"] = markdown_content
            updated = True
            
    if not updated:
        for row in dashboard_data.get("panels", []):
            for panel in row.get("panels", []):
                if panel.get("type") == "text" and panel.get("title") == "Industry News":
                    panel["options"]["content"] = markdown_content
                    updated = True

    if updated:
        with open(dashboard_path, "w") as f:
            json.dump(dashboard_data, f, indent=2)
        print("Dashboard file successfully updated with latest articles.")
    else:
        print("Could not find a Text panel named 'Industry News' inside your JSON structure.")

if __name__ == "__main__":
    fetch_and_inject()
