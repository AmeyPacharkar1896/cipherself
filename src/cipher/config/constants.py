from datetime import datetime

# GitHub API Configuration
GITHUB_BASE_URL = "https://api.github.com"

# Search Configuration
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="
DUCKDUCKGO_SEARCH_URL = "https://duckduckgo.com/html/?q="
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# Valuation Models (Legacy base rates)
CPM_LOW = 15.0
CPM_HIGH = 45.0
BROKER_LOW = 0.50
BROKER_HIGH = 5.0
ACTIVE_YEARS = 35

# Demo Data
DEMO_DATA = {
    "name": "Alex Mercer",
    "github_username": "alexmercer-dev",
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
    ],
    "personality_inferences": [
        "Systems-oriented language choices suggest preference for performance-critical problem solving",
        "Peak Wednesday evening activity indicates side-project driven development outside work hours",
        "Consistent contribution streak suggests disciplined long-term thinking over short bursts"
    ],
    "valuation": {
        "richness": "Medium",
        "google": 3.20,
        "meta": 1.90,
        "brokers": 2.50,
        "total": 7.60,
        "lifetime": 3192.00,
        "sources": "GitHub, Public Records"
    }
}
