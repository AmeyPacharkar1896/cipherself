import os
from cipher.config.constants import DEMO_DATA
from cipher.generators.pdf import PDFGenerator

def handle_demo(args):
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
    
    print("[+] Analyzing subject intelligence...")
    personality_intel = "\n".join(DEMO_DATA["personality_inferences"])
    valuation_intel = DEMO_DATA["valuation"]
    
    print("[+] Compiling intelligence report...")
    output_subfolder = "demo"
            
    output_dir = os.path.join("outputs", output_subfolder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    gen = PDFGenerator(gh_data, subject_name, github_user, personality_intel, valuation_intel, reddit_data, reddit_intel)
    gen.filename = os.path.join(output_dir, gen.filename)
    output_file = gen.generate()
    
    print(f"[*] Report saved to: {output_file}")
    print("[*] Operation complete.")
