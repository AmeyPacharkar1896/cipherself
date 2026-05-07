import argparse
import sys
from collector import GitHubCollector, SearchCollector
from generator import ReportGenerator

import os
from pdf2image import convert_from_path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="cipherself - Digital Footprint Intelligence Tool")
    parser.add_argument("--github", help="GitHub username")
    parser.add_argument("--name", help="Full Name of the subject")
    parser.add_argument("--demo", action="store_true", help="Generate a demo report with fictional data")
    
    args = parser.parse_args()

    if args.demo:
        print("[*] Running in DEMO mode with fictional data...")
        gh_data = {
            "profile": {
                "location": "San Francisco, CA",
                "bio": "Software Engineer interested in Rust and Distributed Systems.",
                "created_at": "2018-05-07T00:00:00Z"
            },
            "repos_count": 28,
            "languages": {"Python": 12, "Rust": 10, "Go": 6},
            "stars": 1243,
            "activity_stats": {
                "days": {"Wednesday": 15},
                "hours": {20: 10} # Evening
            },
            "last_active": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "search_results": [
                {"title": "Alex Mercer - Personal Blog", "url": "https://alexmercer.dev", "snippet": "Writing about Rust, distributed systems, and developer tooling"},
                {"title": "alexmercer-dev on DEV Community", "url": "https://dev.to/alexmercer", "snippet": "12 posts on backend architecture and CLI tools"},
                {"title": "Alex Mercer | LinkedIn", "url": "https://linkedin.com/in/alexmercer", "snippet": "Software Engineer at a Series B startup in San Francisco"}
            ]
        }
        subject_name = "Alex Mercer"
        github_user = "alexmercer-dev"
    else:
        if not args.github or not args.name:
            parser.error("The --github and --name arguments are required when not in --demo mode.")
            
        subject_name = args.name
        github_user = args.github
        
        print(f"[*] Initiating collection for: {subject_name} (@{github_user})")
        
        # 1. Collect GitHub Data
        print("[+] Fetching GitHub intelligence...")
        gh = GitHubCollector(github_user)
        gh_data = gh.fetch_all()
        
        if not gh_data:
            print(f"[!] Error: Could not fetch data for GitHub user '{github_user}'. Check username or rate limits.")
            sys.exit(1)
            
        # 2. Collect Search Data
        print("[+] Scanning public records via Google...")
        sc = SearchCollector(subject_name)
        search_results = sc.fetch_top_results(limit=10)
        gh_data['search_results'] = search_results
    
    # 3. Generate Report
    print("[+] Compiling intelligence report...")
    gen = ReportGenerator(gh_data, subject_name, github_user, demo_mode=args.demo)
    output_file = gen.generate()
    
    print(f"[*] Report successfully generated: {output_file}")
    
    # 4. Handle Demo Assets
    if args.demo:
        print("[+] Converting demo report to preview image...")
        if not os.path.exists("assets"):
            os.makedirs("assets")
        
        images = convert_from_path(output_file, first_page=1, last_page=1)
        if images:
            images[0].save("assets/preview.png", "PNG")
            print("[*] Preview image saved to assets/preview.png")

    print("[*] Operation complete.")

if __name__ == "__main__":
    main()
