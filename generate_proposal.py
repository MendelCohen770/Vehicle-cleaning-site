"""
יצירת קובץ PDF של הצעת מחיר לאתר LAVERVOTREVEHICULE.FR
"""
from datetime import datetime

from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# --- Fonts ---
pdfmetrics.registerFont(TTFont("Heb", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
pdfmetrics.registerFont(TTFont("HebBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


# --- Helpers ---
def rtl(text: str) -> str:
    """המרת טקסט עברי לסדר RTL נכון לתצוגה ב-reportlab."""
    return get_display(text)


# --- Colors (לפי פלטת הצבעים של האתר) ---
GREEN_ECO = colors.HexColor("#2E7D4F")
BLUE_AZUR = colors.HexColor("#1E6FB8")
ORANGE_CTA = colors.HexColor("#F59E0B")
DARK = colors.HexColor("#1F2937")
LIGHT_BG = colors.HexColor("#F3F4F6")
BORDER = colors.HexColor("#D1D5DB")


# --- Styles ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleHeb",
    fontName="HebBold",
    fontSize=26,
    leading=32,
    alignment=TA_RIGHT,
    textColor=GREEN_ECO,
    spaceAfter=4,
)

subtitle_style = ParagraphStyle(
    "SubtitleHeb",
    fontName="Heb",
    fontSize=13,
    leading=18,
    alignment=TA_RIGHT,
    textColor=DARK,
    spaceAfter=14,
)

h1_style = ParagraphStyle(
    "H1Heb",
    fontName="HebBold",
    fontSize=18,
    leading=24,
    alignment=TA_RIGHT,
    textColor=BLUE_AZUR,
    spaceBefore=14,
    spaceAfter=8,
)

h2_style = ParagraphStyle(
    "H2Heb",
    fontName="HebBold",
    fontSize=14,
    leading=20,
    alignment=TA_RIGHT,
    textColor=GREEN_ECO,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "BodyHeb",
    fontName="Heb",
    fontSize=11,
    leading=17,
    alignment=TA_RIGHT,
    textColor=DARK,
    spaceAfter=4,
)

bullet_style = ParagraphStyle(
    "BulletHeb",
    fontName="Heb",
    fontSize=11,
    leading=17,
    alignment=TA_RIGHT,
    textColor=DARK,
    rightIndent=14,
    spaceAfter=2,
)

small_style = ParagraphStyle(
    "SmallHeb",
    fontName="Heb",
    fontSize=9,
    leading=12,
    alignment=TA_CENTER,
    textColor=colors.grey,
)

price_total_style = ParagraphStyle(
    "PriceTotal",
    fontName="HebBold",
    fontSize=16,
    leading=22,
    alignment=TA_RIGHT,
    textColor=ORANGE_CTA,
)


def P(text, style=body_style):
    return Paragraph(rtl(text), style)


def bullet(text):
    return Paragraph(rtl(f"◄  {text}"), bullet_style)


# --- Document ---
OUTPUT = "הצעת-מחיר-LAVERVOTREVEHICULE.pdf"


def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    canvas.setFillColor(GREEN_ECO)
    canvas.rect(0, h - 12, w, 12, fill=1, stroke=0)
    canvas.setFillColor(ORANGE_CTA)
    canvas.rect(0, h - 18, w, 6, fill=1, stroke=0)

    canvas.setFillColor(GREEN_ECO)
    canvas.rect(0, 0, w, 10, fill=1, stroke=0)

    canvas.setFont("Heb", 9)
    canvas.setFillColor(colors.grey)
    footer = rtl(f"הצעת מחיר – LAVERVOTREVEHICULE.FR   |   עמוד {doc.page}")
    canvas.drawCentredString(w / 2, 16, footer)
    canvas.restoreState()


doc = BaseDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2.2 * cm,
    bottomMargin=1.8 * cm,
    title="הצעת מחיר - LAVERVOTREVEHICULE.FR",
)

frame = Frame(
    doc.leftMargin,
    doc.bottomMargin,
    doc.width,
    doc.height,
    id="normal",
)
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])

story = []

# ============ Cover / Header ============
today = datetime.now().strftime("%d/%m/%Y")

story.append(Spacer(1, 6))
story.append(P("הצעת מחיר לפיתוח אתר", title_style))
story.append(P("LAVERVOTREVEHICULE.FR — AvaLior", subtitle_style))

meta_data = [
    [P("ניקוי רכבים נייד, אקולוגי ללא מים – ניס, הריביירה הצרפתית", body_style),
     P("<b>פרטי הפרויקט:</b>", body_style)],
    [P(today, body_style),
     P("<b>תאריך:</b>", body_style)],
    [P("אתר תדמית + מערכת הזמנות ותשלומים + פאנל ניהול", body_style),
     P("<b>סוג הפרויקט:</b>", body_style)],
    [P("צרפתית (ראשית) + אנגלית", body_style),
     P("<b>שפות:</b>", body_style)],
]
meta_table = Table(meta_data, colWidths=[12.5 * cm, 4.5 * cm])
meta_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(meta_table)
story.append(Spacer(1, 10))

# ============ 1. Executive Summary ============
story.append(P("1. סקירה כללית", h1_style))
story.append(P(
    "הצעה זו מפרטת את פיתוחו של אתר מודרני, מהיר ומאובטח עבור חברת AvaLior "
    "(שם מסחרי: lavervotrevehicule). האתר ישרת את קהל היעד הצרפתי והתיירים "
    "באזור ניס והריביירה, ויכלול מערכת הזמנות מלאה, תשלומים מאובטחים, חשבוניות "
    "אוטומטיות, פאנל ניהול והתאמה מלאה לרגולציית GDPR.",
    body_style,
))
story.append(Spacer(1, 6))

# ============ 2. What's included ============
story.append(P("2. מה כלול בהצעה", h1_style))

story.append(P("א. עיצוב וחוויית משתמש (UI/UX)", h2_style))
for item in [
    "עיצוב מותאם אישית בפלטת הצבעים של המותג (ירוק אקולוגי, כחול Azur, כתום CTA)",
    "התאמה מלאה למובייל, טאבלט ודסקטופ (Mobile-First)",
    "אנימציות חלקות ותחושה פרימיום (Framer Motion)",
    "ספריית רכיבים מבוססת shadcn/ui + Tailwind CSS",
    "עיצוב לוגו טקסטואלי זמני עד לקבלת לוגו רשמי",
]:
    story.append(bullet(item))

story.append(P("ב. עמודי תוכן (4 עמודים עיקריים)", h2_style))
for item in [
    "עמוד בית (Homepage) — Hero, שירותים, מונה מים חסכוניים, איך זה עובד, המלצות",
    "עמוד ניקוי רכבי פנאי (קרוואנים / Camping-cars) עם מחירון מלא",
    "עמוד ניקוי רכבים פרטיים (Standard / Premium) עם תוספות",
    "עמוד ניקוי אופנועים (Moto)",
    "עמוד בלוג מלא עם מערכת CMS (Sanity / MDX)",
    "עמודים משפטיים: Mentions légales, CGV, RGPD, Cookies",
]:
    story.append(bullet(item))

story.append(P("ג. מערכת הזמנות חכמה (Booking System)", h2_style))
for item in [
    "3 טפסי הזמנה נפרדים (קרוואן, רכב, אופנוע) בסגנון Multi-Step",
    "חישוב מחיר דינמי בזמן אמת בהתאם לגודל, חבילה ותוספות",
    "שדה כתובת חכם עם Google Places Autocomplete",
    "חישוב מרחק אוטומטי מניס (רדיוס 5–10 ק\"מ)",
    "לוח שנה להצגת זמינות לפי אזור ושעה",
    "שליחת אישור הזמנה ותזכורת למייל הלקוח",
]:
    story.append(bullet(item))

story.append(PageBreak())

story.append(P("ד. תשלומים וחשבוניות", h2_style))
for item in [
    "אינטגרציה מלאה עם Stripe (תואם EU, SEPA, כרטיסי אשראי)",
    "בחירה בין תשלום מקדמה (10–15%) או תשלום מלא",
    "יצירת חשבונית מקדמה PDF אוטומטית עם פרטי SIRET",
    "שליחת החשבונית במייל ישירות ללקוח (Resend / SendGrid)",
    "Webhook לאישור תשלום ועדכון סטטוס הזמנה",
]:
    story.append(bullet(item))

story.append(P("ה. פאנל ניהול (Admin Panel)", h2_style))
for item in [
    "התחברות מאובטחת עם NextAuth",
    "דשבורד עם סטטיסטיקות: הזמנות, הכנסות, ליטרים שנחסכו",
    "ניהול הזמנות — צפייה, עריכה, ביטול, סימון כבוצע",
    "ניהול זמינות יומנית (ימי חופש, שעות פעילות, אזורים)",
    "ניהול מחירים, מבצעים והנחות",
    "ייצוא רשימת לקוחות לקובץ CSV",
]:
    story.append(bullet(item))

story.append(P("ו. תמיכה רב-לשונית (i18n)", h2_style))
for item in [
    "שפה ראשית: צרפתית (FR) — מלאה בכל האתר",
    "שפה משנית: אנגלית (EN) — מלאה בכל האתר",
    "מנגנון החלפת שפה דינמי (next-intl)",
    "כתובות URL ידידותיות ל-SEO לכל שפה (/fr, /en)",
]:
    story.append(bullet(item))

story.append(P("ז. SEO, ביצועים ואבטחה", h2_style))
for item in [
    "Meta tags, Open Graph, Twitter Cards לכל עמוד",
    "Sitemap.xml דינמי + Robots.txt",
    "Structured Data (JSON-LD) לסוג LocalBusiness",
    "אופטימיזציית תמונות (next/image, WebP)",
    "יעד ביצועים: ציון Lighthouse 90+ בכל הקטגוריות",
    "SSL מלא, הגנה מפני התקפות נפוצות, CAPTCHA בטפסים",
    "התאמה מלאה ל-GDPR: Cookie Banner, מדיניות פרטיות",
]:
    story.append(bullet(item))

story.append(P("ח. אנליטיקה ומדידה", h2_style))
for item in [
    "חיבור Google Analytics 4 או Plausible (ידידותי-פרטיות)",
    "חיבור Google Search Console ו-Google My Business",
    "Sentry — ניטור שגיאות בזמן אמת",
]:
    story.append(bullet(item))

story.append(PageBreak())

# ============ 3. Tech Stack ============
story.append(P("3. הטכנולוגיה שנשתמש בה", h1_style))
story.append(P(
    "הפרויקט ייבנה עם ה-Stack המודרני והמומלץ ביותר לאתרים מסוג זה, "
    "תוך דגש על ביצועים, SEO ותחזוקה קלה:",
    body_style,
))
story.append(Spacer(1, 4))

tech_data = [
    [P("<b>תיאור</b>", body_style), P("<b>טכנולוגיה</b>", body_style), P("<b>רכיב</b>", body_style)],
    [P("Framework מוביל, SSR מלא, SEO מעולה", body_style), P("Next.js 15", body_style), P("Frontend", body_style)],
    [P("בטיחות טיפוסים ופחות באגים", body_style), P("TypeScript", body_style), P("שפה", body_style)],
    [P("עיצוב מהיר, מודרני ונגיש", body_style), P("Tailwind CSS + shadcn/ui", body_style), P("עיצוב", body_style)],
    [P("מסד נתונים רלציוני מצוין", body_style), P("PostgreSQL (Supabase)", body_style), P("DB", body_style)],
    [P("תשלומים מאובטחים וחשבוניות", body_style), P("Stripe", body_style), P("תשלומים", body_style)],
    [P("חיסכון של 300 ליטר לניקוי", body_style), P("Google Maps API", body_style), P("מפות", body_style)],
    [P("פריסה מהירה וחינמית להתחלה", body_style), P("Vercel", body_style), P("Hosting", body_style)],
]
tech_table = Table(tech_data, colWidths=[8.5 * cm, 5.5 * cm, 3 * cm])
tech_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BLUE_AZUR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "HebBold"),
    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(tech_table)

# ============ 4. Pricing ============
story.append(P("4. פירוט מחירים", h1_style))
story.append(P(
    "המחירים מפורטים למודולים, כך שניתן לבחור להוציא לפועל את כולם יחד "
    "או בשלבים, לפי סדר עדיפויות התקציב והזמן.",
    body_style,
))
story.append(Spacer(1, 6))

pricing_data = [
    [P("<b>מחיר (₪)</b>", body_style), P("<b>פירוט קצר</b>", body_style), P("<b>מודול</b>", body_style)],
    [P("4,500", body_style),
     P("הקמת פרויקט, ספריית רכיבים, פלטת צבעים, responsive", body_style),
     P("1. תשתית ורכיבים משותפים", body_style)],
    [P("5,500", body_style),
     P("עמוד בית + 3 עמודי שירות (קרוואנים, רכב, אופנוע)", body_style),
     P("2. עמודי תוכן עיקריים", body_style)],
    [P("2,500", body_style),
     P("חיבור CMS, רשימת פוסטים, עמוד פוסט, קטגוריות, SEO", body_style),
     P("3. מערכת בלוג", body_style)],
    [P("8,500", body_style),
     P("3 טפסי הזמנה, חישוב מחיר דינמי, מפות, יומן זמינות", body_style),
     P("4. מערכת הזמנות מלאה", body_style)],
    [P("3,500", body_style),
     P("Stripe, חשבונית PDF, מיילים אוטומטיים, webhooks", body_style),
     P("5. תשלומים וחשבוניות", body_style)],
    [P("4,000", body_style),
     P("דשבורד, ניהול הזמנות ומחירים, ייצוא CSV", body_style),
     P("6. פאנל ניהול", body_style)],
    [P("2,000", body_style),
     P("FR + EN מלא, next-intl, כתובות URL לכל שפה", body_style),
     P("7. תמיכה ב-2 שפות", body_style)],
    [P("1,500", body_style),
     P("Mentions légales, CGV, RGPD, Cookie Banner", body_style),
     P("8. עמודים משפטיים + GDPR", body_style)],
    [P("2,000", body_style),
     P("Meta tags, Sitemap, JSON-LD, אופטימיזציית תמונות", body_style),
     P("9. SEO ואופטימיזציה", body_style)],
    [P("1,500", body_style),
     P("בדיקות על כל הדפדפנים והמכשירים, נגישות", body_style),
     P("10. בדיקות QA", body_style)],
    [P("1,000", body_style),
     P("חיבור דומיין, פריסה, Analytics, Search Console", body_style),
     P("11. השקה לאוויר", body_style)],
]
pricing_table = Table(pricing_data, colWidths=[2.8 * cm, 8 * cm, 6.2 * cm])
pricing_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GREEN_ECO),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "HebBold"),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(pricing_table)
story.append(Spacer(1, 8))

# Summary totals
totals_data = [
    [P("<b>₪ 36,500</b>", price_total_style),
     P("סך הכל (לפני מע\"מ)", body_style)],
    [P("<b>₪ 6,205</b>", body_style),
     P("מע\"מ (17%)", body_style)],
    [P("<b>₪ 42,705</b>", price_total_style),
     P("<b>סה\"כ לתשלום (כולל מע\"מ)</b>", h2_style)],
]
totals_table = Table(totals_data, colWidths=[5 * cm, 12 * cm])
totals_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
    ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#FFF7ED")),
    ("BOX", (0, 0), (-1, -1), 1, GREEN_ECO),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(totals_table)

story.append(PageBreak())

# ============ 5. Timeline ============
story.append(P("5. לוח זמנים", h1_style))
story.append(P(
    "הפרויקט כולו צפוי להסתיים תוך כ-4–5 שבועות של עבודה במשרה מלאה. "
    "להלן חלוקה משוערת לשלבים:",
    body_style,
))
story.append(Spacer(1, 4))

timeline_data = [
    [P("<b>משך</b>", body_style), P("<b>שלב</b>", body_style)],
    [P("3–5 ימים", body_style), P("הקמת תשתית, עיצוב ורכיבים משותפים", body_style)],
    [P("7–10 ימים", body_style), P("פיתוח עמודי תוכן ומערכת הבלוג", body_style)],
    [P("4–5 ימים", body_style), P("פיתוח מערכת ההזמנות (החלק המורכב ביותר)", body_style)],
    [P("2–3 ימים", body_style), P("פיתוח פאנל הניהול", body_style)],
    [P("2–3 ימים", body_style), P("עמודים משפטיים, GDPR ו-SEO", body_style)],
    [P("3 ימים", body_style), P("בדיקות QA, תיקונים והשקה לאוויר", body_style)],
    [P("<b>~4–5 שבועות</b>", body_style), P("<b>סה\"כ</b>", body_style)],
]
timeline_table = Table(timeline_data, colWidths=[4 * cm, 13 * cm])
timeline_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BLUE_AZUR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "HebBold"),
    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FFF7ED")),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(timeline_table)

# ============ 6. Payment Terms ============
story.append(P("6. תנאי תשלום", h1_style))
for item in [
    "<b>40%</b> מקדמה עם תחילת העבודה",
    "<b>30%</b> בסיום פיתוח עמודי התוכן ומערכת ההזמנות",
    "<b>30%</b> לאחר השקת האתר לאוויר וקבלת אישור סופי",
    "כל התשלומים יכולים להתבצע בהעברה בנקאית, ביט או באשראי",
    "כל ההצעה בתוקף למשך 30 יום מתאריך המסמך",
]:
    story.append(bullet(item))

# ============ 7. What's included post-launch ============
story.append(P("7. מה כלול לאחר ההשקה", h1_style))
for item in [
    "<b>חודש חופשי</b> של תמיכה מלאה ותיקון באגים ללא עלות",
    "העברת קוד מלאה ב-GitHub (Ownership של הלקוח)",
    "תיעוד מלא: איך לעדכן מחירים, להוסיף פוסטים, לנהל הזמנות",
    "הדרכה של עד שעה על פאנל הניהול (בזום)",
]:
    story.append(bullet(item))

# ============ 8. Optional Add-ons ============
story.append(P("8. תוספות אופציונליות (Add-ons)", h1_style))
addons_data = [
    [P("<b>מחיר (₪)</b>", body_style), P("<b>תוספת</b>", body_style)],
    [P("800 / חודש", body_style), P("חבילת תחזוקה חודשית (עדכונים, גיבויים, תמיכה)", body_style)],
    [P("1,500", body_style), P("עיצוב לוגו מקצועי ומדריך מותג (Brand Guidelines)", body_style)],
    [P("2,500", body_style), P("הוספת שפה שלישית (איטלקית / גרמנית)", body_style)],
    [P("2,000", body_style), P("אינטגרציית SMS ללקוחות (Twilio)", body_style)],
    [P("3,000", body_style), P("פורטל B2B ייעודי לקמפינגים וסוכנויות", body_style)],
    [P("1,500", body_style), P("מערכת ביקורות ודירוגים מובנית", body_style)],
    [P("לפי היקף", body_style), P("כתיבת תוכן שיווקי בצרפתית (Copywriter)", body_style)],
]
addons_table = Table(addons_data, colWidths=[4 * cm, 13 * cm])
addons_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ORANGE_CTA),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "HebBold"),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(addons_table)

story.append(PageBreak())

# ============ 9. What the client provides ============
story.append(P("9. מה הלקוח צריך לספק", h1_style))
for item in [
    "טקסטים שיווקיים סופיים בצרפתית (או אישור לשימוש בטקסטים שנכתבים על ידינו)",
    "תמונות מקצועיות של השירות, הרכבים והצוות (או תקציב לרכישת Stock)",
    "לוגו וזהות מותגית (אם קיימים) — אחרת נכין לוגו זמני",
    "פרטי SIRET, כתובת החברה ופרטים משפטיים לחשבוניות",
    "גישה ל-Stripe, Google (Maps + Search Console), דומיין",
    "רשימת מילות מפתח עיקריות לקידום (נוכל לעזור במחקר)",
]:
    story.append(bullet(item))

# ============ 10. Nice-to-have Future ============
story.append(P("10. תכונות לפיתוח עתידי (Phase 2)", h1_style))
story.append(P(
    "לאחר השקת האתר ותחילת הפעילות, ניתן להרחיב את המערכת בתכונות "
    "נוספות בהתאם לצמיחת העסק:",
    body_style,
))
for item in [
    "אפליקציית מובייל נלווית (React Native)",
    "הרחבה לערים נוספות (Antibes, Cannes, Monaco) עם גיאופילטרציה",
    "תוכנית נאמנות דיגיטלית עם כרטיסיות וירטואליות",
    "דשבורד ייעודי ללקוחות עסקיים",
    "Chatbot חכם מבוסס AI לתמיכה בלקוחות",
    "העלאת תמונות 'לפני ואחרי' אוטומטית עם כל הזמנה",
]:
    story.append(bullet(item))

# ============ 11. Why me ============
story.append(P("11. למה לבחור בי", h1_style))
for item in [
    "התמחות בבניית אתרים מבוססי Next.js עם דגש על ביצועים ו-SEO",
    "ניסיון באינטגרציות מורכבות (תשלומים, מפות, חשבוניות, אוטומציות)",
    "קוד נקי, מאורגן ומתועד — ניתן להמשיך לעבוד עליו בקלות גם בעתיד",
    "זמינות ותקשורת שוטפת במהלך כל הפרויקט",
    "הבנה מעמיקה של GDPR ורגולציית אתרי מסחר בצרפת",
]:
    story.append(bullet(item))

story.append(Spacer(1, 12))

# ============ Signature / Contact ============
story.append(P("12. אישור ההצעה", h1_style))
story.append(P(
    "לאישור ההצעה וקביעת פגישה ראשונה להעמקה בדרישות, ניתן לחתום למטה "
    "או להשיב במייל. לאחר האישור נתאם את תחילת העבודה ונשלח חשבונית מקדמה.",
    body_style,
))
story.append(Spacer(1, 18))

sign_data = [
    [P("_________________________", body_style), P("_________________________", body_style)],
    [P("חתימת הלקוח", body_style), P("חתימת נותן השירות", body_style)],
    [P("תאריך: ____________", body_style), P("תאריך: ____________", body_style)],
]
sign_table = Table(sign_data, colWidths=[8.5 * cm, 8.5 * cm])
sign_table.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(sign_table)

story.append(Spacer(1, 20))
story.append(P(
    "תודה על ההזדמנות — נשמח להעניק לעסק אתר שמייצג אותו בדיוק כפי שהוא ראוי.",
    ParagraphStyle(
        "Thanks",
        fontName="HebBold",
        fontSize=12,
        alignment=TA_CENTER,
        textColor=GREEN_ECO,
    ),
))

# ============ Build ============
doc.build(story)
print(f"✔ PDF נוצר: {OUTPUT}")
