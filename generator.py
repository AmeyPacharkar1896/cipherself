from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class ReportGenerator:
    def __init__(self, data, real_name, github_username, demo_mode=False):
        self.data = data
        self.real_name = real_name
        self.github_username = github_username
        self.demo_mode = demo_mode
        self.filename = f"{real_name.replace(' ', '_')}_exposed.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        # Monospace style
        self.styles.add(ParagraphStyle(
            name='DossierBase',
            fontName='Courier',
            fontSize=10,
            leading=12,
            textColor=colors.black
        ))
        self.styles.add(ParagraphStyle(
            name='DossierTitle',
            parent=self.styles['DossierBase'],
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Courier-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='DossierHeader',
            parent=self.styles['DossierBase'],
            fontSize=14,
            leading=18,
            fontName='Courier-Bold',
            backColor=colors.black,
            textColor=colors.white,
            borderPadding=5,
            spaceBefore=15,
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='Redacted',
            parent=self.styles['DossierBase'],
            backColor=colors.black,
            textColor=colors.black
        ))

    def generate(self):
        doc = SimpleDocTemplate(self.filename, pagesize=LETTER)
        story = []

        # Header
        story.append(Paragraph("CLASSIFIED // SENSITIVE INTEL", self.styles['DossierHeader']))
        story.append(Paragraph(f"SUBJECT: {self.real_name.upper()}", self.styles['DossierTitle']))
        story.append(Paragraph(f"ALIAS: {self.github_username}", self.styles['DossierBase']))
        story.append(Paragraph(f"FILE CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['DossierBase']))
        story.append(Spacer(1, 0.5 * inch))

        # Section 1: SUBJECT PROFILE
        story.append(Paragraph("SECTION 1: SUBJECT PROFILE", self.styles['DossierHeader']))
        
        profile = self.data.get('profile', {})
        activity = self.data.get('activity_stats', {})
        
        # Narrative construction
        location = profile.get('location', 'UNKNOWN')
        bio = profile.get('bio', 'No official declaration provided.')
        last_active = self.data.get('last_active', 'N/A')
        
        narrative = [
            f"The subject, identified as {self.real_name}, operates primarily from {location}.",
            f"Professional background indicates focus on {', '.join(self.data.get('languages', {}).keys()) or 'unspecified technologies'}.",
            f"Activity patterns show peak engagement during {self._get_peak_days(activity)} and {self._get_peak_hours(activity)}.",
            f"Digital footprint is estimated at {self.data.get('repos_count', 0)} repositories with a total star impact of {self.data.get('stars', 0)}.",
            f"Last known active signal detected on {last_active}.",
            f"Personality inferences: {self._infer_personality()}"
        ]

        for p in narrative:
            story.append(Paragraph(f"> {p}", self.styles['DossierBase']))
            story.append(Spacer(1, 0.1 * inch))

        # Google Search Results (Public Mentions)
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("DIGITAL FOOTPRINT (SEARCH RECORDS):", self.styles['DossierBase']))
        search_results = self.data.get('search_results', [])
        for res in search_results[:5]:
            story.append(Paragraph(f"- <u>{res['title']}</u>", self.styles['DossierBase']))
            story.append(Paragraph(f"  <i>{res['snippet']}</i>", self.styles['DossierBase']))
            story.append(Spacer(1, 0.05 * inch))

        story.append(PageBreak())

        # Section 2: MARKET VALUATION
        story.append(Paragraph("SECTION 2: MARKET VALUATION", self.styles['DossierHeader']))
        story.append(Paragraph("ESTIMATED DATA VALUE (MONTHLY AD REVENUE)", self.styles['DossierBase']))
        story.append(Spacer(1, 0.2 * inch))

        valuation_data = self._calculate_valuation()
        
        table_data = [
            ["PLATFORM/BROKER", "ESTIMATED VALUE"],
            ["Data Richness Score", valuation_data['richness']],
            ["Google Ads (Search/Targeting)", f"${valuation_data['google']:.2f}/mo"],
            ["Meta Ads (Demographic/Interests)", f"${valuation_data['meta']:.2f}/mo"],
            ["Data Brokers (Aggregation)", f"${valuation_data['brokers']:.2f}/mo"],
            ["TOTAL MONTHLY VALUE", f"${valuation_data['total']:.2f}"],
            ["", ""],
            ["ESTIMATED LIFETIME VALUE", f"${valuation_data['lifetime']:.2f}"]
        ]

        t = Table(table_data, colWidths=[3.5 * inch, 2.0 * inch])
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (-1, -1), (-1, -1), 'Courier-Bold'),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.black),
            ('BACKGROUND', (0, 4), (-1, 4), colors.lightgrey),
        ]))
        story.append(t)

        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("DISCLAIMER: These figures are estimates based on industry average CPM and data broker pricing models for a technical professional demographic. Actual value may vary based on specific engagement metrics.", self.styles['DossierBase']))

        doc.build(story)
        return self.filename

    def _get_peak_days(self, activity):
        days = activity.get('days', {})
        if not days: return "irregular intervals"
        sorted_days = sorted(days.items(), key=lambda x: x[1], reverse=True)
        return sorted_days[0][0]

    def _get_peak_hours(self, activity):
        hours = activity.get('hours', {})
        if not hours: return "variable hours"
        sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)
        peak_hour = sorted_hours[0][0]
        if 0 <= peak_hour < 6: return "early morning (late night) shifts"
        if 6 <= peak_hour < 12: return "morning sessions"
        if 12 <= peak_hour < 18: return "standard working hours"
        return "evening/night sessions"

    def _infer_personality(self):
        if self.demo_mode:
            return "Systems-oriented language choices suggest preference for performance-critical problem solving. Peak Wednesday evening activity indicates side-project driven development outside work hours. Consistent contribution streak suggests disciplined long-term thinking over short bursts."
        
        profile = self.data.get('profile', {})
        languages = self.data.get('languages', {})
        activity = self.data.get('activity_stats', {})
        repos = self.data.get('repos_count', 0)
        stars = self.data.get('stars', 0)
        
        inferences = []
        
        # 1. Nocturnal Check
        hours = activity.get('hours', {})
        night_commits = sum(count for hour, count in hours.items() if 0 <= hour <= 6)
        total_commits = sum(hours.values())
        if total_commits > 0 and (night_commits / total_commits) > 0.3:
            inferences.append("Subject shows nocturnal work patterns suggesting self-directed work environment.")
        
        # 2. Systems Focus
        systems_langs = {'C', 'Rust', 'Assembly', 'C++', 'Go'}
        if any(lang in systems_langs for lang in languages):
            inferences.append("Low-level systems focus indicates preference for precision over abstraction.")
        
        # 3. Disciplined Check (Account Age)
        created_at = profile.get('created_at')
        if created_at:
            dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            years = (datetime.now() - dt).days / 365
            if years >= 10:
                inferences.append("Long-term consistent presence suggests disciplined, non-trend-driven approach to technology.")
        
        # 4. Quality Over Quantity (Stars/Repo ratio)
        if repos > 0:
            ratio = stars / repos
            if stars > 500 and ratio > 10:
                inferences.append("High community impact relative to repository count suggests quality over quantity output.")
        
        # 5. Breadth of Influence (Languages)
        if len(languages) >= 5:
            inferences.append("Broad technological stack suggests high adaptability and cross-domain competency.")
        
        # 6. Active Contributor
        last_active = self.data.get('last_active')
        if last_active:
            dt = datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%SZ")
            days_since = (datetime.now() - dt).days
            if days_since < 30 and total_commits > 50:
                inferences.append("Recent high-intensity activity indicates subject is currently engaged in high-value output cycles.")

        if not inferences:
            return "Subject maintains a focused digital presence with specific technological interests."
            
        return " ".join(inferences[:5])

    def _calculate_valuation(self):
        if self.demo_mode:
            return {
                "richness": "Medium",
                "google": 3.20,
                "meta": 1.90,
                "brokers": 2.50,
                "total": 7.60,
                "lifetime": 3192.00
            }

        profile = self.data.get('profile', {})
        repos = self.data.get('repos_count', 0)
        stars = self.data.get('stars', 0)
        search_count = len(self.data.get('search_results', []))
        location = (profile.get('location') or '').lower()
        
        # Base industry inputs
        cpm_low = 15.0
        cpm_high = 45.0
        broker_low = 0.50
        broker_high = 5.0
        
        # Multipliers
        loc_mult = 1.5 if ('united states' in location or 'usa' in location or 'us' == location) else 1.0
        
        if repos > 50 or stars > 100:
            activity_mult = 1.3 # High
            activity_level = "High"
        elif repos > 10:
            activity_mult = 1.1 # Medium
            activity_level = "Medium"
        else:
            activity_mult = 1.0 # Low
            activity_level = "Low"
            
        mention_mult = 1.0 + (min(search_count, 10) * 0.05)
        
        # Calculations
        google = (cpm_high if activity_level == "High" else cpm_low) * loc_mult * mention_mult / 10.0 # Normalized per user month
        meta = (cpm_high * 0.6 if activity_level == "High" else cpm_low * 0.6) * loc_mult * mention_mult / 10.0
        brokers = (broker_high if activity_level == "High" else broker_low) * loc_mult * mention_mult
        
        total = google + meta + brokers
        
        # Cap monthly totals at realistic ranges ($2 - $50)
        total = max(2.0, min(total, 50.0))
        
        # Lifetime Value calculation
        # Based on estimated active years online for a professional demographic (35 years)
        lifetime = total * 12 * 35
        
        # Richness Score calculation
        # Low: GitHub stars under 1000 AND fewer than 3 search results found
        # Medium: GitHub stars 1000-50000 OR 3-7 search results found
        # High: GitHub stars above 50000 OR more than 7 search results found
        
        if stars > 50000 or search_count > 7:
            richness = "High"
        elif stars >= 1000 or (3 <= search_count <= 7):
            richness = "Medium"
        else:
            richness = "Low"
        
        return {
            "google": google,
            "meta": meta,
            "brokers": brokers,
            "total": total,
            "lifetime": lifetime,
            "richness": richness
        }
