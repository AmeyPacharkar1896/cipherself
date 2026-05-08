import os
from cipher.collectors.github import GitHubCollector
from cipher.collectors.search import SearchCollector
from cipher.collectors.reddit import RedditCollector
from cipher.analyzers.personality import PersonalityAnalyzer
from cipher.analyzers.valuation import ValuationAnalyzer
from cipher.analyzers.reddit import RedditAnalyzer
from cipher.generators.pdf import PDFGenerator

def handle_scan(args, scan_parser):
    if not any([args.github, args.name, args.reddit]):
        scan_parser.error("Please provide at least one of: --github, --name, or --reddit")
        
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
    is_demo = False
    
    if gh_data and 'profile' in gh_data:
        personality_analyzer = PersonalityAnalyzer(gh_data, demo_mode=is_demo)
        personality_intel = personality_analyzer.infer()
    
    valuation_intel = {
        "richness": "Low", "google": 0.0, "meta": 0.0, "brokers": 0.0, "total": 0.0, "lifetime": 0.0, "sources": "None"
    }
    valuation_analyzer = ValuationAnalyzer(gh_data, reddit_data, demo_mode=is_demo)
    valuation_intel = valuation_analyzer.calculate()
    
    # 3. Generate Report
    print("[+] Compiling intelligence report...")
    
    sources = []
    if getattr(args, 'github', None): sources.append("github")
    if getattr(args, 'reddit', None): sources.append("reddit")
    if getattr(args, 'name', None): sources.append("name")
    
    if len(sources) == 3:
        output_subfolder = "full"
    else:
        output_subfolder = "_".join(sources)
        
    output_dir = os.path.join("outputs", output_subfolder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    gen = PDFGenerator(gh_data, subject_name, github_user, personality_intel, valuation_intel, reddit_data, reddit_intel)
    gen.filename = os.path.join(output_dir, gen.filename)
    output_file = gen.generate()
    
    print(f"[*] Report saved to: {output_file}")
    print("[*] Operation complete.")
