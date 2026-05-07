import argparse
import sys
import os
from datetime import datetime

from cipherself.config import DEMO_DATA
from cipherself.collector.github import GitHubCollector
from cipherself.collector.search import SearchCollector
from cipherself.collector.reddit import RedditCollector
from cipherself.analyzer.personality import PersonalityAnalyzer
from cipherself.analyzer.valuation import ValuationAnalyzer
from cipherself.analyzer.reddit_personality import RedditAnalyzer
from cipherself.generator.pdf import PDFGenerator

def cli():
    parser = argparse.ArgumentParser(description="cipherself - Digital Footprint Intelligence Tool")
    parser.add_argument("--github", help="GitHub username")
    parser.add_argument("--name", help="Full Name of the subject")
    parser.add_argument("--reddit", help="Reddit username (optional)")
    parser.add_argument("--demo", action="store_true", help="Generate a demo report with fictional data")
    
    args = parser.parse_args()

    if args.demo:
        # ... existing demo logic ...
        print("[*] Running in DEMO mode with fictional data...")
        gh_data = {
            "profile": DEMO_DATA["profile"],
            "repos_count": DEMO_DATA["repos_count"],
            "languages": DEMO_DATA["languages"],
            "stars": DEMO_DATA["stars"],
            "activity_stats": DEMO_DATA["activity_stats"],
            "last_active": DEMO_DATA["last_active"],
            "search_results": DEMO_DATA["search_results"]
        }
        subject_name = DEMO_DATA["name"]
        github_user = DEMO_DATA["github_username"]
        reddit_data = None
        reddit_intel = []
    else:
        if not any([args.github, args.name, args.reddit]):
            parser.error("Please provide at least one of: --github, --name, or --reddit")
            
        subject_name = args.name or args.github or args.reddit or "Unknown Subject"
        github_user = args.github
        
        print(f"[*] Initiating collection for: {subject_name}")
        
        # 1. Collect GitHub Data
        gh_data = None
        if args.github:
            print("[+] Fetching GitHub intelligence...")
            gh = GitHubCollector(args.github)
            gh_data = gh.fetch_all()
            if not gh_data:
                print(f"[!] Warning: Could not fetch data for GitHub user '{args.github}'.")
        
        # 2. Collect Search Data
        if args.name:
            print("[+] Scanning public records via Google...")
            sc = SearchCollector(args.name)
            if gh_data:
                gh_data['search_results'] = sc.fetch_top_results(limit=10)
            else:
                gh_data = {'search_results': sc.fetch_top_results(limit=10)}
        elif gh_data:
            gh_data['search_results'] = []
            
        # 3. Collect Reddit Data
        reddit_data = None
        reddit_intel = []
        if args.reddit:
            rc = RedditCollector(args.reddit)
            reddit_data = rc.fetch_all()
            if reddit_data:
                ra = RedditAnalyzer(reddit_data, gh_data)
                reddit_intel = ra.infer()
    
    # 2. Analyze Data
    print("[+] Analyzing subject intelligence...")
    personality_intel = ""
    if gh_data and 'profile' in gh_data:
        personality_analyzer = PersonalityAnalyzer(gh_data, demo_mode=args.demo)
        personality_intel = personality_analyzer.infer()
    
    valuation_intel = {
        "richness": "Low", "google": 0.0, "meta": 0.0, "brokers": 0.0, "total": 0.0, "lifetime": 0.0, "sources": "None"
    }
    valuation_analyzer = ValuationAnalyzer(gh_data, reddit_data, demo_mode=args.demo)
    valuation_intel = valuation_analyzer.calculate()
    
    # 3. Generate Report
    print("[+] Compiling intelligence report...")
    
    # Determine output folder
    if args.demo:
        output_subfolder = "demo"
    else:
        sources = []
        if args.github: sources.append("github")
        if args.reddit: sources.append("reddit")
        if args.name: sources.append("name")
        
        if len(sources) == 3:
            output_subfolder = "full"
        else:
            output_subfolder = "_".join(sources)
            
    output_dir = os.path.join("outputs", output_subfolder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    gen = PDFGenerator(gh_data, subject_name, github_user, personality_intel, valuation_intel, reddit_data, reddit_intel)
    # Update filename to include path
    gen.filename = os.path.join(output_dir, gen.filename)
    output_file = gen.generate()
    
    print(f"[*] Report saved to: {output_file}")
    print("[*] Operation complete.")
