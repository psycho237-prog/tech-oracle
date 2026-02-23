import requests
import json
import os
from datetime import datetime

class TechOracle:
    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.report_content = [f"# 🦾 Tech Oracle Alpha Report - {self.report_date}\n"]
        self.report_content.append("> *Autonomous intelligence distilled from the developer ecosystem.*\n")

    def fetch_hacker_news(self):
        print("Fetching HackerNews...")
        try:
            top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:5]
            stories = []
            for item_id in top_ids:
                item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
                stories.append(f"- [{item.get('title')}]({item.get('url', f'https://news.ycombinator.com/item?id={item_id}')}) ({item.get('score')} points)")
            
            self.report_content.append("## 🧡 HackerNews Top Alpha")
            self.report_content.extend(stories)
            self.report_content.append("")
        except Exception as e:
            print(f"Error fetching HN: {e}")

    def fetch_reddit_tech(self):
        print("Fetching Reddit...")
        try:
            headers = {'User-Agent': 'TechOracle/1.0'}
            # Fetching from /r/technology and /r/programming
            for sub in ["technology", "programming"]:
                url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit=3"
                data = requests.get(url, headers=headers).json()
                stories = []
                for post in data['data']['children']:
                    p = post['data']
                    stories.append(f"- [{p['title']}](https://www.reddit.com{p['permalink']}) ({p['ups']} upvotes)")
                
                self.report_content.append(f"## 🤖 Reddit /r/{sub}")
                self.report_content.extend(stories)
                self.report_content.append("")
        except Exception as e:
            print(f"Error fetching Reddit: {e}")

    def fetch_github_trending(self):
        print("Fetching GitHub Trends...")
        try:
            # We use a simple search for repo created/updated in last 24h with high stars
            # This is a good proxy for "Trending"
            url = "https://api.github.com/search/repositories?q=stars:>50&sort=stars&order=desc"
            data = requests.get(url).json()
            repos = []
            for repo in data.get('items', [])[:5]:
                repos.append(f"- [{repo['full_name']}]({repo['html_url']}): {repo['description']} (⭐ {repo['stargazers_count']})")
            
            self.report_content.append("## 🚀 GitHub Trending Repos")
            self.report_content.extend(repos)
            self.report_content.append("")
        except Exception as e:
            print(f"Error fetching GitHub: {e}")

    def generate_report(self):
        self.fetch_hacker_news()
        self.fetch_reddit_tech()
        self.fetch_github_trending()

        report_path = f"reports/{self.report_date}.md"
        os.makedirs("reports", exist_ok=True)
        
        with open(report_path, "w") as f:
            f.write("\n".join(self.report_content))
        
        # Also update README to link to latest report
        with open("README.md", "w") as f:
            f.write(f"# 🦾 Tech Oracle\n\n")
            f.write(f"Autonomous intelligence hub. [Latest Report ({self.report_date})](./reports/{self.report_date}.md)\n\n")
            f.write("## 🗄️ Archives\n")
            # List some recent reports
            reports = sorted(os.listdir("reports"), reverse=True)[:10]
            for r in reports:
                f.write(f"- [{r.replace('.md', '')}](./reports/{r})\n")

        print(f"Report generated: {report_path}")

if __name__ == "__main__":
    oracle = TechOracle()
    oracle.generate_report()
