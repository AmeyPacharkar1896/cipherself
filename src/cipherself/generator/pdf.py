from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class PDFGenerator:
    def __init__(self, data, real_name, github_username, personality_intel, valuation_intel, reddit_data=None, reddit_intel=None):
        self.data = data
        self.real_name = real_name
        self.github_username = github_username
        self.personality_intel = personality_intel
        self.valuation_intel = valuation_intel
        self.reddit_data = reddit_data
        self.reddit_intel = reddit_intel
        self.filename = f"{real_name.replace(' ', '_')}_exposed.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
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

    def generate(self):
        doc = SimpleDocTemplate(self.filename, pagesize=LETTER)
        story = []

        # Header
        story.append(Paragraph("CLASSIFIED // SENSITIVE INTEL", self.styles['DossierHeader']))
        story.append(Paragraph(f"SUBJECT: {self.real_name.upper()}", self.styles['DossierTitle']))
        alias = self.github_username or (f"u/{self.reddit_data['username']}" if self.reddit_data else "UNKNOWN")
        story.append(Paragraph(f"ALIAS: {alias}", self.styles['DossierBase']))
        story.append(Paragraph(f"FILE CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['DossierBase']))
        story.append(Spacer(1, 0.5 * inch))

        # Section 1: SUBJECT PROFILE (GitHub focused)
        if self.data and 'profile' in self.data:
            story.append(Paragraph("SECTION 1: SUBJECT PROFILE", self.styles['DossierHeader']))
            
            profile = self.data.get('profile', {})
            activity = self.data.get('activity_stats', {})
            location = profile.get('location') or 'UNKNOWN'
            last_active = self.data.get('last_active', 'N/A')
            
            narrative = [
                f"The subject, identified as {self.real_name}, operates primarily from {location}.",
                f"Professional background indicates focus on {', '.join(self.data.get('languages', {}).keys()) or 'unspecified technologies'}.",
                f"Activity patterns show peak engagement during {self._get_peak_days(activity)} and {self._get_peak_hours(activity)}.",
                f"Digital footprint is estimated at {self.data.get('repos_count', 0)} repositories with a total star impact of {self.data.get('stars', 0)}.",
                f"Last known active signal detected on {last_active}.",
                f"Personality inferences: {self.personality_intel}"
            ]

            for p in narrative:
                story.append(Paragraph(f"> {p}", self.styles['DossierBase']))
                story.append(Spacer(1, 0.1 * inch))

        # Digital Footprint (Search focused)
        search_results = self.data.get('search_results', []) if self.data else []
        if search_results:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("DIGITAL FOOTPRINT (SEARCH RECORDS):", self.styles['DossierBase']))
            for res in search_results[:5]:
                story.append(Paragraph(f"- <u>{res['title']}</u>", self.styles['DossierBase']))
                story.append(Paragraph(f"  <i>{res['snippet']}</i>", self.styles['DossierBase']))
                story.append(Spacer(1, 0.05 * inch))

        # Section 1-B: REDDIT (Optional)
        if self.reddit_data:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph("SECTION 1-B: SOCIAL INTELLIGENCE (REDDIT)", self.styles['DossierHeader']))
            
            created_utc = self.reddit_data.get('created_utc')
            age_str = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d') if created_utc else "N/A"
            
            reddit_summary = [
                f"Subject operates on Reddit as u/{self.reddit_data['username']}.",
                f"Account created on {age_str} with a total karma impact of {self.reddit_data['total_karma']}.",
                f"Most active hour for social engagement: {self.reddit_data['most_active_hour']}:00 UTC.",
                f"Top Subreddits: {', '.join(self.reddit_data['top_subreddits'].keys())}."
            ]
            
            for s in reddit_summary:
                story.append(Paragraph(f"> {s}", self.styles['DossierBase']))
            
            if self.reddit_intel:
                story.append(Spacer(1, 0.1 * inch))
                story.append(Paragraph("SOCIAL INFERENCES:", self.styles['DossierBase']))
                for inf in self.reddit_intel:
                    story.append(Paragraph(f"- {inf}", self.styles['DossierBase']))

        story.append(PageBreak())

        # Section 2: MARKET VALUATION
        story.append(Paragraph("SECTION 2: MARKET VALUATION", self.styles['DossierHeader']))
        story.append(Paragraph("ESTIMATED DATA VALUE (MONTHLY AD REVENUE)", self.styles['DossierBase']))
        story.append(Spacer(1, 0.2 * inch))

        table_data = [
            ["PLATFORM/BROKER", "ESTIMATED VALUE"],
            ["Data Richness Score", self.valuation_intel['richness']],
            ["Sources Analyzed", self.valuation_intel.get('sources', 'N/A')],
            ["Google Ads (Search/Targeting)", f"${self.valuation_intel['google']:.2f}/mo"],
            ["Meta Ads (Demographic/Interests)", f"${self.valuation_intel['meta']:.2f}/mo"],
            ["Data Brokers (Aggregation)", f"${self.valuation_intel['brokers']:.2f}/mo"],
            ["TOTAL MONTHLY VALUE", f"${self.valuation_intel['total']:.2f}"],
            ["", ""],
            ["ESTIMATED LIFETIME VALUE", f"${self.valuation_intel['lifetime']:.2f}"]
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
            ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ]))
        story.append(t)

        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("DISCLAIMER: These figures are estimates based on industry average CPM and data broker pricing models for a technical professional demographic.", self.styles['DossierBase']))

        doc.build(story)
        return self.filename

    def _get_peak_days(self, activity):
        days = activity.get('days', {})
        if not days: return "irregular intervals"
        return sorted(days.items(), key=lambda x: x[1], reverse=True)[0][0]

    def _get_peak_hours(self, activity):
        hours = activity.get('hours', {})
        if not hours: return "variable hours"
        peak_hour = sorted(hours.items(), key=lambda x: x[1], reverse=True)[0][0]
        if 0 <= peak_hour < 6: return "early morning (late night) shifts"
        if 6 <= peak_hour < 12: return "morning sessions"
        if 12 <= peak_hour < 18: return "standard working hours"
        return "evening/night sessions"
