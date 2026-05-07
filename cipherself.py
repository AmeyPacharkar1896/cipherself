import argparse
import sys
from collector import GitHubCollector, SearchCollector
from generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="cipherself - Digital Footprint Intelligence Tool")
    parser.add_argument("--github", required=True, help="GitHub username")
    parser.add_argument("--name", required=True, help="Full Name of the subject")
    
    args = parser.parse_args()
    
    print(f"[*] Initiating collection for: {args.name} (@{args.github})")
    
    # 1. Collect GitHub Data
    print("[+] Fetching GitHub intelligence...")
    gh = GitHubCollector(args.github)
    gh_data = gh.fetch_all()
    
    if not gh_data:
        print(f"[!] Error: Could not fetch data for GitHub user '{args.github}'. Check username or rate limits.")
        sys.exit(1)
        
    # 2. Collect Search Data
    print("[+] Scanning public records via Google...")
    sc = SearchCollector(args.name)
    search_results = sc.fetch_top_results(limit=10)
    gh_data['search_results'] = search_results
    
    # 3. Generate Report
    print("[+] Compiling intelligence report...")
    gen = ReportGenerator(gh_data, args.name, args.github)
    output_file = gen.generate()
    
    print(f"[*] Report successfully generated: {output_file}")
    print("[*] Operation complete.")

if __name__ == "__main__":
    main()
