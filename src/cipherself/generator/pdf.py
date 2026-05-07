from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class PDFGenerator:
    def __init__(self, data, real_name, github_username, personality_intel, valuation_intel):
        self.data = data
        self.real_name = real_name
        self.github_username = github_username
        self.personality_intel = personality_intel
        self.valuation_intel = valuation_intel
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
        story.append(Paragraph(f"ALIAS: {self.github_username}", self.styles['DossierBase']))
        story.append(Paragraph(f"FILE CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['DossierBase']))
        story.append(Spacer(1, 0.5 * inch))

        # Section 1: SUBJECT PROFILE
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

        # Digital Footprint
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

        table_data = [
            ["PLATFORM/BROKER", "ESTIMATED VALUE"],
            ["Data Richness Score", self.valuation_intel['richness']],
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
            ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),
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
