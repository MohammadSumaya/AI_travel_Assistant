from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle


def create_pdf(text, filename):

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    story = []

    story.append(
        Paragraph("AI Travel Assistant", title_style)
    )

    story.append(
        Paragraph("Travel Itinerary", styles["Heading2"])
    )

    story.append(Spacer(1, 10))

    for line in text.split("\n"):

        line = line.strip()

        if line:

            # Make simple markdown headings look better
            if line.startswith("#"):
                line = line.replace("#", "").strip()

                story.append(
                    Paragraph(
                        line,
                        styles["Heading2"]
                    )
                )

            else:

                # Convert markdown bold to HTML bold
                line = line.replace("**", "<b>", 1)

                if "<b>" in line and "**" in text:
                    line = line.replace("**", "</b>", 1)

                story.append(
                    Paragraph(
                        line,
                        styles["BodyText"]
                    )
                )

            story.append(Spacer(1, 6))

    document.build(story)

    return filename