import argparse
import sys
import os
from datetime import datetime
from pdf2image import convert_from_path

from cipherself.config import DEMO_DATA
from cipherself.collector.github import GitHubCollector
from cipherself.collector.search import SearchCollector
from cipherself.analyzer.personality import PersonalityAnalyzer
from cipherself.analyzer.valuation import ValuationAnalyzer
from cipherself.generator.pdf import PDFGenerator

def cli():
    parser = argparse.ArgumentParser(description="cipherself - Digital Footprint Intelligence Tool")
    parser.add_argument("--github", help="GitHub username")
    parser.add_argument("--name", help="Full Name of the subject")
    parser.add_argument("--demo", action="store_true", help="Generate a demo report with fictional data")
    
    args = parser.parse_args()

    if args.demo:
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
    else:
        if not args.github or not args.name:
            parser.error("The --github and --name arguments are required when not in --demo mode.")
            
        subject_name = args.name
        github_user = args.github
        
        print(f"[*] Initiating collection for: {subject_name} (@{github_user})")
        
        # 1. Collect Data
        print("[+] Fetching GitHub intelligence...")
        gh = GitHubCollector(github_user)
        gh_data = gh.fetch_all()
        
        if not gh_data:
            print(f"[!] Error: Could not fetch data for GitHub user '{github_user}'. Check username or rate limits.")
            sys.exit(1)
            
        print("[+] Scanning public records via Google...")
        sc = SearchCollector(subject_name)
        gh_data['search_results'] = sc.fetch_top_results(limit=10)
    
    # 2. Analyze Data
    print("[+] Analyzing subject intelligence...")
    personality_analyzer = PersonalityAnalyzer(gh_data, demo_mode=args.demo)
    personality_intel = personality_analyzer.infer()
    
    valuation_analyzer = ValuationAnalyzer(gh_data, demo_mode=args.demo)
    valuation_intel = valuation_analyzer.calculate()
    
    # 3. Generate Report
    print("[+] Compiling intelligence report...")
    gen = PDFGenerator(gh_data, subject_name, github_user, personality_intel, valuation_intel)
    output_file = gen.generate()
    
    print(f"[*] Report successfully generated: {output_file}")
    
    # 4. Handle Demo Assets
    if args.demo:
        print("[+] Converting demo report to preview image...")
        if not os.path.exists("assets"):
            os.makedirs("assets")
        
        try:
            images = convert_from_path(output_file, first_page=1, last_page=1)
            if images:
                images[0].save("assets/preview.png", "PNG")
                print("[*] Preview image saved to assets/preview.png")
        except Exception as e:
            print(f"[!] Error generating preview image: {e}")

    print("[*] Operation complete.")
