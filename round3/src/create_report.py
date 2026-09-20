from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        Image,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    raise SystemExit("Install reportlab first: python -m pip install reportlab")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "classified_public_reaction.csv"
DAILY = ROOT / "outputs" / "daily_analysis.csv"
TOPICS = ROOT / "outputs" / "topic_summary.csv"
SOURCES = ROOT / "outputs" / "source_summary.csv"
SHIFTS = ROOT / "outputs" / "sentiment_shifts.csv"
SPIKES = ROOT / "outputs" / "engagement_spikes.csv"
FIGURES = ROOT / "figures"
REPORT = ROOT / "reports" / "round3_analytical_report.pdf"
REPORT.parent.mkdir(parents=True, exist_ok=True)


def para(text, style):
    return Paragraph(escape(str(text)).replace("\n", "<br/>") , style)


def table(data, widths=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9FB3C8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F4F8")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def main():
    data = pd.read_csv(DATA)
    daily = pd.read_csv(DAILY)
    topics = pd.read_csv(TOPICS)
    sources = pd.read_csv(SOURCES)
    shifts = pd.read_csv(SHIFTS)
    spikes = pd.read_csv(SPIKES)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=19, leading=23, textColor=colors.HexColor("#102A43")))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="Heading", parent=styles["Heading2"], textColor=colors.HexColor("#243B53"), spaceBefore=12, spaceAfter=6))
    story = []

    story.append(Paragraph("Round 3 Analytical Report", styles["TitleCenter"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Public Reaction to a New Educational Technology: Claude for Teachers", styles["Heading1"]))
    story.append(Paragraph("Social Engine — Data Vortex A’26", styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Executive summary", styles["Heading"]))
    story.append(Paragraph(
        f"This report studies public reaction to Anthropic’s Claude for Teachers launch. The case study uses {len(data)} relevant public records collected from Google News RSS and Reddit RSS after the 14 July 2026 launch. The Round 2 sentiment and topic models were reused without retraining. The model classified {int((data['sentiment_prediction']=='Neutral').sum())} records as neutral, {int((data['sentiment_prediction']=='Negative').sum())} as negative, and {int((data['sentiment_prediction']=='Positive').sum())} as positive. Attention was highest on 15 July, immediately after launch, with {int(spikes.iloc[0]['records'])} collected mentions.", styles["BodyText"]))

    story.append(Paragraph("1. Data collection method", styles["Heading"]))
    story.append(Paragraph("The assigned theme was Public Reaction to a New Educational Technology. Claude for Teachers was selected as the case study because it is a clearly dated, teacher-focused educational technology launch. Public records were collected through Google News RSS and public Reddit RSS. A GNews API collector was also tested; its one returned article was retained in the raw archive but excluded from the cleaned event dataset because it was not clearly about the Claude for Teachers launch.", styles["BodyText"]))
    source_rows = [["Source", "Records used"]] + [[str(r.source_type), str(int(r.records))] for r in sources.itertuples()]
    story.append(table(source_rows, [3.7*inch, 1.4*inch]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("The raw self-collected file and cleaning log are preserved separately. The cleaning process removed records published before the launch and records that were not clearly related to Claude for Teachers and education. Negative and critical records were retained rather than removed for their sentiment.", styles["BodyText"]))

    story.append(Paragraph("2. Time window", styles["Heading"]))
    story.append(Paragraph("The analysis window begins on 14 July 2026, the date of Anthropic’s official announcement, and ends on 12 September 2026, the latest relevant record in the cleaned dataset. Each record contains a publication timestamp and a collection timestamp.", styles["BodyText"]))

    story.append(Paragraph("3. Reuse of the Round 2 NLP models", styles["Heading"]))
    story.append(Paragraph("The Round 2 sentiment_model.pkl and topic_model.pkl files were copied into the Round 3 models directory and applied to every cleaned record. The sentiment model produced Negative, Neutral, or Positive predictions. The topic model produced the Round 2 topic labels Community_Discussion, Feature_Feedback, Technical_Issues, and Account_Security. No new classifier was trained for Round 3.", styles["BodyText"]))
    sentiment_rows = [["Sentiment prediction", "Records", "Share"]]
    for label in ["Positive", "Neutral", "Negative"]:
        n = int((data["sentiment_prediction"] == label).sum())
        sentiment_rows.append([label, str(n), f"{n/len(data):.1%}"])
    story.append(table(sentiment_rows, [2.5*inch, 1.1*inch, 1.1*inch]))

    story.append(Paragraph("4. Sentiment analysis", styles["Heading"]))
    story.append(Paragraph("The overall reaction is predominantly neutral under the Round 2 model. Negative predictions are more common than positive predictions, which is consistent with the presence of critical coverage about privacy, classroom usefulness, and the limits of teacher-facing generative AI. The result should be interpreted as model-based classification of headlines and short descriptions, not as a survey of all teachers.", styles["BodyText"]))
    shift_rows = [["Date", "Records", "Mean sentiment", "Change"]]
    for r in shifts.head(5).itertuples():
        shift_rows.append([str(r.date)[:10], str(int(r.records)), f"{r.mean_sentiment:.2f}", f"{r.sentiment_change:.2f}"])
    story.append(table(shift_rows, [1.4*inch, 0.8*inch, 1.2*inch, 0.8*inch]))
    story.append(Paragraph("Two notable transitions are visible in the time series. Coverage moved from the mostly neutral launch period toward a more negative model prediction around 21 July. A later isolated negative prediction appears on 12 September after a positive prediction on 11 September. The second transition is treated cautiously because both dates contain only one record; it is a signal for follow-up, not proof of a population-wide shift.", styles["BodyText"]))
    story.append(Image(str(FIGURES / "sentiment_timeline.png"), width=6.5*inch, height=3.1*inch))

    story.append(Paragraph("5. Activity and attention analysis", styles["Heading"]))
    story.append(Paragraph("The largest activity spike occurred immediately after launch. The dataset contains 14 mentions on 14 July and 19 mentions on 15 July. The concentration is consistent with launch-day news amplification and follow-up coverage. Because RSS feeds do not consistently expose likes, comments, or shares, the report labels this measure an attention or mention-volume proxy rather than true social-media engagement.", styles["BodyText"]))
    spike_rows = [["Date", "Mentions", "Spike flag"]]
    for r in spikes.head(5).itertuples():
        spike_rows.append([str(r.date)[:10], str(int(r.records)), "Yes" if getattr(r, "attention_spike", False) else "Top day"])
    story.append(table(spike_rows, [1.5*inch, 1.1*inch, 1.4*inch]))
    story.append(Image(str(FIGURES / "engagement_spike_timeline.png"), width=6.5*inch, height=3.1*inch))

    story.append(Paragraph("6. Topic and entity analysis", styles["Heading"]))
    topic_rows = [["Predicted topic", "Records", "Share", "Mean sentiment"]]
    for r in topics.itertuples():
        topic_rows.append([str(r.topic_prediction), str(int(r.records)), f"{r.share:.1%}", f"{r.mean_sentiment:.2f}"])
    story.append(table(topic_rows, [2.5*inch, 0.9*inch, 0.8*inch, 1.1*inch]))
    story.append(Paragraph("Community_Discussion is the dominant predicted topic. Feature_Feedback is the second-largest category, while Technical_Issues appears only once. Important entities and themes in the source material include Anthropic, Claude, teachers, K–12 schools, classroom AI, Learning Commons, education standards, and student privacy.", styles["BodyText"]))
    story.append(Image(str(FIGURES / "topic_distribution.png"), width=6.2*inch, height=3.6*inch))

    story.append(Paragraph("7. Trigger explanations", styles["Heading"]))
    story.append(Paragraph("The first activity spike is explained by the official 14 July launch announcement and the immediate news cycle. The later negative predictions are associated with commentary that questions whether standards alignment is a meaningful differentiator, whether AI could deskill newer teachers, and whether student-data and privacy safeguards are sufficient. The later neutral or positive records reflect continuing product and school-access coverage rather than a new launch event.", styles["BodyText"]))

    story.append(Paragraph("8. Limitations", styles["Heading"]))
    story.append(Paragraph("The dataset is a public-web sample rather than a census of public opinion. Google News RSS returned many syndicated or broad-query results, so relevance filtering was necessary. Reddit RSS was temporarily rate-limited for two feeds, leaving one Reddit record in the cleaned set. The attention measure counts collected mentions because likes, comments, and shares were not consistently available. Finally, the Round 2 model was trained on a different labelled dataset, so its predictions should be treated as an analytical instrument rather than ground-truth sentiment labels for every article.", styles["BodyText"]))

    story.append(Paragraph("9. Conclusion", styles["Heading"]))
    story.append(Paragraph("Public attention peaked immediately after Claude for Teachers was announced. The Round 2 model classified most of the collected reaction as neutral, with a smaller negative group and very few positive predictions. Discussion was dominated by broad community reaction, with a smaller set of feature-focused and technical records. The evidence supports a cautious conclusion: the launch generated rapid public attention, while subsequent coverage mixed product interest with concerns about classroom value, teacher expertise, and privacy.", styles["BodyText"]))

    story.append(Paragraph("References", styles["Heading"]))
    refs = [
        "[1] https://www.anthropic.com/news/claude-for-teachers — Introducing Claude for Teachers, 14 July 2026.",
        "[2] https://www.edweek.org/technology/anthropic-launches-claude-for-teachers-why-some-critics-are-concerned/2026/07 — Anthropic Launches Claude for Teachers. Why Some Critics Are Concerned, Education Week, 17 July 2026.",
        "[3] https://gnews.io/ — GNews API documentation and public article search service.",
        "[4] https://news.google.com/ — Google News RSS public search feeds.",
        "[5] https://www.reddit.com/ — Public Reddit RSS feeds used for discussion discovery.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, styles["Small"]))

    doc = SimpleDocTemplate(str(REPORT), pagesize=A4, rightMargin=0.65*inch, leftMargin=0.65*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
    doc.build(story)
    print(f"Created: {REPORT}")


if __name__ == "__main__":
    main()
