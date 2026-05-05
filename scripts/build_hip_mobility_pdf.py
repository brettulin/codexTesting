#!/usr/bin/env python3
"""Build the 4-week hip mobility program PDF."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "hip_mobility_4_week_program.pdf"

EXERCISES = [
    {
        "name": "90/90 Breathing Reset",
        "dose": "5 slow breaths",
        "why": "Relaxes the low back/hip flexors and sets the pelvis before mobility work.",
        "video": "https://www.youtube.com/results?search_query=90%2F90+breathing+reset+exercise",
        "cue": "Feet on wall or chair. Exhale slowly and let ribs soften down.",
        "kind": "breath",
    },
    {
        "name": "Half-Kneeling Hip Flexor Stretch",
        "dose": "30-45 sec/side",
        "why": "Opens the front of the hip for posture, stride, and golf hip extension.",
        "video": "https://www.youtube.com/results?search_query=half+kneeling+hip+flexor+stretch+glute+squeeze",
        "cue": "Tuck pelvis slightly, squeeze kneeling-side glute, then shift forward gently.",
        "kind": "kneel",
    },
    {
        "name": "Adductor Rock-Back",
        "dose": "8-10 reps/side",
        "why": "Targets inner-thigh mobility needed for squat depth and hip turn.",
        "video": "https://www.youtube.com/results?search_query=adductor+rock+back+stretch+exercise",
        "cue": "One leg out to the side. Rock hips back slowly; do not force the groin.",
        "kind": "adductor",
    },
    {
        "name": "90/90 Hip Switches",
        "dose": "6-8 slow reps total",
        "why": "Builds hip internal and external rotation control.",
        "video": "https://www.youtube.com/results?search_query=90+90+hip+switches+mobility",
        "cue": "Use hands behind you. Rotate knees side to side like windshield wipers.",
        "kind": "switch",
    },
    {
        "name": "Figure-4 Glute Stretch",
        "dose": "30 sec/side",
        "why": "Opens glutes and deep hip rotators that can restrict squat and rotation.",
        "video": "https://www.youtube.com/results?search_query=figure+4+glute+stretch+floor",
        "cue": "Cross ankle over thigh and gently pull thigh toward you. Do not force knee down.",
        "kind": "fig4",
    },
    {
        "name": "Knee-to-Wall Ankle Rocks",
        "dose": "10 reps/side",
        "why": "Improves ankle dorsiflexion so heels can stay down in the squat.",
        "video": "https://www.youtube.com/results?search_query=knee+to+wall+ankle+mobility+exercise",
        "cue": "Keep heel down and knee tracking over middle toes as knee moves toward wall.",
        "kind": "ankle",
    },
    {
        "name": "Supported Deep Squat Hold",
        "dose": "30-60 sec",
        "why": "Integrates hips and ankles into a comfortable heels-down squat.",
        "video": "https://www.youtube.com/results?search_query=supported+deep+squat+hold+mobility",
        "cue": "Hold support. Only squat as low as heels stay down. Breathe and relax.",
        "kind": "squat",
    },
    {
        "name": "Optional Golf Hip Turns",
        "dose": "8 reps/side",
        "why": "Teaches hip rotation without forcing the low back to do all the work.",
        "video": "https://www.youtube.com/results?search_query=standing+golf+hip+turn+mobility+drill",
        "cue": "Club or broom across shoulders. Turn smoothly; avoid cranking the back.",
        "kind": "golf",
    },
]

PROGRESSION = [
    ["Week 1", "Learn positions", "Use support freely. Do not chase depth."],
    ["Week 2", "Add time", "Add 10-15 sec to exercises #2, #5, and #7 if they feel good."],
    ["Week 3", "Add control", "Pause 2 sec at the end range of #3, #4, and #6."],
    ["Week 4", "Integrate", "After the routine, do 3 easy heels-down squats and 5 slow golf hip turns/side."],
]


class ExerciseSketch(Flowable):
    """Small, intentionally simple line-art exercise sketch."""

    def __init__(self, kind: str, width: float = 1.45 * inch, height: float = 1.0 * inch):
        super().__init__()
        self.kind = kind
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#284b63"))
        c.setLineWidth(2)
        w, h = self.width, self.height
        y0 = 10
        c.setStrokeColor(colors.HexColor("#d8e2dc"))
        c.line(5, y0, w - 5, y0)
        c.setStrokeColor(colors.HexColor("#284b63"))

        def head(x, y):
            c.circle(x, y, 5, stroke=1, fill=0)

        if self.kind == "breath":
            head(42, 42); c.line(47, 40, 88, 25); c.line(60, 32, 70, 56); c.line(70, 56, 105, 56); c.line(88, 25, 113, 25)
            c.setStrokeColor(colors.HexColor("#3c6e71")); c.arc(22, 48, 39, 65, 200, 120)
        elif self.kind == "kneel":
            head(55, 62); c.line(55, 57, 55, 30); c.line(55, 35, 30, 15); c.line(55, 33, 85, 33); c.line(85, 33, 100, 14); c.line(35, 15, 58, 15)
        elif self.kind == "adductor":
            head(52, 56); c.line(52, 51, 60, 35); c.line(45, 36, 70, 36); c.line(52, 38, 32, 15); c.line(60, 34, 112, 18); c.line(112, 18, 126, 18)
        elif self.kind == "switch":
            head(64, 58); c.line(64, 53, 64, 35); c.line(64, 35, 38, 20); c.line(38, 20, 28, 38); c.line(64, 35, 94, 20); c.line(94, 20, 112, 34)
            c.setStrokeColor(colors.HexColor("#3c6e71")); c.arc(42, 18, 102, 58, 210, 120)
        elif self.kind == "fig4":
            head(37, 43); c.line(42, 41, 80, 28); c.line(80, 28, 113, 29); c.line(78, 30, 61, 50); c.line(61, 50, 93, 48); c.line(82, 29, 65, 14)
        elif self.kind == "ankle":
            c.setStrokeColor(colors.HexColor("#6b705c")); c.line(w - 25, y0, w - 25, h - 5)
            c.setStrokeColor(colors.HexColor("#284b63")); head(55, 62); c.line(55, 57, 62, 35); c.line(62, 35, 38, 14); c.line(62, 35, 98, 16); c.line(98, 16, 119, 16); c.line(98, 16, w - 30, 38)
        elif self.kind == "squat":
            c.setStrokeColor(colors.HexColor("#6b705c")); c.line(18, y0, 18, h - 5)
            c.setStrokeColor(colors.HexColor("#284b63")); head(58, 58); c.line(58, 53, 64, 35); c.line(64, 35, 42, 15); c.line(42, 15, 25, 15); c.line(64, 35, 90, 15); c.line(90, 15, 110, 15); c.line(56, 48, 20, 45)
        else:
            head(65, 57); c.line(65, 52, 65, 25); c.line(35, 44, 95, 44); c.line(65, 25, 45, 12); c.line(65, 25, 87, 12)
            c.setStrokeColor(colors.HexColor("#3c6e71")); c.arc(35, 25, 98, 70, 20, 140)


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(doc.leftMargin, 0.35 * inch, "4-Week Hip Mobility Program • General fitness education, not medical care")
    canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=LETTER, rightMargin=0.55 * inch, leftMargin=0.55 * inch,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=24, leading=28, textColor=colors.HexColor("#1f2937")))
    styles.add(ParagraphStyle(name="Sub", parent=styles["BodyText"], alignment=TA_CENTER, fontSize=11, leading=15, textColor=colors.HexColor("#374151")))
    styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontSize=15, leading=18, textColor=colors.HexColor("#284b63"), spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontSize=9.5, leading=12.5))
    styles.add(ParagraphStyle(name="Link", parent=styles["BodyText"], fontSize=8.5, leading=10.5, textColor=colors.HexColor("#1d4ed8")))

    story = [
        p("4-Week Hip Mobility Program", styles["TitleCenter"]),
        p("Simple daily guide for heels-down squats, general health, and golf rotation", styles["Sub"]),
        Spacer(1, 0.14 * inch),
        p("Time commitment: <b>10-12 minutes/day, 5 days/week</b>. Optional 2-minute golf add-on before practice or rounds.", styles["Body"]),
        p("Safety: stop for sharp pain, numbness, tingling, front-of-hip pinching, or symptoms that linger. Work at a 3-5/10 stretch intensity; tension is fine, pain is not. Warm up with 2-3 minutes of easy walking or marching.", styles["Body"]),
        p("Why this helps", styles["H2x"]),
        p("If your heels lift when you squat, the limitation can come from hips, ankles, trunk control, or a mix. This plan targets hip flexors, adductors, hip rotation, glutes, and ankles because they are common restrictions for squatting and golf rotation.", styles["Body"]),
        p("Weekly progress checks", styles["H2x"]),
        ListFlowable([
            ListItem(p("<b>Heels-down squat:</b> once per week, note how low you can go before heels lift.", styles["Body"])),
            ListItem(p("<b>Knee-to-wall ankle check:</b> toes 3-5 inches from wall, knee toward wall, heel down. Note best distance on each side.", styles["Body"])),
        ], bulletType="bullet", start="circle"),
        p("Daily routine", styles["H2x"]),
    ]

    header = ["#", "Exercise", "Dose", "Why", "Video"]
    data = [header]
    for i, ex in enumerate(EXERCISES, 1):
        data.append([
            str(i),
            p(f"<b>{ex['name']}</b>", styles["Small"]),
            p(ex["dose"], styles["Small"]),
            p(ex["why"], styles["Small"]),
            p(f"<link href='{ex['video']}'>Open demo</link>", styles["Link"]),
        ])
    table = Table(data, colWidths=[0.28 * inch, 1.55 * inch, 0.9 * inch, 2.35 * inch, 0.9 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#284b63")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story += [table, p("Four-week progression", styles["H2x"])]

    prog = Table([["Week", "Focus", "What to do"]] + PROGRESSION, colWidths=[0.85 * inch, 1.35 * inch, 4.0 * inch])
    prog.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3c6e71")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story += [prog, PageBreak(), p("Exercise cards", styles["H2x"])]

    cards = []
    for i, ex in enumerate(EXERCISES, 1):
        card = Table([
            [ExerciseSketch(ex["kind"]), p(f"<b>{i}. {ex['name']}</b><br/><b>Dose:</b> {ex['dose']}<br/><b>Cue:</b> {ex['cue']}<br/><link href='{ex['video']}'>Click for video demo</link>", styles["Body"])]
        ], colWidths=[1.65 * inch, 4.7 * inch])
        card.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbfbf8")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        cards.extend([card, Spacer(1, 0.08 * inch)])
    story += cards
    story += [
        p("Weekly target", styles["H2x"]),
        p("Minimum effective dose: 5 sessions/week. Best time: after a short walk, workout, shower, or at night when you can be consistent. Expect less stiffness in 1-2 weeks; squat depth improves gradually.", styles["Body"]),
        p("References", styles["H2x"]),
        p("Mayo Clinic stretching guidance was used for safety principles: warm up, avoid bouncing, breathe, and stretch to tension rather than pain. Titleist golf instruction was used for the golf-rotation rationale.", styles["Small"]),
    ]
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
