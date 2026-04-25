"""
Generate two quote PDFs based on DEVIS-AVALIOR style:
- Hebrew: DEVIS-MENDEL-HE.pdf
- French: DEVIS-MENDEL-FR.pdf

Includes custom scope, pricing, provider details, and 25 business days delivery.
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

# --- Fonts ---
pdfmetrics.registerFont(TTFont("Uni", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
pdfmetrics.registerFont(TTFont("UniBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

# --- Palette: close to original modern blue ---
NAVY = colors.HexColor("#0F2A4A")
BLUE = colors.HexColor("#1E5AA8")
BLUE_SOFT = colors.HexColor("#E8F0FB")
DARK = colors.HexColor("#111827")
GRAY = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#F4F6FA")
BORDER = colors.HexColor("#D1D5DB")
ACCENT = colors.HexColor("#C9A24C")

# --- User-provided business details ---
PROVIDER_NAME = "mendel cohen"
PROVIDER_PHONE = "+972587527708"
PROVIDER_EMAIL = "mendeldinacohen@gmail.com"

# --- Quotation details ---
TODAY = datetime.now()
DEVIS_NUM = f"DEV-{TODAY.strftime('%Y%m%d')}-5410"
VALIDITY_DATE = (TODAY + timedelta(days=30)).strftime("%d/%m/%Y")
DELIVERY_DAYS_TEXT_FR = "25 jours ouvrés"
DELIVERY_DAYS_TEXT_HE = "25 ימי עסקים"

ITEMS_FR = [
    ("Site vitrine responsive", "Design moderne, adaptation mobile et desktop.", 1790.00),
    ("SEO avancé", "Optimisation SEO, données structurées, sitemap, balises meta.", 990.00),
    ("Paiements Stripe", "Intégration de paiement en ligne sécurisé.", 390.00),
    ("Blog / Actualités", "Publication d'articles, catégories et tags.", 290.00),
    ("Réservation en ligne", "Formulaire de réservation intelligent avec validation.", 490.00),
    (
        "Calcul de distance (rayon 5-10 km) pour la réservation",
        "Calcul du tarif selon distance autour de la zone d'intervention.",
        330.00,
    ),
    ("Galerie photos", "Galerie de réalisations avec affichage optimisé.", 190.00),
    ("Carte de zone d'intervention", "Carte dynamique avec périmètre de service.", 150.00),
    ("Création de logo", "Proposition de logo et fichiers exportables.", 490.00),
    ("Site multilingue", "Version du site en plusieurs langues.", 390.00),
]

ITEMS_HE = [
    ("אתר תדמית רספונסיבי", "עיצוב מודרני והתאמה מלאה למובייל ודסקטופ.", 1790.00),
    ("SEO מתקדם", "אופטימיזציה למנועי חיפוש, נתונים מובנים, sitemap, מטא-תגיות.", 990.00),
    ("תשלומי Stripe", "אינטגרציה מאובטחת לתשלום אונליין.", 390.00),
    ("בלוג / חדשות", "מערכת לפרסום פוסטים, קטגוריות ותגיות.", 290.00),
    ("הזמנה אונליין", "טופס הזמנה חכם עם ולידציה ותהליך ברור.", 490.00),
    (
        "חישוב מרחק של רדיוס 5-10 ק\"מ להזמנה",
        "חישוב מחיר לפי מרחק מאזור הפעילות.",
        330.00,
    ),
    ("גלריית תמונות", "תצוגת עבודות עם תמונות אופטימליות.", 190.00),
    ("מפת אזור פעילות", "מפה דינמית להצגת אזור השירות.", 150.00),
    ("יצירת לוגו", "עיצוב לוגו וקבצי יצוא לשימוש דיגיטלי.", 490.00),
    ("אתר רב-לשוני", "תמיכה בשפות מרובות לאתר.", 390.00),
]

TOTAL = sum(p for _, _, p in ITEMS_FR)
assert TOTAL == 5500.00, f"Total mismatch: {TOTAL}"
ACOMPTE = round(TOTAL * 0.30, 2)
SOLDE = round(TOTAL - ACOMPTE, 2)


def rtl(text: str) -> str:
    return get_display(text)


def eur(amount: float) -> str:
    return f"{amount:,.2f} €".replace(",", " ").replace(".", ",")


def build_doc(filename: str, title: str, lang: str):
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=title,
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="main",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    def on_page(canvas, doc_):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(NAVY)
        canvas.rect(0, h - 7, w, 7, fill=1, stroke=0)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, 0, w, 3, fill=1, stroke=0)
        canvas.setFillColor(GRAY)
        canvas.setFont("Uni", 8)
        if lang == "he":
            footer = rtl(f"הצעת מחיר {DEVIS_NUM} | עמוד {doc_.page}")
        else:
            footer = f"Devis {DEVIS_NUM} | page {doc_.page}"
        canvas.drawCentredString(w / 2, 14, footer)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    return doc


def make_styles(hebrew: bool):
    align = TA_RIGHT if hebrew else TA_LEFT
    return {
        "title": ParagraphStyle(
            "title", fontName="UniBold", fontSize=30, leading=34, alignment=align, textColor=NAVY
        ),
        "meta": ParagraphStyle(
            "meta", fontName="Uni", fontSize=9.5, leading=13, alignment=align, textColor=GRAY
        ),
        "hblock": ParagraphStyle(
            "hblock", fontName="UniBold", fontSize=9, leading=12, alignment=align, textColor=BLUE
        ),
        "line": ParagraphStyle(
            "line", fontName="Uni", fontSize=10, leading=14, alignment=align, textColor=DARK
        ),
        "line_bold": ParagraphStyle(
            "lineb", fontName="UniBold", fontSize=10.5, leading=14, alignment=align, textColor=DARK
        ),
        "section": ParagraphStyle(
            "section",
            fontName="UniBold",
            fontSize=12.5,
            leading=16,
            alignment=align,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=6,
        ),
        "ititle": ParagraphStyle(
            "ititle", fontName="UniBold", fontSize=10, leading=13, alignment=align, textColor=DARK
        ),
        "idesc": ParagraphStyle(
            "idesc", fontName="Uni", fontSize=8.5, leading=11, alignment=align, textColor=GRAY
        ),
        "price_r": ParagraphStyle(
            "pricer", fontName="UniBold", fontSize=10.5, leading=13, alignment=TA_RIGHT, textColor=DARK
        ),
        "price_l": ParagraphStyle(
            "pricel", fontName="UniBold", fontSize=10.5, leading=13, alignment=TA_LEFT, textColor=DARK
        ),
        "white_h_r": ParagraphStyle(
            "whr", fontName="UniBold", fontSize=9, leading=12, alignment=TA_RIGHT, textColor=colors.white
        ),
        "white_h_l": ParagraphStyle(
            "whl", fontName="UniBold", fontSize=9, leading=12, alignment=TA_LEFT, textColor=colors.white
        ),
        "grand_l": ParagraphStyle(
            "gl", fontName="UniBold", fontSize=14, leading=18, alignment=TA_LEFT, textColor=colors.white
        ),
        "grand_r": ParagraphStyle(
            "gr", fontName="UniBold", fontSize=14, leading=18, alignment=TA_RIGHT, textColor=colors.white
        ),
    }


def build_french():
    s = make_styles(False)
    doc = build_doc("DEVIS-MENDEL-FR.pdf", "Devis Mendel Cohen", "fr")
    story = []

    header = Table(
        [
            [
                Paragraph("DEVIS", s["title"]),
                Paragraph(
                    f"<b>N°</b> {DEVIS_NUM}<br/>"
                    f"<b>Date :</b> {TODAY.strftime('%d/%m/%Y')}<br/>"
                    f"<b>Validité :</b> 30 jours (jusqu'au {VALIDITY_DATE})<br/>"
                    f"<b>Délai de livraison :</b> {DELIVERY_DAYS_TEXT_FR}",
                    s["meta"],
                ),
            ]
        ],
        colWidths=[8.5 * cm, 9.9 * cm],
    )
    header.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(header)

    rule = Table([[""]], colWidths=[18.4 * cm], rowHeights=[3])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY)]))
    story += [Spacer(1, 7), rule, Spacer(1, 14)]

    provider = [
        Paragraph("PRESTATAIRE", s["hblock"]),
        Paragraph(f"<b>{PROVIDER_NAME}</b>", s["line_bold"]),
        Paragraph(f"Tél : {PROVIDER_PHONE}", s["line"]),
        Paragraph(f"Email : {PROVIDER_EMAIL}", s["line"]),
    ]
    client = [
        Paragraph("DESTINATAIRE", s["hblock"]),
        Paragraph("<b>AVALIOR</b>", s["line_bold"]),
        Paragraph("Monsieur Badr Tallali", s["line"]),
        Paragraph("77bis bd Gambetta, Nice", s["line"]),
    ]
    pc = Table([[provider, client]], colWidths=[9.2 * cm, 9.2 * cm])
    pc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT),
                ("BACKGROUND", (1, 0), (1, 0), BLUE_SOFT),
                ("BOX", (0, 0), (0, 0), 0.4, BORDER),
                ("BOX", (1, 0), (1, 0), 0.4, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story += [pc, Spacer(1, 14)]

    story.append(Paragraph("OBJET DU DEVIS", s["section"]))
    story.append(
        Paragraph(
            "Création d'un site vitrine performant avec SEO avancé, paiements Stripe, blog, "
            "réservation en ligne, calcul de distance, galerie, carte de zone d'intervention, "
            "logo et version multilingue.",
            s["line"],
        )
    )
    story += [Spacer(1, 10), Paragraph("DÉTAIL DU DEVIS", s["section"])]

    rows = [[Paragraph("<b>DÉSIGNATION</b>", s["white_h_l"]), Paragraph("<b>MONTANT HT</b>", s["white_h_r"])]]
    for title, desc, price in ITEMS_FR:
        rows.append([[Paragraph(title, s["ititle"]), Paragraph(desc, s["idesc"])], Paragraph(eur(price), s["price_r"])])
    dt = Table(rows, colWidths=[14.2 * cm, 4.2 * cm])
    dt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story += [dt, Spacer(1, 10)]

    totals = Table(
        [
            [Paragraph("Total HT", s["line_bold"]), Paragraph(eur(TOTAL), s["price_r"])],
            [Paragraph("TVA (0%)", s["line_bold"]), Paragraph(eur(0), s["price_r"])],
            [Paragraph("Acompte (30%)", s["line_bold"]), Paragraph(eur(ACOMPTE), s["price_r"])],
            [Paragraph("Solde (70%)", s["line_bold"]), Paragraph(eur(SOLDE), s["price_r"])],
        ],
        colWidths=[14.2 * cm, 4.2 * cm],
    )
    totals.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.3, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(totals)

    ttc = Table(
        [[Paragraph("TOTAL TTC", s["grand_l"]), Paragraph(eur(TOTAL), s["grand_r"])]],
        colWidths=[14.2 * cm, 4.2 * cm],
    )
    ttc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story += [ttc, Spacer(1, 8), Paragraph("Moyen de paiement: virement bancaire.", s["meta"])]

    story += [PageBreak(), Paragraph(f"ACCEPTATION DU DEVIS — {DEVIS_NUM}", s["section"]), Spacer(1, 8)]
    story.append(Paragraph("Bon pour accord, date et signature:", s["line"]))
    story.append(Spacer(1, 26))
    sign = Table(
        [
            ["_________________________", "_________________________"],
            ["Signature du client", "Signature du prestataire"],
            ["Date : ____________", "Date : ____________"],
        ],
        colWidths=[9.2 * cm, 9.2 * cm],
    )
    sign.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, -1), "Uni")]))
    story.append(sign)

    doc.build(story)
    print("✔ DEVIS-MENDEL-FR.pdf")


def build_hebrew():
    s = make_styles(True)
    doc = build_doc("DEVIS-MENDEL-HE.pdf", "הצעת מחיר Mendel Cohen", "he")
    story = []

    months_he = {
        "January": "ינואר",
        "February": "פברואר",
        "March": "מרץ",
        "April": "אפריל",
        "May": "מאי",
        "June": "יוני",
        "July": "יולי",
        "August": "אוגוסט",
        "September": "ספטמבר",
        "October": "אוקטובר",
        "November": "נובמבר",
        "December": "דצמבר",
    }
    date_he = f"{TODAY.day} ב{months_he[TODAY.strftime('%B')]} {TODAY.year}"

    header = Table(
        [
            [
                Paragraph(
                    rtl(
                        f"<b>מספר:</b> {DEVIS_NUM}<br/>"
                        f"<b>תאריך:</b> {date_he}<br/>"
                        f"<b>תוקף:</b> 30 יום (עד {VALIDITY_DATE})<br/>"
                        f"<b>זמן אספקה:</b> {DELIVERY_DAYS_TEXT_HE}"
                    ),
                    s["meta"],
                ),
                Paragraph(rtl("הצעת מחיר"), s["title"]),
            ]
        ],
        colWidths=[10 * cm, 8.4 * cm],
    )
    header.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(header)

    rule = Table([[""]], colWidths=[18.4 * cm], rowHeights=[3])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY)]))
    story += [Spacer(1, 7), rule, Spacer(1, 14)]

    client = [
        Paragraph(rtl("נמען"), s["hblock"]),
        Paragraph(rtl("<b>AVALIOR</b>"), s["line_bold"]),
        Paragraph(rtl("מר Badr Tallali"), s["line"]),
        Paragraph(rtl("77bis bd Gambetta, Nice"), s["line"]),
    ]
    provider = [
        Paragraph(rtl("נותן השירות"), s["hblock"]),
        Paragraph(rtl(f"<b>{PROVIDER_NAME}</b>"), s["line_bold"]),
        Paragraph(rtl(f"טלפון: {PROVIDER_PHONE}"), s["line"]),
        Paragraph(rtl(f"אימייל: {PROVIDER_EMAIL}"), s["line"]),
    ]
    pc = Table([[provider, client]], colWidths=[9.2 * cm, 9.2 * cm])
    pc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT),
                ("BACKGROUND", (1, 0), (1, 0), BLUE_SOFT),
                ("BOX", (0, 0), (0, 0), 0.4, BORDER),
                ("BOX", (1, 0), (1, 0), 0.4, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story += [pc, Spacer(1, 14)]

    story.append(Paragraph(rtl("נושא ההצעה"), s["section"]))
    story.append(
        Paragraph(
            rtl(
                "הקמת אתר תדמית מקצועי עם SEO מתקדם, סליקת Stripe, בלוג, הזמנה אונליין, "
                "חישוב מרחק להזמנה, גלריית תמונות, מפה, לוגו ותמיכה באתר רב-לשוני."
            ),
            s["line"],
        )
    )
    story += [Spacer(1, 10), Paragraph(rtl("פירוט ההצעה"), s["section"])]

    rows = [[Paragraph(rtl("<b>סכום ללא מע\"מ</b>"), s["white_h_l"]), Paragraph(rtl("<b>פירוט</b>"), s["white_h_r"])]]
    for title, desc, price in ITEMS_HE:
        rows.append([Paragraph(eur(price), s["price_l"]), [Paragraph(rtl(title), s["ititle"]), Paragraph(rtl(desc), s["idesc"])]])
    dt = Table(rows, colWidths=[4.2 * cm, 14.2 * cm])
    dt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story += [dt, Spacer(1, 10)]

    totals = Table(
        [
            [Paragraph(eur(TOTAL), s["price_l"]), Paragraph(rtl("סה\"כ ללא מע\"מ"), s["line_bold"])],
            [Paragraph(eur(0), s["price_l"]), Paragraph(rtl("מע\"מ (0%)"), s["line_bold"])],
            [Paragraph(eur(ACOMPTE), s["price_l"]), Paragraph(rtl("מקדמה (30%)"), s["line_bold"])],
            [Paragraph(eur(SOLDE), s["price_l"]), Paragraph(rtl("יתרה (70%)"), s["line_bold"])],
        ],
        colWidths=[4.2 * cm, 14.2 * cm],
    )
    totals.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.3, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(totals)

    ttc = Table(
        [[Paragraph(eur(TOTAL), s["grand_l"]), Paragraph(rtl("סה\"כ לתשלום"), s["grand_r"])]],
        colWidths=[4.2 * cm, 14.2 * cm],
    )
    ttc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story += [ttc, Spacer(1, 8), Paragraph(rtl("אמצעי תשלום: העברה בנקאית."), s["meta"])]

    story += [PageBreak(), Paragraph(rtl(f"אישור ההצעה — {DEVIS_NUM}"), s["section"]), Spacer(1, 8)]
    story.append(Paragraph(rtl("נא לאשר בכתב יד, תאריך וחתימה:"), s["line"]))
    story.append(Spacer(1, 26))
    sign = Table(
        [
            ["_________________________", "_________________________"],
            [rtl("חתימת הלקוח"), rtl("חתימת נותן השירות")],
            [rtl("תאריך: ____________"), rtl("תאריך: ____________")],
        ],
        colWidths=[9.2 * cm, 9.2 * cm],
    )
    sign.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, -1), "Uni")]))
    story.append(sign)

    doc.build(story)
    print("✔ DEVIS-MENDEL-HE.pdf")


if __name__ == "__main__":
    build_french()
    build_hebrew()
    print(f"Total HT/TTC: {eur(TOTAL)} | Acompte: {eur(ACOMPTE)} | Solde: {eur(SOLDE)}")
