"""
יצירת 2 קבצי DEVIS (הצעת מחיר רשמית) עבור AVALIOR:
  - גרסה צרפתית (DEVIS-AVALIOR-FR.pdf)
  - גרסה עברית (DEVIS-AVALIOR-HE.pdf)

הסגנון מבוסס על ה-DEVIS המקורי של Miner's Hub: פריסה נקייה,
בלוקים של פרטי לקוח/ספק, טבלת פריטים, סיכום מחירים וסעיפי
אישור בתחתית.
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

# --- Colors (שומרים על זהות המותג) ---
DARK = colors.HexColor("#111827")
GRAY = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#F3F4F6")
BORDER = colors.HexColor("#D1D5DB")
ACCENT = colors.HexColor("#2E7D4F")  # ירוק אקולוגי
ACCENT_SOFT = colors.HexColor("#E8F5EE")
ORANGE = colors.HexColor("#F59E0B")


def rtl(t: str) -> str:
    return get_display(t)


# =======================================================================
# תבנית משותפת
# =======================================================================
def build_doc(filename: str, title: str, lang: str = "fr"):
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=title,
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )

    def on_page(canvas, doc_):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(ACCENT)
        canvas.rect(0, h - 6, w, 6, fill=1, stroke=0)
        canvas.setFillColor(ORANGE)
        canvas.rect(0, 0, w, 4, fill=1, stroke=0)

        canvas.setFont("Uni", 8)
        canvas.setFillColor(GRAY)
        if lang == "he":
            footer = rtl(f"הצעת מחיר – AVALIOR   |   עמוד {doc_.page}")
        else:
            footer = f"DEVIS – AVALIOR   |   page {doc_.page}"
        canvas.drawCentredString(w / 2, 14, footer)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    return doc


# =======================================================================
# סגנונות (ניצור סט לכל שפה)
# =======================================================================
def make_styles(align_right: bool):
    """
    align_right=True  -> עברית (RTL)
    align_right=False -> צרפתית (LTR)
    """
    default_align = TA_RIGHT if align_right else TA_LEFT

    return {
        "huge": ParagraphStyle("huge", fontName="UniBold", fontSize=28, leading=32,
                               alignment=default_align, textColor=DARK),
        "devis_num": ParagraphStyle("dn", fontName="UniBold", fontSize=11, leading=14,
                                    alignment=default_align, textColor=ACCENT),
        "meta": ParagraphStyle("meta", fontName="Uni", fontSize=9, leading=12,
                               alignment=default_align, textColor=GRAY),
        "h_block": ParagraphStyle("hb", fontName="UniBold", fontSize=9, leading=12,
                                  alignment=default_align, textColor=GRAY,
                                  spaceAfter=4),
        "block_line": ParagraphStyle("bl", fontName="Uni", fontSize=10, leading=14,
                                     alignment=default_align, textColor=DARK),
        "block_line_bold": ParagraphStyle("blb", fontName="UniBold", fontSize=10.5,
                                          leading=14, alignment=default_align,
                                          textColor=DARK),
        "section": ParagraphStyle("sec", fontName="UniBold", fontSize=12, leading=16,
                                  alignment=default_align, textColor=ACCENT,
                                  spaceBefore=6, spaceAfter=6),
        "item_title": ParagraphStyle("it", fontName="UniBold", fontSize=10, leading=13,
                                     alignment=default_align, textColor=DARK),
        "item_desc": ParagraphStyle("id", fontName="Uni", fontSize=8.5, leading=11,
                                    alignment=default_align, textColor=GRAY),
        "price": ParagraphStyle("pr", fontName="UniBold", fontSize=10.5, leading=13,
                                alignment=TA_RIGHT, textColor=DARK),
        "total_label": ParagraphStyle("tl", fontName="UniBold", fontSize=11, leading=14,
                                      alignment=default_align, textColor=DARK),
        "total_val": ParagraphStyle("tv", fontName="UniBold", fontSize=11, leading=14,
                                    alignment=TA_RIGHT, textColor=DARK),
        "grand_total": ParagraphStyle("gt", fontName="UniBold", fontSize=14, leading=18,
                                      alignment=default_align, textColor=colors.white),
        "grand_total_val": ParagraphStyle("gtv", fontName="UniBold", fontSize=14,
                                          leading=18, alignment=TA_RIGHT,
                                          textColor=colors.white),
        "small": ParagraphStyle("sm", fontName="Uni", fontSize=8.5, leading=12,
                                alignment=default_align, textColor=GRAY),
        "body": ParagraphStyle("body", fontName="Uni", fontSize=9.5, leading=14,
                               alignment=default_align, textColor=DARK),
        "accept_h": ParagraphStyle("ah", fontName="UniBold", fontSize=13, leading=17,
                                   alignment=TA_CENTER, textColor=ACCENT,
                                   spaceBefore=10, spaceAfter=8),
    }


# =======================================================================
# נתוני הצעה (זהים לשתי הגרסאות)
# =======================================================================
today = datetime.now()
devis_num = f"DEV-{today.strftime('%Y%m%d')}-5500"
validity_date = (today + timedelta(days=30)).strftime("%d/%m/%Y")

# פירוט המודולים — אותם פריטים, מתורגמים
ITEMS_FR = [
    ("Site vitrine premium — 4 pages + pages légales",
     "Next.js 15, TypeScript, Tailwind + shadcn/ui, 100% responsive, animations Framer Motion. "
     "Accueil, Véhicules de loisir, Voiture, Moto + Mentions légales, CGV, RGPD, Cookies.",
     1990.00),
    ("Système de réservation avancé",
     "3 formulaires multi-étapes (camping-car, voiture, moto), calcul de prix dynamique, "
     "Google Places Autocomplete, calcul de distance (rayon 5–10 km de Nice), calendrier "
     "de disponibilités, choix acompte ou paiement intégral.",
     990.00),
    ("Paiement Stripe + factures d'acompte PDF",
     "Stripe Checkout (cartes, SEPA), webhooks, génération automatique de factures d'acompte "
     "au format PDF, envoi par email au client (Resend).",
     490.00),
    ("Espace administrateur (Back-office)",
     "Connexion sécurisée (NextAuth), tableau de bord avec statistiques, gestion des "
     "réservations, gestion du calendrier de disponibilités, gestion des tarifs et promotions, "
     "export CSV des clients.",
     790.00),
    ("Blog / Actualités avec CMS",
     "Intégration Sanity ou MDX, liste d'articles, pagination, catégories, SEO dynamique, "
     "partage sur réseaux sociaux.",
     270.00),
    ("Site multilingue FR / EN",
     "next-intl, URLs dédiées (/fr, /en), sélecteur de langue, traduction complète de toutes "
     "les pages et formulaires.",
     390.00),
    ("SEO avancé + Données structurées",
     "Meta tags optimisés, Open Graph, sitemap.xml dynamique, robots.txt, JSON-LD "
     "LocalBusiness, optimisation images (WebP), objectif Lighthouse 90+, intégration "
     "Google Search Console et Google My Business.",
     390.00),
    ("Conformité RGPD + sécurité",
     "Cookie Banner conforme GDPR, reCAPTCHA sur formulaires, SSL, monitoring d'erreurs "
     "(Sentry), textes légaux rédigés.",
     190.00),
    ("Tests, QA & mise en ligne",
     "Tests multi-navigateurs (Chrome/Safari/Firefox), tests mobile (iOS/Android), "
     "accessibilité, connexion du domaine, déploiement Vercel, Analytics, formation de 1h.",
     ["inclus", "inclus", "inclus"][0]),  # 0.00
    ("Création de logo textuel + charte couleurs",
     "Logo provisoire textuel et définition de la palette (vert éco, bleu Azur, orange CTA) "
     "dans l'attente du logo définitif.",
     "inclus"),
]

ITEMS_HE = [
    ("אתר תדמית פרמיום — 4 עמודים + עמודים משפטיים",
     "Next.js 15, TypeScript, Tailwind + shadcn/ui, רספונסיבי מלא, אנימציות Framer Motion. "
     "עמוד בית, קרוואנים, רכבים, אופנועים + Mentions légales, CGV, RGPD, Cookies.",
     1990.00),
    ("מערכת הזמנות מתקדמת",
     "3 טפסי Multi-Step נפרדים (קרוואן, רכב, אופנוע), חישוב מחיר דינמי, Google Places "
     "Autocomplete, חישוב מרחק (רדיוס 5–10 ק\"מ מניס), יומן זמינות, בחירה בין מקדמה "
     "לתשלום מלא.",
     990.00),
    ("תשלומי Stripe + חשבוניות מקדמה PDF",
     "Stripe Checkout (אשראי, SEPA), webhooks, יצירה אוטומטית של חשבוניות מקדמה "
     "בפורמט PDF, שליחה במייל ללקוח (Resend).",
     490.00),
    ("פאנל ניהול (Back-office)",
     "התחברות מאובטחת (NextAuth), דשבורד עם סטטיסטיקות, ניהול הזמנות, ניהול יומן "
     "זמינות, ניהול מחירים ומבצעים, ייצוא לקוחות ל-CSV.",
     790.00),
    ("בלוג / חדשות עם CMS",
     "אינטגרציית Sanity או MDX, רשימת פוסטים, pagination, קטגוריות, SEO דינמי, "
     "שיתוף ברשתות חברתיות.",
     270.00),
    ("אתר רב-לשוני FR / EN",
     "next-intl, כתובות ייעודיות (/fr, /en), בורר שפה, תרגום מלא של כל העמודים והטפסים.",
     390.00),
    ("SEO מתקדם + נתונים מובנים",
     "Meta tags מותאמים, Open Graph, sitemap.xml דינמי, robots.txt, JSON-LD LocalBusiness, "
     "אופטימיזציית תמונות (WebP), יעד Lighthouse 90+, חיבור Google Search Console "
     "ו-Google My Business.",
     390.00),
    ("תאימות GDPR + אבטחה",
     "Cookie Banner תואם GDPR, reCAPTCHA בטפסים, SSL, ניטור שגיאות (Sentry), טקסטים "
     "משפטיים כתובים.",
     190.00),
    ("בדיקות QA והעלאה לאוויר",
     "בדיקות רב-דפדפניות (Chrome/Safari/Firefox), בדיקות מובייל (iOS/Android), נגישות, "
     "חיבור דומיין, פריסה ל-Vercel, Analytics, הדרכה של שעה.",
     "כלול"),
    ("יצירת לוגו טקסטואלי + מדריך צבעים",
     "לוגו זמני טקסטואלי והגדרת פלטת הצבעים (ירוק אקולוגי, כחול Azur, כתום CTA) עד "
     "לקבלת לוגו סופי.",
     "כלול"),
]

# בדיקת סכום (סה\"כ = 5500)
total_check = sum(x[2] for x in ITEMS_FR if isinstance(x[2], (int, float)))
assert total_check == 5500.00, f"סכום לא מסתכם ל-5500: {total_check}"


# =======================================================================
# גרסה צרפתית
# =======================================================================
def build_french():
    styles = make_styles(align_right=False)
    doc = build_doc("DEVIS-AVALIOR-FR.pdf", "Devis AVALIOR", lang="fr")
    story = []

    # --- כותרת עליונה: DEVIS | מספר | תאריכים ---
    header_data = [[
        Paragraph("DEVIS", styles["huge"]),
        Paragraph(
            f"<b>N°</b> {devis_num}<br/>"
            f"<b>Date :</b> {today.strftime('%d %B %Y').replace(today.strftime('%B'), {'January':'janvier','February':'février','March':'mars','April':'avril','May':'mai','June':'juin','July':'juillet','August':'août','September':'septembre','October':'octobre','November':'novembre','December':'décembre'}[today.strftime('%B')])}<br/>"
            f"<b>Validité :</b> 30 jours (jusqu'au {validity_date})<br/>"
            f"<b>Délai de livraison :</b> 4 à 5 semaines",
            styles["meta"],
        ),
    ]]
    header_tbl = Table(header_data, colWidths=[8 * cm, 9.8 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_tbl)

    # קו הפרדה בצבע
    line_tbl = Table([[""]], colWidths=[17.8 * cm], rowHeights=[3])
    line_tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    story.append(Spacer(1, 6))
    story.append(line_tbl)
    story.append(Spacer(1, 14))

    # --- Provider | Client ---
    provider_block = [
        Paragraph("PRESTATAIRE", styles["h_block"]),
        Paragraph("<b>[Votre nom / entreprise]</b>", styles["block_line_bold"]),
        Paragraph("Développement Web — Freelance", styles["block_line"]),
        Paragraph("Email : [votre.email@example.com]", styles["block_line"]),
        Paragraph("Tél : [+33 / +972 ...]", styles["block_line"]),
        Paragraph("SIRET / N° entreprise : [à compléter]", styles["small"]),
    ]
    client_block = [
        Paragraph("DESTINATAIRE", styles["h_block"]),
        Paragraph("<b>AVALIOR</b>", styles["block_line_bold"]),
        Paragraph("Monsieur Badr Tallali", styles["block_line"]),
        Paragraph("77bis bd Gambetta, Nice", styles["block_line"]),
        Paragraph("Gregory.maiale@gmail.com", styles["block_line"]),
        Paragraph("Badrtallali@gmail.com", styles["block_line"]),
        Paragraph("+33 6 25 36 05 11", styles["block_line"]),
    ]
    pc_tbl = Table([[provider_block, client_block]], colWidths=[8.9 * cm, 8.9 * cm])
    pc_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT),
        ("BACKGROUND", (1, 0), (1, 0), ACCENT_SOFT),
        ("BOX", (0, 0), (0, 0), 0.5, BORDER),
        ("BOX", (1, 0), (1, 0), 0.5, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(pc_tbl)
    story.append(Spacer(1, 16))

    # --- Project summary ---
    story.append(Paragraph("OBJET DU DEVIS", styles["section"]))
    story.append(Paragraph(
        "Développement complet du site <b>lavervotrevehicule.fr</b> — application web "
        "sur-mesure pour AvaLior : site vitrine premium, système de réservation avancé, "
        "paiements Stripe, facturation automatique, espace administrateur et conformité RGPD. "
        "Le site sera disponible en français et en anglais.",
        styles["body"],
    ))
    story.append(Spacer(1, 10))

    # --- DETAIL ---
    story.append(Paragraph("DÉTAIL DU DEVIS", styles["section"]))

    detail_rows = [[
        Paragraph("<b>DÉSIGNATION</b>", styles["item_title"]),
        Paragraph("<b>MONTANT HT</b>", ParagraphStyle(
            "hdr", parent=styles["item_title"], alignment=TA_RIGHT)),
    ]]
    for title, desc, price in ITEMS_FR:
        if isinstance(price, (int, float)):
            price_str = "inclus" if price == 0 else f"{price:,.2f} €".replace(",", " ")
        else:
            price_str = price
        cell = [
            Paragraph(title, styles["item_title"]),
            Paragraph(desc, styles["item_desc"]),
        ]
        detail_rows.append([cell, Paragraph(price_str, styles["price"])])

    detail_tbl = Table(detail_rows, colWidths=[13.8 * cm, 4 * cm])
    detail_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "UniBold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(detail_tbl)
    story.append(Spacer(1, 10))

    # --- Totals ---
    total_rows = [
        [Paragraph("Total HT", styles["total_label"]),
         Paragraph("5 500,00 €", styles["total_val"])],
        [Paragraph("TVA (0% — micro-entrepreneur, art. 293 B CGI)",
                   styles["total_label"]),
         Paragraph("0,00 €", styles["total_val"])],
    ]
    total_tbl = Table(total_rows, colWidths=[13.8 * cm, 4 * cm])
    total_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.3, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(total_tbl)

    # TTC highlight
    ttc_tbl = Table(
        [[Paragraph("TOTAL TTC", styles["grand_total"]),
          Paragraph("5 500,00 €", styles["grand_total_val"])]],
        colWidths=[13.8 * cm, 4 * cm],
    )
    ttc_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ttc_tbl)
    story.append(Spacer(1, 10))

    # --- Payment terms ---
    pay_rows = [
        [Paragraph("<b>Acompte à la signature (30%)</b>", styles["block_line_bold"]),
         Paragraph("1 650,00 €", styles["price"])],
        [Paragraph("<b>Solde à la livraison (70%)</b>", styles["block_line_bold"]),
         Paragraph("3 850,00 €", styles["price"])],
    ]
    pay_tbl = Table(pay_rows, colWidths=[13.8 * cm, 4 * cm])
    pay_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.3, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(pay_tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Moyens de paiement acceptés :</b> virement bancaire, Stripe, PayPal.",
        styles["small"]))

    story.append(PageBreak())

    # ==================== עמוד 2: אופציות וחתימה ====================
    story.append(Paragraph("OPTIONS COMPLÉMENTAIRES (hors devis)", styles["section"]))
    options_data = [
        [Paragraph("<b>Option</b>", styles["item_title"]),
         Paragraph("<b>Prix</b>", ParagraphStyle("h", parent=styles["item_title"], alignment=TA_RIGHT))],
        [Paragraph("Hébergement + maintenance mensuelle (2 modifs + corrections de bugs)",
                   styles["item_desc"]),
         Paragraph("59 € / mois", styles["price"])],
        [Paragraph("Création de logo professionnel + charte graphique complète",
                   styles["item_desc"]),
         Paragraph("390,00 €", styles["price"])],
        [Paragraph("Ajout d'une 3e langue (italien ou allemand)", styles["item_desc"]),
         Paragraph("490,00 €", styles["price"])],
        [Paragraph("Notifications SMS clients (Twilio)", styles["item_desc"]),
         Paragraph("390,00 €", styles["price"])],
        [Paragraph("Portail B2B dédié (campings, concessionnaires)", styles["item_desc"]),
         Paragraph("690,00 €", styles["price"])],
        [Paragraph("Rédaction de contenu marketing en français (copywriter)",
                   styles["item_desc"]),
         Paragraph("sur devis", styles["price"])],
    ]
    opt_tbl = Table(options_data, colWidths=[13.8 * cm, 4 * cm])
    opt_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "UniBold"),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(opt_tbl)
    story.append(Spacer(1, 14))

    # --- Included post-launch ---
    story.append(Paragraph("INCLUS APRÈS LIVRAISON", styles["section"]))
    included = [
        "1 mois de support technique gratuit après la mise en ligne",
        "Transfert complet du code sur GitHub (propriété totale du client)",
        "Documentation complète pour mettre à jour les tarifs, publier des articles, gérer les réservations",
        "Formation de 1h sur le back-office (en visioconférence)",
    ]
    for item in included:
        story.append(Paragraph(f"•  {item}", styles["body"]))
    story.append(Spacer(1, 14))

    # --- Conditions générales résumé ---
    story.append(Paragraph("CONDITIONS PRINCIPALES", styles["section"]))
    conds = [
        "Devis valable 30 jours à compter de la date d'émission.",
        "L'acompte de 30% est exigé pour démarrer les travaux.",
        "Le solde est payable à la livraison finale du site.",
        "Le client s'engage à fournir les contenus (textes, photos) dans les délais convenus.",
        "La propriété intellectuelle du code est transférée au client après paiement intégral.",
        "Toute modification hors périmètre fera l'objet d'un avenant.",
    ]
    for c in conds:
        story.append(Paragraph(f"•  {c}", styles["body"]))
    story.append(Spacer(1, 18))

    # --- Acceptance ---
    story.append(Paragraph(f"ACCEPTATION DU DEVIS — {devis_num}", styles["accept_h"]))
    story.append(Paragraph(
        "Bon pour accord. Mention manuscrite « Bon pour accord » requise, suivie de la "
        "date et de la signature.",
        styles["body"],
    ))
    story.append(Spacer(1, 24))

    sign_tbl = Table(
        [
            ["_________________________", "_________________________"],
            ["Signature du client", "Signature du prestataire"],
            ["Date : ____________", "Date : ____________"],
        ],
        colWidths=[8.9 * cm, 8.9 * cm],
    )
    sign_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Uni"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sign_tbl)

    doc.build(story)
    print("✔ DEVIS-AVALIOR-FR.pdf")


# =======================================================================
# גרסה עברית
# =======================================================================
def build_hebrew():
    styles = make_styles(align_right=True)
    doc = build_doc("DEVIS-AVALIOR-HE.pdf", "הצעת מחיר AVALIOR", lang="he")
    story = []

    months_he = {
        "January": "ינואר", "February": "פברואר", "March": "מרץ", "April": "אפריל",
        "May": "מאי", "June": "יוני", "July": "יולי", "August": "אוגוסט",
        "September": "ספטמבר", "October": "אוקטובר", "November": "נובמבר",
        "December": "דצמבר",
    }
    date_he = f"{today.day} ב{months_he[today.strftime('%B')]} {today.year}"

    # --- כותרת עליונה ---
    header_data = [[
        Paragraph(rtl(
            f"<b>מספר:</b> {devis_num}<br/>"
            f"<b>תאריך:</b> {date_he}<br/>"
            f"<b>תוקף:</b> 30 יום (עד {validity_date})<br/>"
            f"<b>זמן אספקה:</b> 4–5 שבועות"
        ), styles["meta"]),
        Paragraph(rtl("הצעת מחיר"), styles["huge"]),
    ]]
    header_tbl = Table(header_data, colWidths=[9.8 * cm, 8 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_tbl)

    line_tbl = Table([[""]], colWidths=[17.8 * cm], rowHeights=[3])
    line_tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    story.append(Spacer(1, 6))
    story.append(line_tbl)
    story.append(Spacer(1, 14))

    # --- Client | Provider (RTL order: לקוח בצד ימין) ---
    client_block = [
        Paragraph(rtl("נמען"), styles["h_block"]),
        Paragraph(rtl("<b>AVALIOR</b>"), styles["block_line_bold"]),
        Paragraph(rtl("מר Badr Tallali"), styles["block_line"]),
        Paragraph(rtl("77bis bd Gambetta, Nice"), styles["block_line"]),
        Paragraph("Gregory.maiale@gmail.com", styles["block_line"]),
        Paragraph("Badrtallali@gmail.com", styles["block_line"]),
        Paragraph("+33 6 25 36 05 11", styles["block_line"]),
    ]
    provider_block = [
        Paragraph(rtl("נותן השירות"), styles["h_block"]),
        Paragraph(rtl("<b>[השם / שם העסק שלך]</b>"), styles["block_line_bold"]),
        Paragraph(rtl("פיתוח אתרים — פרילנס"), styles["block_line"]),
        Paragraph(rtl("אימייל: [your.email@example.com]"), styles["block_line"]),
        Paragraph(rtl("טלפון: [+972 ...]"), styles["block_line"]),
        Paragraph(rtl("ח.פ / עוסק מורשה: [למלא]"), styles["small"]),
    ]
    pc_tbl = Table([[provider_block, client_block]], colWidths=[8.9 * cm, 8.9 * cm])
    pc_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT),
        ("BACKGROUND", (1, 0), (1, 0), ACCENT_SOFT),
        ("BOX", (0, 0), (0, 0), 0.5, BORDER),
        ("BOX", (1, 0), (1, 0), 0.5, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(pc_tbl)
    story.append(Spacer(1, 16))

    # --- Project summary ---
    story.append(Paragraph(rtl("נושא ההצעה"), styles["section"]))
    story.append(Paragraph(rtl(
        "פיתוח מלא של אתר <b>lavervotrevehicule.fr</b> — אפליקציית Web מותאמת אישית "
        "עבור AvaLior: אתר תדמית פרמיום, מערכת הזמנות מתקדמת, תשלומי Stripe, "
        "הפקת חשבוניות אוטומטית, פאנל ניהול ותאימות מלאה ל-GDPR. האתר יהיה זמין "
        "בצרפתית ובאנגלית."
    ), styles["body"]))
    story.append(Spacer(1, 10))

    # --- DETAIL ---
    story.append(Paragraph(rtl("פירוט ההצעה"), styles["section"]))

    detail_rows = [[
        Paragraph(rtl("<b>סכום (לא כולל מע\"מ)</b>"), ParagraphStyle(
            "h", parent=styles["item_title"], alignment=TA_RIGHT)),
        Paragraph(rtl("<b>תיאור</b>"), styles["item_title"]),
    ]]
    for title, desc, price in ITEMS_HE:
        if isinstance(price, (int, float)):
            price_str = "כלול" if price == 0 else f"{price:,.2f} €".replace(",", " ")
            price_disp = rtl(price_str) if not price_str.endswith("€") else price_str
        else:
            price_str = price
            price_disp = rtl(price_str)
        cell = [
            Paragraph(rtl(title), styles["item_title"]),
            Paragraph(rtl(desc), styles["item_desc"]),
        ]
        detail_rows.append([Paragraph(price_disp, styles["price"]), cell])

    detail_tbl = Table(detail_rows, colWidths=[4 * cm, 13.8 * cm])
    detail_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "UniBold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(detail_tbl)
    story.append(Spacer(1, 10))

    # --- Totals ---
    total_rows = [
        [Paragraph("5 500,00 €", styles["total_val"]),
         Paragraph(rtl("סה\"כ ללא מע\"מ"), styles["total_label"])],
        [Paragraph("0,00 €", styles["total_val"]),
         Paragraph(rtl("מע\"מ (0% — משטר Micro-entrepreneur, סעיף 293 B CGI)"),
                   styles["total_label"])],
    ]
    total_tbl = Table(total_rows, colWidths=[4 * cm, 13.8 * cm])
    total_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.3, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(total_tbl)

    ttc_tbl = Table(
        [[Paragraph("5 500,00 €", styles["grand_total_val"]),
          Paragraph(rtl("סה\"כ לתשלום"), styles["grand_total"])]],
        colWidths=[4 * cm, 13.8 * cm],
    )
    ttc_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ttc_tbl)
    story.append(Spacer(1, 10))

    # --- Payment terms ---
    pay_rows = [
        [Paragraph("1 650,00 €", styles["price"]),
         Paragraph(rtl("<b>מקדמה עם החתימה (30%)</b>"), styles["block_line_bold"])],
        [Paragraph("3 850,00 €", styles["price"]),
         Paragraph(rtl("<b>יתרה בסיום הפרויקט (70%)</b>"), styles["block_line_bold"])],
    ]
    pay_tbl = Table(pay_rows, colWidths=[4 * cm, 13.8 * cm])
    pay_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.3, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(pay_tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        rtl("<b>אמצעי תשלום מקובלים:</b> העברה בנקאית, Stripe, PayPal, ביט."),
        styles["small"]))

    story.append(PageBreak())

    # ==================== עמוד 2 ====================
    story.append(Paragraph(rtl("אופציות נוספות (לא כלולות בהצעה)"), styles["section"]))
    opt_items = [
        ("אחסון + תחזוקה חודשית (2 עדכונים + תיקון באגים)", "59 € / חודש"),
        ("יצירת לוגו מקצועי + מדריך מותג מלא", "390,00 €"),
        ("הוספת שפה שלישית (איטלקית או גרמנית)", "490,00 €"),
        ("התראות SMS ללקוחות (Twilio)", "390,00 €"),
        ("פורטל B2B ייעודי (קמפינגים, סוכנויות)", "690,00 €"),
        ("כתיבת תוכן שיווקי בצרפתית (Copywriter)", "לפי היקף"),
    ]
    opt_rows = [[
        Paragraph(rtl("<b>מחיר</b>"), ParagraphStyle(
            "h", parent=styles["item_title"], alignment=TA_RIGHT)),
        Paragraph(rtl("<b>אופציה</b>"), styles["item_title"]),
    ]]
    for name, price in opt_items:
        opt_rows.append([
            Paragraph(rtl(price), styles["price"]),
            Paragraph(rtl(name), styles["item_desc"]),
        ])
    opt_tbl = Table(opt_rows, colWidths=[4 * cm, 13.8 * cm])
    opt_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "UniBold"),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(opt_tbl)
    story.append(Spacer(1, 14))

    # --- Included post-launch ---
    story.append(Paragraph(rtl("כלול לאחר השקת האתר"), styles["section"]))
    included = [
        "חודש של תמיכה טכנית חינם לאחר ההשקה",
        "העברת קוד מלאה ב-GitHub (בעלות מלאה של הלקוח)",
        "תיעוד מלא לעדכון מחירים, פרסום פוסטים וניהול הזמנות",
        "הדרכה של שעה על הפאנל הניהולי (בזום)",
    ]
    for item in included:
        story.append(Paragraph(rtl(f"•  {item}"), styles["body"]))
    story.append(Spacer(1, 14))

    # --- Conditions ---
    story.append(Paragraph(rtl("תנאים עיקריים"), styles["section"]))
    conds = [
        "ההצעה בתוקף למשך 30 יום מתאריך ההנפקה.",
        "מקדמה של 30% נדרשת לתחילת העבודה.",
        "היתרה משולמת בסיום ההשקה הסופית של האתר.",
        "הלקוח מתחייב לספק תכנים (טקסטים, תמונות) בזמן שנקבע.",
        "זכויות היוצרים של הקוד עוברות ללקוח לאחר תשלום מלא.",
        "כל שינוי מחוץ להיקף ההצעה יתומחר בנפרד בתוספת הסכם.",
    ]
    for c in conds:
        story.append(Paragraph(rtl(f"•  {c}"), styles["body"]))
    story.append(Spacer(1, 18))

    # --- Acceptance ---
    story.append(Paragraph(rtl(f"אישור ההצעה — {devis_num}"), styles["accept_h"]))
    story.append(Paragraph(rtl(
        "נא לכתוב בכתב יד \"אושר וחתום\" ולאחר מכן לחתום ולציין את התאריך."),
        styles["body"]))
    story.append(Spacer(1, 24))

    sign_tbl = Table(
        [
            ["_________________________", "_________________________"],
            [rtl("חתימת נותן השירות"), rtl("חתימת הלקוח")],
            [rtl("תאריך: ____________"), rtl("תאריך: ____________")],
        ],
        colWidths=[8.9 * cm, 8.9 * cm],
    )
    sign_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Uni"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sign_tbl)

    doc.build(story)
    print("✔ DEVIS-AVALIOR-HE.pdf")


if __name__ == "__main__":
    build_french()
    build_hebrew()
    print(f"\nסה\"כ בשתי ההצעות: 5,500.00 €")
