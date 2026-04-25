"""
יצירת הגרסה העברית של ה-DEVIS המקורי של Miner's Hub עבור AVALIOR.

הסקריפט מתרגם את התוכן של DEVIS-AVALIOR.pdf (Canva, Bleu Moderne) לעברית
תוך שמירה על אותם פריטים, מחירים, פרטי ספק ולקוח, ועיצוב כחול־מודרני נקי.

הפלט: DEVIS-AVALIOR-MINERS-HE.pdf
"""
from datetime import datetime, timedelta

from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
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

# --- פונטים שתומכים בעברית + לטינית ---
pdfmetrics.registerFont(TTFont("Uni", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
pdfmetrics.registerFont(TTFont("UniBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

# --- צבעים: כחול מודרני, כמו המקור ---
NAVY = colors.HexColor("#0F2A4A")     # כחול עמוק לכותרות
BLUE = colors.HexColor("#1E5AA8")     # כחול מודגש
BLUE_SOFT = colors.HexColor("#E8F0FB")
GOLD = colors.HexColor("#C9A24C")     # מבטא חם עדין
DARK = colors.HexColor("#111827")
GRAY = colors.HexColor("#5B6473")
LIGHT = colors.HexColor("#F4F6FA")
BORDER = colors.HexColor("#D6DBE4")

# --- נתוני ה-DEVIS (זהים למקור) ---
DEVIS_NUM = "DEV-20260421-8400"
DEVIS_DATE = datetime(2026, 4, 21)
VALIDITY_DAYS = 30
DELIVERY_DAYS = 14

# פירוט הפריטים — כותרת בעברית, מחיר ב-€
ITEMS = [
    ("אתר תדמית רספונסיבי (כולל 4 עמודים)",
     "עמוד בית, אודות, שירותים, צור קשר. עיצוב מודרני, מותאם לנייד ולמחשב.",
     1790.00),
    ("תשלומי Stripe",
     "אינטגרציית סליקה מאובטחת לאתר (כרטיסי אשראי, SEPA).",
     190.00),
    ("בלוג / חדשות",
     "מערכת לפרסום פוסטים, קטגוריות, תגיות, ושיתוף ברשתות חברתיות.",
     290.00),
    ("SEO מתקדם",
     "אופטימיזציה למנועי חיפוש, נתונים מובנים, sitemap, מטא־תגיות.",
     990.00),
    ("הזמנה אונליין",
     "מערכת הזמנות עם יומן זמינות, אישורי הזמנה אוטומטיים במייל.",
     490.00),
    ("גלריית תמונות / פורטפוליו",
     "תצוגת עבודות עם סינון לפי קטגוריה, lightbox, אופטימיזציית תמונות.",
     190.00),
    ("מפת אזור פעילות",
     "מפה אינטראקטיבית עם אזורי שירות, נקודות עניין וכתובת העסק.",
     150.00),
    ("יצירת לוגו",
     "עיצוב לוגו מקצועי בכמה ואריאציות, כולל קבצים וקטוריים (SVG, PDF).",
     490.00),
]

# --- חישוב סכומים ---
TOTAL_HT = sum(p for _, _, p in ITEMS)        # 4580 €
TVA = 0.0
TOTAL_TTC = TOTAL_HT + TVA                    # 4580 €
ACOMPTE = round(TOTAL_TTC * 0.30, 2)          # 1374 €
SOLDE = round(TOTAL_TTC - ACOMPTE, 2)         # 3206 €

assert TOTAL_HT == 4580.00, f"סכום שגוי: {TOTAL_HT}"


def rtl(text: str) -> str:
    """המרה ל-RTL להצגה תקינה ב-reportlab."""
    return get_display(text)


def fmt_eur(value: float) -> str:
    """פורמט אירו עם פסיק עשרוני ורווח לאלפים."""
    s = f"{value:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} €"


# =======================================================================
# סגנונות
# =======================================================================
def make_styles():
    return {
        "huge": ParagraphStyle("huge", fontName="UniBold", fontSize=34, leading=38,
                               alignment=TA_LEFT, textColor=NAVY),
        "huge_right": ParagraphStyle("hugeR", fontName="UniBold", fontSize=34,
                                     leading=38, alignment=TA_RIGHT, textColor=NAVY),
        "devis_num": ParagraphStyle("dn", fontName="UniBold", fontSize=11, leading=14,
                                    alignment=TA_RIGHT, textColor=BLUE),
        "meta": ParagraphStyle("meta", fontName="Uni", fontSize=9.5, leading=13,
                               alignment=TA_LEFT, textColor=GRAY),
        "meta_right": ParagraphStyle("metaR", fontName="Uni", fontSize=9.5, leading=13,
                                     alignment=TA_RIGHT, textColor=GRAY),
        "h_block": ParagraphStyle("hb", fontName="UniBold", fontSize=8.5, leading=11,
                                  alignment=TA_RIGHT, textColor=BLUE,
                                  spaceAfter=4, letterSpacing=1),
        "h_block_left": ParagraphStyle("hbL", fontName="UniBold", fontSize=8.5,
                                       leading=11, alignment=TA_LEFT, textColor=BLUE,
                                       spaceAfter=4, letterSpacing=1),
        "block_line": ParagraphStyle("bl", fontName="Uni", fontSize=10, leading=14,
                                     alignment=TA_RIGHT, textColor=DARK),
        "block_line_left": ParagraphStyle("blL", fontName="Uni", fontSize=10,
                                          leading=14, alignment=TA_LEFT,
                                          textColor=DARK),
        "block_line_bold": ParagraphStyle("blb", fontName="UniBold", fontSize=11.5,
                                          leading=15, alignment=TA_RIGHT,
                                          textColor=NAVY),
        "block_line_bold_left": ParagraphStyle("blbL", fontName="UniBold",
                                               fontSize=11.5, leading=15,
                                               alignment=TA_LEFT, textColor=NAVY),
        "section": ParagraphStyle("sec", fontName="UniBold", fontSize=13, leading=17,
                                  alignment=TA_RIGHT, textColor=NAVY,
                                  spaceBefore=6, spaceAfter=6),
        "section_left": ParagraphStyle("secL", fontName="UniBold", fontSize=13,
                                       leading=17, alignment=TA_LEFT, textColor=NAVY,
                                       spaceBefore=6, spaceAfter=6),
        "item_title": ParagraphStyle("it", fontName="UniBold", fontSize=10.5,
                                     leading=13, alignment=TA_RIGHT, textColor=DARK),
        "item_desc": ParagraphStyle("id", fontName="Uni", fontSize=8.5, leading=11,
                                    alignment=TA_RIGHT, textColor=GRAY),
        "price": ParagraphStyle("pr", fontName="UniBold", fontSize=10.5, leading=13,
                                alignment=TA_LEFT, textColor=DARK),
        "th_right": ParagraphStyle("thR", fontName="UniBold", fontSize=9.5,
                                   leading=12, alignment=TA_RIGHT,
                                   textColor=colors.white, letterSpacing=1),
        "th_left": ParagraphStyle("thL", fontName="UniBold", fontSize=9.5,
                                  leading=12, alignment=TA_LEFT,
                                  textColor=colors.white, letterSpacing=1),
        "total_label": ParagraphStyle("tl", fontName="UniBold", fontSize=11,
                                      leading=14, alignment=TA_RIGHT, textColor=DARK),
        "total_val": ParagraphStyle("tv", fontName="UniBold", fontSize=11, leading=14,
                                    alignment=TA_LEFT, textColor=DARK),
        "grand_total": ParagraphStyle("gt", fontName="UniBold", fontSize=16,
                                      leading=20, alignment=TA_RIGHT,
                                      textColor=colors.white, letterSpacing=1),
        "grand_total_val": ParagraphStyle("gtv", fontName="UniBold", fontSize=18,
                                          leading=22, alignment=TA_LEFT,
                                          textColor=colors.white),
        "small": ParagraphStyle("sm", fontName="Uni", fontSize=8.5, leading=12,
                                alignment=TA_RIGHT, textColor=GRAY),
        "small_left": ParagraphStyle("smL", fontName="Uni", fontSize=8.5, leading=12,
                                     alignment=TA_LEFT, textColor=GRAY),
        "body": ParagraphStyle("body", fontName="Uni", fontSize=10, leading=15,
                               alignment=TA_RIGHT, textColor=DARK),
        "accept_h": ParagraphStyle("ah", fontName="UniBold", fontSize=14, leading=18,
                                   alignment=TA_CENTER, textColor=NAVY,
                                   spaceBefore=10, spaceAfter=8, letterSpacing=1),
    }


# =======================================================================
# תבנית עמוד
# =======================================================================
def build_doc(filename: str):
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="הצעת מחיר AVALIOR",
        author="MINER'S HUB",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )

    def on_page(canvas, doc_):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(NAVY)
        canvas.rect(0, h - 8, w, 8, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0, 0, w, 4, fill=1, stroke=0)

        canvas.setFont("Uni", 8)
        canvas.setFillColor(GRAY)
        footer = rtl(f"הצעת מחיר {DEVIS_NUM}   |   MINER'S HUB   |   עמוד {doc_.page}")
        canvas.drawCentredString(w / 2, 18, footer)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    return doc


# =======================================================================
# בניית התוכן
# =======================================================================
def build():
    styles = make_styles()
    doc = build_doc("DEVIS-AVALIOR-MINERS-HE.pdf")
    story = []

    # תאריכים בעברית
    months_he = {
        1: "ינואר", 2: "פברואר", 3: "מרץ", 4: "אפריל", 5: "מאי", 6: "יוני",
        7: "יולי", 8: "אוגוסט", 9: "ספטמבר", 10: "אוקטובר",
        11: "נובמבר", 12: "דצמבר",
    }
    date_he = f"{DEVIS_DATE.day} ב{months_he[DEVIS_DATE.month]} {DEVIS_DATE.year}"
    valid_until = (DEVIS_DATE + timedelta(days=VALIDITY_DAYS)).strftime("%d/%m/%Y")

    # ============ כותרת עליונה: מטה־דאטה משמאל | "הצעת מחיר" מימין ============
    header_data = [[
        Paragraph(
            f"<b>{DEVIS_NUM}</b><br/>"
            f"<b>{rtl('תאריך:')}</b> {date_he}<br/>"
            f"<b>{rtl('תוקף:')}</b> {rtl('חודש (עד')} {valid_until})<br/>"
            f"<b>{rtl('זמן אספקה:')}</b> {rtl('14 ימים')}",
            styles["meta"],
        ),
        Paragraph(rtl("הצעת מחיר"), styles["huge_right"]),
    ]]
    header_tbl = Table(header_data, colWidths=[9.8 * cm, 8 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_tbl)

    # קו הפרדה כחול
    line_tbl = Table([[""]], colWidths=[17.8 * cm], rowHeights=[3])
    line_tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY)]))
    story.append(Spacer(1, 8))
    story.append(line_tbl)
    story.append(Spacer(1, 16))

    # ============ ספק (משמאל בלטינית) | לקוח (מימין בעברית) ============
    client_block = [
        Paragraph(rtl("נמען"), styles["h_block"]),
        Paragraph(rtl("AVALIOR"), styles["block_line_bold"]),
        Paragraph(rtl("מר Badr Tallali"), styles["block_line"]),
        Paragraph(rtl("77bis bd Gambetta, Nice"), styles["block_line"]),
        Paragraph("Gregory.maiale@gmail.com", styles["block_line"]),
        Paragraph("Badrtallali@gmail.com", styles["block_line"]),
        Paragraph("+33 6 25 36 05 11", styles["block_line"]),
    ]
    provider_block = [
        Paragraph("MINER'S HUB", styles["h_block_left"]),
        Paragraph("Antoine MOURY", styles["block_line_bold_left"]),
        Paragraph("26 rue Charles de Mouchy", styles["block_line_left"]),
        Paragraph("06210 Mandelieu-la-Napoule", styles["block_line_left"]),
        Paragraph("Tel : +33 7 60 82 76 49", styles["block_line_left"]),
        Paragraph("contact@antoinemoury.fr", styles["block_line_left"]),
        Paragraph("SIRET : 913 844 619 00019  |  NAF : 6201Z", styles["small_left"]),
        Paragraph("Micro-entrepreneur — EI", styles["small_left"]),
    ]
    pc_tbl = Table([[provider_block, client_block]], colWidths=[8.9 * cm, 8.9 * cm])
    pc_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT),
        ("BACKGROUND", (1, 0), (1, 0), BLUE_SOFT),
        ("BOX", (0, 0), (0, 0), 0.5, BORDER),
        ("BOX", (1, 0), (1, 0), 0.5, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(pc_tbl)
    story.append(Spacer(1, 18))

    # ============ נושא ההצעה ============
    story.append(Paragraph(rtl("נושא ההצעה"), styles["section"]))
    story.append(Paragraph(rtl(
        "אתר תדמית עתיר ביצועים (כולל 4 עמודים) — אינטגרציית תשלומים, "
        "מערכת הזמנות, גלריה, מפה, SEO מתקדם, בלוג ויצירת לוגו."
    ), styles["body"]))
    story.append(Spacer(1, 12))

    # ============ פירוט ההצעה ============
    story.append(Paragraph(rtl("פירוט ההצעה"), styles["section"]))

    detail_rows = [[
        Paragraph(rtl("סכום ללא מע\"מ"), styles["th_left"]),
        Paragraph(rtl("פירוט"), styles["th_right"]),
    ]]
    for title, desc, price in ITEMS:
        cell = [
            Paragraph(rtl(title), styles["item_title"]),
            Paragraph(rtl(desc), styles["item_desc"]),
        ]
        detail_rows.append([
            Paragraph(fmt_eur(price), styles["price"]),
            cell,
        ])

    detail_tbl = Table(detail_rows, colWidths=[3.8 * cm, 14 * cm])
    detail_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, NAVY),
        ("LINEBELOW", (0, 1), (-1, -2), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(detail_tbl)
    story.append(Spacer(1, 10))

    # ============ סיכום סכומים ============
    total_rows = [
        [Paragraph(fmt_eur(TOTAL_HT), styles["total_val"]),
         Paragraph(rtl("סה\"כ ללא מע\"מ"), styles["total_label"])],
        [Paragraph(fmt_eur(TVA), styles["total_val"]),
         Paragraph(rtl("מע\"מ (0% — Micro-entrepreneur, art. 293 B CGI)"),
                   styles["total_label"])],
        [Paragraph(fmt_eur(ACOMPTE), styles["total_val"]),
         Paragraph(rtl("מקדמה (30%)"), styles["total_label"])],
    ]
    total_tbl = Table(total_rows, colWidths=[3.8 * cm, 14 * cm])
    total_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.3, BORDER),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(total_tbl)

    # ============ TOTAL TTC מודגש ============
    ttc_tbl = Table(
        [[Paragraph(fmt_eur(TOTAL_TTC), styles["grand_total_val"]),
          Paragraph(rtl("סה\"כ לתשלום (כולל מע\"מ)"), styles["grand_total"])]],
        colWidths=[5 * cm, 12.8 * cm],
    )
    ttc_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ttc_tbl)
    story.append(Spacer(1, 12))

    # ============ אמצעי תשלום ============
    pay_info = Table(
        [[Paragraph(rtl("העברה בנקאית"), styles["block_line"]),
          Paragraph(rtl("אמצעי תשלום:"), styles["h_block"])]],
        colWidths=[10 * cm, 7.8 * cm],
    )
    pay_info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.3, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "RIGHT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(pay_info)

    # =================================================================
    # עמוד 2 — אחסון ותחזוקה חודשית
    # =================================================================
    story.append(PageBreak())

    story.append(Paragraph(rtl("מסלול אחסון חודשי + תחזוקה"), styles["section"]))
    story.append(Spacer(1, 6))

    monthly_rows = [
        [Paragraph(rtl("69,00 € / חודש"), styles["price"]),
         Paragraph(rtl("אחסון (כולל תחזוקה חודשית)"), styles["item_title"])],
        [Paragraph(rtl("כלול"), styles["price"]),
         Paragraph(rtl("תחזוקה (כלולה במסלול האחסון)"), styles["item_title"])],
    ]
    monthly_tbl = Table(monthly_rows, colWidths=[4.5 * cm, 13.3 * cm])
    monthly_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.3, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(monthly_tbl)
    story.append(Spacer(1, 12))

    warning = Table(
        [[Paragraph(rtl(
            "<b>שימו לב:</b> סכום זה אינו כלול בסה\"כ ההצעה לעיל. "
            "החיוב החודשי יחל מתאריך מסירת האתר הסופית. "
            "ניתן לבטל בהודעה מוקדמת של 30 יום (ראו סעיף "
            "\"שירותים תקופתיים\" בתנאים הכלליים)."
        ), styles["body"])]],
        colWidths=[17.8 * cm],
    )
    warning.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E5")),
        ("BOX", (0, 0), (-1, -1), 0.3, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(warning)
    story.append(Spacer(1, 10))

    story.append(Paragraph(rtl(
        "התחזוקה החודשית כוללת 2 שינויים קטנים בחודש ותיקוני באגים."
    ), styles["body"]))
    story.append(Spacer(1, 24))

    # =================================================================
    # עמוד 3 — תנאים כלליים (תקציר)
    # =================================================================
    story.append(PageBreak())
    story.append(Paragraph(rtl(f"תנאים כלליים — {DEVIS_NUM}"), styles["section"]))
    story.append(Spacer(1, 8))

    conds = [
        ("תוקף ההצעה",
         "ההצעה בתוקף למשך 30 יום מתאריך הנפקתה."),
        ("מקדמה ותחילת עבודה",
         "תחילת העבודה מותנית בקבלת מקדמה של 30% מהסכום הכולל."),
        ("יתרת תשלום",
         "יתרת התשלום (70%) משולמת במסירת האתר הסופית."),
        ("זמן אספקה",
         "זמן האספקה המשוער הוא 14 ימים מתאריך קבלת התכנים והאישור הסופי "
         "של עיצוב הדפים."),
        ("חובת הלקוח",
         "הלקוח מתחייב לספק את כל התכנים (טקסטים, תמונות, לוגו, פרטי קשר) "
         "במועדים שיוסכמו, על מנת לעמוד בלוח הזמנים."),
        ("שינויים מחוץ להיקף",
         "כל שינוי או תוספת שאינם כלולים בהצעה זו, יתומחרו בנפרד "
         "באמצעות תוספת להסכם."),
        ("שירותים תקופתיים",
         "מסלול האחסון והתחזוקה הוא שירות חודשי מתחדש. ניתן לבטל בהודעה "
         "מוקדמת של 30 יום, בהודעה בכתב לכתובת המייל של הספק."),
        ("קניין רוחני",
         "זכויות הקוד והאתר עוברות לבעלות הלקוח לאחר ביצוע התשלום במלואו."),
        ("אחריות",
         "המעצב/המפתח אחראי לביצוע מקצועי של העבודה אך אינו אחראי "
         "לאי־זמינות הנובעת משירותים חיצוניים (Stripe, ספק אחסון, וכו')."),
        ("חוק חל",
         "ההסכם כפוף לחוקי הרפובליקה הצרפתית. בכל מחלוקת — סמכות שיפוט "
         "לבתי המשפט המוסמכים בעיר Nice."),
    ]
    for title, body in conds:
        story.append(Paragraph(rtl(f"<b>{title}.</b>"), styles["block_line_bold"]))
        story.append(Paragraph(rtl(body), styles["body"]))
        story.append(Spacer(1, 8))

    # =================================================================
    # עמוד 4 — אישור ההצעה
    # =================================================================
    story.append(PageBreak())
    story.append(Spacer(1, 30))
    story.append(Paragraph(rtl(f"אישור ההצעה — {DEVIS_NUM}"), styles["accept_h"]))
    story.append(Spacer(1, 16))

    # סיכום תשלום מודגש
    accept_rows = [
        [Paragraph(fmt_eur(ACOMPTE), styles["total_val"]),
         Paragraph(rtl("מקדמה (30%) עם החתימה"), styles["block_line_bold"])],
        [Paragraph(fmt_eur(SOLDE), styles["total_val"]),
         Paragraph(rtl("יתרה (70%) במסירה"), styles["block_line_bold"])],
        [Paragraph(fmt_eur(TOTAL_TTC), styles["grand_total_val"]),
         Paragraph(rtl("סה\"כ לתשלום"), styles["grand_total"])],
    ]
    accept_tbl = Table(accept_rows, colWidths=[5 * cm, 12.8 * cm])
    accept_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 1), BLUE_SOFT),
        ("BACKGROUND", (0, 2), (-1, 2), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.5, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.3, BLUE),
        ("LINEBELOW", (0, 1), (-1, 1), 0.3, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(accept_tbl)
    story.append(Spacer(1, 30))

    story.append(Paragraph(rtl(
        "נא לכתוב בכתב יד \"אושר וחתום\" ולחתום בצד הלקוח, "
        "תוך ציון התאריך ומקום החתימה."
    ), styles["body"]))
    story.append(Spacer(1, 36))

    sign_tbl = Table(
        [
            ["_________________________", "_________________________"],
            [rtl("חתימת נותן השירות"), rtl("חתימת הלקוח")],
            ["", ""],
            [rtl("תאריך: ____________"), rtl("תאריך: ____________")],
        ],
        colWidths=[8.9 * cm, 8.9 * cm],
    )
    sign_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Uni"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sign_tbl)

    doc.build(story)
    print("✔ DEVIS-AVALIOR-MINERS-HE.pdf")
    print(f"   סה\"כ: {fmt_eur(TOTAL_TTC)}  |  מקדמה: {fmt_eur(ACOMPTE)}  |  "
          f"יתרה: {fmt_eur(SOLDE)}")


if __name__ == "__main__":
    build()
