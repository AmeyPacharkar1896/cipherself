BASE_RATES = {
    "google_ads": 1.50,      # USD/month base
    "meta_ads": 0.90,
    "data_brokers": 1.00,
}

GITHUB_MULTIPLIERS = {
    "has_github": 1.5,
    "stars_over_100": 1.2,
    "stars_over_1000": 1.5,
    "stars_over_10000": 2.0,
    "us_location": 1.4,
    "active_last_30_days": 1.2,
    "over_10_repos": 1.1,
}

REDDIT_MULTIPLIERS = {
    "has_reddit": 1.3,
    "karma_over_100": 1.1,
    "karma_over_1000": 1.3,
    "karma_over_10000": 1.6,
    "account_over_2_years": 1.2,
    "account_over_5_years": 1.4,
    "active_in_tech_subreddits": 1.2,
    "over_5_active_subreddits": 1.1,
}

SEARCH_MULTIPLIERS = {
    "has_public_mentions": 1.2,
    "over_5_mentions": 1.3,
}

LIFETIME_ACTIVE_YEARS = 35
