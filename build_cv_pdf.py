from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_LEFT
from PIL import Image, ImageOps
import os
from pathlib import Path


OUT_DIR = str(Path(__file__).resolve().parent)
OUTPUT = os.path.join(OUT_DIR, os.environ.get("CV_OUTPUT", "cv-javier-peigneux.pdf"))
PHOTO = os.path.join(OUT_DIR, os.environ.get("CV_PHOTO", "linkedin-photo.jpg"))

PAGE_W, PAGE_H = A4
SIDEBAR_W = 63 * mm
MARGIN = 8 * mm
GREEN = colors.HexColor("#B7E33E")
DARK = colors.HexColor("#1D2124")
TEXT = colors.HexColor("#24282B")
MUTED = colors.HexColor("#60676B")
LIGHT = colors.HexColor("#F4F6F4")

FONT_DIR = os.environ.get("CV_FONT_DIR", os.path.join(OUT_DIR, "assets", "fonts"))
pdfmetrics.registerFont(TTFont("Lato", os.path.join(FONT_DIR, "Lato-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lato-Bold", os.path.join(FONT_DIR, "Lato-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lato-Black", os.path.join(FONT_DIR, "Lato-Black.ttf")))


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def line(c, x, y, width, color=TEXT, thickness=0.8):
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)


def heading(c, text, x, y, width):
    c.setFillColor(TEXT)
    c.setFont("Lato-Bold", 10)
    c.drawString(x, y, text.upper())
    line(c, x, y - 5, width, TEXT, 0.8)
    return y - 14


def sidebar_section(c, title, x, y, width):
    c.setFillColor(colors.white)
    c.setFont("Lato-Bold", 9.2)
    c.drawString(x, y, title)
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.5)
    c.line(x, y - 6, x + 24, y - 6)
    return y - 17


def linkedin_icon(c, x, y, size=8):
    c.setFillColor(GREEN)
    c.roundRect(x, y, size, size, 1.2, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Lato-Bold", size * 0.72)
    c.drawCentredString(x + size / 2, y + size * 0.12, "in")


def mail_icon(c, x, y, size=8):
    c.setStrokeColor(GREEN)
    c.setLineWidth(1)
    c.roundRect(x, y, size, size * 0.75, 1.2, fill=0, stroke=1)
    c.line(x + 1, y + size * 0.67, x + size / 2, y + size * 0.25)
    c.line(x + size / 2, y + size * 0.25, x + size - 1, y + size * 0.67)


def location_icon(c, x, y, size=8):
    c.setStrokeColor(GREEN)
    c.setLineWidth(1)
    c.circle(x + size / 2, y + size * 0.62, size * 0.22, fill=0, stroke=1)
    path = c.beginPath()
    path.moveTo(x + size * 0.28, y + size * 0.48)
    path.lineTo(x + size / 2, y)
    path.lineTo(x + size * 0.72, y + size * 0.48)
    c.drawPath(path, fill=0, stroke=1)


def draw_sidebar(c, page_number):
    c.setFillColor(DARK)
    c.rect(0, 0, SIDEBAR_W, PAGE_H, fill=1, stroke=0)
    x = 8 * mm
    width = SIDEBAR_W - 16 * mm

    c.setFillColor(colors.white)
    c.setFont("Lato-Black", 19)
    c.drawString(x, PAGE_H - 18 * mm, "Javier")
    c.drawString(x, PAGE_H - 26 * mm, "Peigneux")
    c.setFont("Lato", 8.2)
    c.setFillColor(colors.HexColor("#D7DADB"))
    c.drawString(x, PAGE_H - 34 * mm, "iOS Software Developer")

    photo_size = 41.6 * mm
    photo_center_y = PAGE_H - 61 * mm
    photo_x = (SIDEBAR_W - photo_size) / 2
    photo_y = photo_center_y - photo_size / 2
    if os.path.exists(PHOTO):
        with Image.open(PHOTO) as source_image:
            image = source_image.convert("RGB")
            crop_side = int(min(image.size) / 1.15)
            left = (image.width - crop_side) // 2
            cropped_image = image.crop((left, 0, left + crop_side, crop_side))
            square_image = ImageOps.fit(cropped_image, (800, 800), centering=(0.5, 0.0))
            photo_reader = ImageReader(square_image)
        c.saveState()
        circle = c.beginPath()
        circle.circle(photo_x + photo_size / 2, photo_y + photo_size / 2, photo_size / 2)
        c.clipPath(circle, stroke=0, fill=0)
        c.drawImage(photo_reader, photo_x, photo_y, photo_size, photo_size, preserveAspectRatio=False, mask="auto")
        c.restoreState()

    y = PAGE_H - 91 * mm
    c.setFillColor(colors.white)
    linkedin_icon(c, x, y - 1)
    c.setFillColor(colors.white)
    c.setFont("Lato-Bold", 7.8)
    c.drawString(x + 12, y, "LinkedIn")
    c.setFillColor(GREEN)
    c.linkURL("https://www.linkedin.com/in/javier-peigneux-d-egmont/", (x, y - 2, x + width, y + 8), relative=0)
    y -= 15
    c.setFillColor(colors.white)
    c.setFont("Lato", 7.8)
    mail_icon(c, x, y - 1)
    c.drawString(x + 12, y, "javierpeigneux@gmail.com")
    c.linkURL("mailto:javierpeigneux@gmail.com", (x, y - 2, x + width, y + 8), relative=0)
    y -= 13
    location_icon(c, x, y - 1)
    c.drawString(x + 12, y, "Valencia, Spain")

def draw_sidebar_details(c):
    x = 8 * mm
    width = SIDEBAR_W - 16 * mm
    y = PAGE_H - 115 * mm
    y = sidebar_section(c, "Technical expertise", x, y, width)
    skills = [
        ("iOS Development", "Swift · SwiftUI · UIKit · Combine · Objective-C"),
        ("Architecture", "MVC · MVVM · ViewState · Dependency Injection · SPM modularization"),
        ("APIs & Data", "GraphQL · Apollo · REST"),
        ("Quality", "Swift Testing · XCTest · UI/E2E · accessibility · localization"),
        ("Tools & Backend", "Xcode · Git · CI/CD · Django · Python"),
        ("AI-assisted Engineering", "Codex · Claude Code<br/>Implementation, refactoring, test generation &amp; documentation"),
    ]
    for label, value in skills:
        y -= 5
        c.setFillColor(GREEN)
        c.setFont("Lato-Bold", 8)
        c.drawString(x, y, label)
        y -= 12
        y = paragraph(c, value, x, y + 2, width, ParagraphStyle("skill", fontName="Lato", fontSize=8, leading=10, textColor=colors.white)) - 7

    y -= 10
    y = sidebar_section(c, "Education", x, y, width)
    education = [
        ("Universitat Politècnica de València", "Technical Engineering in Computer Management<br/>2007 - 2011"),
        ("Politechnika Krakowska", "Computer Science final project<br/>2011 - 2012"),
    ]
    for school, detail in education:
        c.setFillColor(GREEN)
        c.setFont("Lato-Bold", 6.9)
        y = paragraph(c, school, x, y, width, ParagraphStyle("school", fontName="Lato-Bold", fontSize=8, leading=10, textColor=GREEN)) - 3
        y = paragraph(c, detail, x, y, width, ParagraphStyle("edu", fontName="Lato", fontSize=7.8, leading=10, textColor=colors.white)) - 8

    y -= 8
    y = sidebar_section(c, "Languages", x, y, width)
    for language, level in [("Spanish", "Native"), ("English", "Full professional"), ("Valencian", "Bilingual")]:
        c.setFillColor(colors.white)
        c.setFont("Lato-Bold", 8)
        c.drawString(x, y, language)
        c.setFont("Lato", 7.8)
        c.setFillColor(colors.HexColor("#D7DADB"))
        c.drawRightString(x + width, y, level)
        y -= 17
    if y < 10 * mm:
        raise ValueError("Sidebar exceeds one-page layout")

def make_pdf():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("Javier Peigneux d'Egmont Benito - CV")
    c.setAuthor("Javier Peigneux d'Egmont Benito")
    content_x = SIDEBAR_W + 8 * mm
    content_w = PAGE_W - content_x - 8 * mm

    body = ParagraphStyle("body", fontName="Lato", fontSize=8.7, leading=11, textColor=TEXT, alignment=TA_LEFT)
    role = ParagraphStyle("role", fontName="Lato-Bold", fontSize=11, leading=13, textColor=TEXT)
    team_role = ParagraphStyle("team_role", fontName="Lato-Bold", fontSize=8.5, leading=10.5, textColor=TEXT)
    date = ParagraphStyle("date", fontName="Lato", fontSize=8, leading=10, textColor=MUTED)
    bullet = ParagraphStyle("bullet", fontName="Lato", fontSize=8.5, leading=10.5, textColor=TEXT, leftIndent=8, firstLineIndent=-5)

    def new_page(number):
        nonlocal y
        if number > 1:
            c.showPage()
        draw_sidebar(c, number)
        y = PAGE_H - 16 * mm

    def ensure(height):
        nonlocal y, page_number
        if y - height < 14 * mm:
            raise ValueError("Content exceeds one-page layout; shorten copy or adjust spacing")

    def add_section(title):
        nonlocal y
        ensure(26)
        y = heading(c, title, content_x, y, content_w)

    def add_role(title, dates, bullets, compact=False, team=False):
        nonlocal y
        y -= 7 if team else 10
        indent = 8 if team else 0
        if team:
            date_width = stringWidth(dates, "Lato", 7.7)
            title_width = content_w - indent - date_width - 10
            title_bottom = paragraph(c, title, content_x + indent, y, title_width, team_role)
            c.setFillColor(MUTED)
            c.setFont("Lato", 7.7)
            c.drawRightString(content_x + content_w, y - 8.5, dates)
            y = title_bottom - 3
        else:
            y = paragraph(c, title, content_x, y, content_w, role) - 2
            y = paragraph(c, dates, content_x, y, content_w, date) - 4
        for item in bullets:
            h_before = y
            y = paragraph(c, f"• {item}", content_x + indent + 2, y, content_w - indent - 2, bullet) - 2
            if h_before - y > 45:
                ensure(5)

    page_number = 1
    new_page(page_number)
    add_section("Profile")
    y = paragraph(c, "iOS engineer with 14 years of experience delivering consumer and client-facing apps. Experienced in modular Swift codebases, SwiftUI/UIKit and GraphQL, with a focus on onboarding, profiles, design systems and automated testing.", content_x, y, content_w, body) - 19

    add_section("Experience")
    add_role("XING", "Valencia, Spain · May 2020 - November 2026", [
        "Deliver iOS features in a modular Swift codebase, collaborating with product, design and engineering from discovery through code review and release.",
    ])
    add_role("Well Described Talents Team (Profile & Onboarding)", "2023 - 2026", [
        "Built GraphQL-backed profile and onboarding flows, including Documents, data imports, skills and work eligibility, with accessibility and end-to-end coverage.",
        "Modernized localization with String(localized:) and migrated unit tests to Swift Testing.",
    ], compact=True, team=True)
    add_role("Notifications Team", "2024 - 2025", ["Improved the notification center and recruiter/contact notifications, including notification limits, tracking and accessibility."], compact=True, team=True)
    add_role("Job Preferences Team", "2024", ["Developed preference collection flows and job-title logic to support job search and profile preferences."], compact=True, team=True)
    add_role("Content Team", "2024", ["Built video and premium article experiences, integrating membership access, caching and GraphQL data."], compact=True, team=True)
    add_role("Disco Team", "2020 - 2023", [
        "Built social-feed features including stories, comments, sharing and recommendations; improved reusable UI, GraphQL integration and unit/UI coverage.",
    ], compact=True, team=True)
    add_role("Armstrong Team", "2020 - 2021", ["Contributed to the iOS migration across the social feed, native advertising and recommendations, including navigation, analytics and test infrastructure."], compact=True, team=True)
    add_role("Design Team", "2020", ["Contributed typography, layout behavior, documentation and examples to XING's SwiftUI design system."], compact=True, team=True)
    add_role("treeNovum", "Valencia, Spain · January 2019 - May 2020", [
        "Maintained complex iOS apps for the Swiss Ice Hockey League and Coca-Cola, working with Combine and product/engineering stakeholders.",
    ], compact=True)
    add_role("Navilo Mobile S.L.", "Valencia, Spain · September 2015 - December 2018", [
        "Delivered apps for international clients, including glucose-monitoring products and a BMW catalogue with complex interfaces and animations.",
        "Worked with Django/Python backends and AWS services alongside mobile development.",
    ], compact=True)
    add_role("CatalogPlayer", "Valencia, Spain · October 2014 - September 2015", ["Developed and maintained iOS product features through implementation and delivery."], compact=True)
    add_role("Imagina group", "Valencia, Spain · October 2012 - August 2014", ["Built apps from concept to delivery, including Timp and sponsored city guides for more than 20 cities."], compact=True)

    ensure(0)
    draw_sidebar_details(c)
    c.save()


if __name__ == "__main__":
    make_pdf()
    print(OUTPUT)
