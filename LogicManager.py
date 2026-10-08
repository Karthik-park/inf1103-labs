"""
LogicManager.py

Sits between the AI API and the Data Manager. For each of the three
AI-assisted resume sections (skills, professional summary, and each job's
description), it:

  1. Normalizes the AI's raw response into 3 clean option strings.
  2. Lets the user pick one.
  3. Asks if they'd like to edit it before it's locked in.
  4. Writes the final value back into the resume record.

Once all sections have been reviewed, it also generates the final PDF
resume, named "<Name>'s Resume.pdf". Everything needed for both steps
lives in this single file.

Expected shape of `ai_results` passed into run_logic_manager():

    ai_results = {
        "skills": <raw AI response containing 3 skill-suggestion options>,
        "summary": <raw AI response containing 3 professional-summary options>,
        "job_descriptions": [
            <raw AI response for job_experiences[0]>,
            <raw AI response for job_experiences[1]>,
            ...
        ],
    }

The exact format coming back from your AI API wasn't finalized at the time
this was written, so `extract_options()` below tries to handle several
common shapes (a plain list of 3 strings, a dict with an "options"/"choices"
key, a dict of "option_1"/"option_2"/"option_3", or raw numbered text).
Once you know your API's actual response format, you likely only need to
adjust `extract_options()` — everything else stays the same.
"""

import json
import os
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    HRFlowable,
)


# ---------------------------------------------------------------------------
# Normalizing raw AI responses into 3 clean options
# ---------------------------------------------------------------------------

def extract_options(ai_response, expected_count=3):
    """
    Converts a raw AI response into a list of `expected_count` strings,
    regardless of whether it arrived as a list, a dict, or raw text.
    """
    data = ai_response

    # If it's a JSON-looking string, try to parse it first.
    if isinstance(data, str):
        stripped = data.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                data = json.loads(stripped)
            except (json.JSONDecodeError, ValueError):
                pass  # Not actually JSON — fall through to plain-text handling.

    options = None

    # Case 1: already a clean list of strings.
    if isinstance(data, list) and all(isinstance(item, str) for item in data):
        options = data

    # Case 2: dict wrapping the options somehow.
    elif isinstance(data, dict):
        for key in ("options", "choices", "suggestions", "results"):
            if key in data and isinstance(data[key], list):
                options = [str(item) for item in data[key]]
                break
        if options is None:
            numbered_keys = [k for k in data.keys() if re.search(r"\d", str(k))]
            if numbered_keys:
                numbered_keys.sort(key=lambda k: re.search(r"\d+", str(k)).group())
                options = [str(data[k]) for k in numbered_keys]
            else:
                options = [str(v) for v in data.values()]

    # Case 3: plain text — split into numbered/newline-separated chunks.
    elif isinstance(data, str):
        lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
        cleaned = [re.sub(r"^\s*(\d+[\.\)]|[-*])\s*", "", line) for line in lines]
        options = cleaned if cleaned else [data.strip()]

    else:
        options = [str(data)]

    # Pad or trim to exactly `expected_count` options.
    if len(options) < expected_count:
        options = options + ["(No additional suggestion provided)"] * (
            expected_count - len(options)
        )
    return options[:expected_count]


# ---------------------------------------------------------------------------
# Interactive selection helpers
# ---------------------------------------------------------------------------

def display_options(options):
    """Prints each option with a number label."""
    for i, option in enumerate(options, start=1):
        print(f"\n  Option {i}:")
        print(f"    {option}")


def choose_option(options):
    """Displays the options and returns the one the user selects."""
    display_options(options)
    valid_choices = [str(i) for i in range(1, len(options) + 1)]
    while True:
        choice = input(f"\nSelect an option (1-{len(options)}): ").strip()
        if choice not in valid_choices:
            print("Invalid choice. Try again.")
            continue
        return options[int(choice) - 1]


def offer_edit(selected_text, field_label):
    """Asks the user if they'd like to edit the selected text before it's locked in."""
    while True:
        wants_edit = input(
            f"\nWould you like to make any changes to the {field_label} "
            f"before it's added to your resume? (yes/no): "
        ).strip().lower()
        if wants_edit in ("yes", "y"):
            print(f"\nCurrent {field_label}:\n{selected_text}")
            edited = input(f"\nEnter your edited {field_label}: ").strip()
            if not edited:
                print("Edited text cannot be empty. Keeping the original selection.")
                return selected_text
            return edited
        elif wants_edit in ("no", "n"):
            return selected_text
        else:
            print("Please enter 'yes' or 'no'.")


# ---------------------------------------------------------------------------
# Section processors
# ---------------------------------------------------------------------------

def process_skills(record, ai_skills_response):
    """
    Presents 3 AI-suggested sets of additional skills, lets the user pick
    and optionally edit one, then merges the result into record['skills'].
    """
    print("\n" + "=" * 50)
    print("SKILLS — AI SUGGESTIONS")
    print("=" * 50)
    print("Here are 3 AI-suggested additions to your skills, based on your profile:")

    options = extract_options(ai_skills_response)
    chosen = choose_option(options)
    chosen = offer_edit(chosen, "skill suggestions")

    new_skills = [s.strip() for s in re.split(r",|;", chosen) if s.strip()]
    for skill in new_skills:
        if skill not in record["skills"]:
            record["skills"].append(skill)

    return record


def process_summary(record, ai_summary_response):
    """
    Presents 3 AI-suggested professional summaries, lets the user pick and
    optionally edit one, then stores it as record['summary'].
    """
    print("\n" + "=" * 50)
    print("PROFESSIONAL SUMMARY — AI SUGGESTIONS")
    print("=" * 50)
    print("Here are 3 AI-suggested professional summaries for your resume:")

    options = extract_options(ai_summary_response)
    chosen = choose_option(options)
    chosen = offer_edit(chosen, "professional summary")

    record["summary"] = chosen
    return record


def process_job_descriptions(record, ai_job_descriptions):
    """
    For each job in record['job_experiences'], presents 3 AI-suggested
    descriptions (aligned by index with ai_job_descriptions), lets the user
    pick and optionally edit one, then overwrites that job's description.
    """
    jobs = record.get("job_experiences", [])

    if not jobs:
        print("\nNo job experience entries to generate descriptions for. Skipping.")
        return record

    print("\n" + "=" * 50)
    print("JOB DESCRIPTIONS — AI SUGGESTIONS")
    print("=" * 50)

    for idx, job in enumerate(jobs):
        if idx >= len(ai_job_descriptions):
            print(
                f"\nNo AI suggestions were provided for "
                f"{job['role']} at {job['company']}. Keeping existing description."
            )
            continue

        print(f"\n--- {job['role']} at {job['company']} ({job['duration']}) ---")
        options = extract_options(ai_job_descriptions[idx])
        chosen = choose_option(options)
        chosen = offer_edit(chosen, "job description")
        job["description"] = chosen

    record["job_experiences"] = jobs
    return record


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def sanitize_filename(name):
    """Strips characters that aren't safe to use in a file name."""
    cleaned = re.sub(r'[\\/:*?"<>|]', "", name).strip()
    return cleaned if cleaned else "Resume"


def build_styles():
    """Builds the paragraph styles used throughout the resume."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ResumeName",
        parent=styles["Title"],
        fontSize=22,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="ContactInfo",
        parent=styles["Normal"],
        fontSize=10,
        alignment=TA_CENTER,
        textColor="#444444",
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=6,
        textColor="#1A1A1A",
    ))

    styles.add(ParagraphStyle(
        name="JobTitle",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica-Bold",
        spaceAfter=1,
    ))

    styles.add(ParagraphStyle(
        name="JobMeta",
        parent=styles["Normal"],
        fontSize=9.5,
        textColor="#555555",
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="BodyTextResume",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=14,
    ))

    return styles


def build_resume_story(record, styles):
    """Builds the list of flowables (content blocks) that make up the resume."""
    story = []

    # --- Header: name + contact info ---
    story.append(Paragraph(record.get("name", ""), styles["ResumeName"]))

    contact_parts = []
    if record.get("email"):
        contact_parts.append(record["email"])
    if record.get("phone"):
        contact_parts.append(record["phone"])
    if record.get("location"):
        contact_parts.append(record["location"])
    if record.get("portfolio_url"):
        contact_parts.append(record["portfolio_url"])
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), styles["ContactInfo"]))

    story.append(HRFlowable(width="100%", thickness=1, color="#CCCCCC", spaceAfter=6))

    # --- Professional summary ---
    if record.get("summary"):
        story.append(Paragraph("Professional Summary", styles["SectionHeading"]))
        story.append(Paragraph(record["summary"], styles["BodyTextResume"]))

    # --- Desired job / objective ---
    if record.get("desired_job"):
        story.append(Paragraph("Career Objective", styles["SectionHeading"]))
        story.append(Paragraph(record["desired_job"], styles["BodyTextResume"]))

    # --- Skills ---
    if record.get("skills"):
        story.append(Paragraph("Skills", styles["SectionHeading"]))
        skill_items = [
            ListItem(Paragraph(skill, styles["BodyTextResume"]), leftIndent=10)
            for skill in record["skills"]
        ]
        story.append(ListFlowable(skill_items, bulletType="bullet", leftIndent=14))

    # --- Work experience ---
    if record.get("job_experiences"):
        story.append(Paragraph("Work Experience", styles["SectionHeading"]))
        for job in record["job_experiences"]:
            story.append(Paragraph(
                f"{job.get('role', '')} — {job.get('company', '')}",
                styles["JobTitle"],
            ))
            if job.get("duration"):
                story.append(Paragraph(job["duration"], styles["JobMeta"]))
            if job.get("description"):
                story.append(Paragraph(job["description"], styles["BodyTextResume"]))
            story.append(Spacer(1, 8))

    # --- Qualification ---
    if record.get("qualification"):
        story.append(Paragraph("Education / Qualification", styles["SectionHeading"]))
        story.append(Paragraph(record["qualification"], styles["BodyTextResume"]))

    return story


def generate_resume_pdf(record, output_dir="."):
    """
    Renders the resume record into a PDF file named "<Name>'s Resume.pdf"
    inside output_dir. Returns the full path to the generated file.
    """
    name = record.get("name", "Resume")
    filename = f"{sanitize_filename(name)}'s Resume.pdf"
    output_path = os.path.join(output_dir, filename)

    styles = build_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    story = build_resume_story(record, styles)
    doc.build(story)

    return output_path


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------

def run_logic_manager(record, ai_results, output_dir="."):
    """
    Runs the user through all AI-assisted sections that are present in
    ai_results, in this order: skills, summary, then job descriptions.
    Once reviewed, generates the final PDF resume and saves it into
    output_dir. Returns the updated resume record, ready to be handed to
    the Data Manager.
    """
    print("\n" + "#" * 50)
    print("   REVIEW AI-GENERATED SUGGESTIONS")
    print("#" * 50)

    if "skills" in ai_results:
        record = process_skills(record, ai_results["skills"])

    if "summary" in ai_results:
        record = process_summary(record, ai_results["summary"])

    if "job_descriptions" in ai_results:
        record = process_job_descriptions(record, ai_results["job_descriptions"])

    print("\nAll AI suggestions have been reviewed and applied.")

    pdf_path = generate_resume_pdf(record, output_dir=output_dir)
    print(f"\nYour resume PDF has been generated at: {pdf_path}")

    return record


# ---------------------------------------------------------------------------
# Standalone demo (safe to delete once wired into your real pipeline)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_record = {
        "name": "Karthik",
        "email": "karthik@example.com",
        "phone": "+65 9123 4567",
        "location": "Singapore",
        "qualification": "Diploma in Information Security, Singapore Institute of Technology",
        "skills": ["Network Security", "Firewalls"],
        "job_experiences": [
            {
                "company": "NCS Pte Ltd",
                "role": "Cybersecurity Intern",
                "duration": "Jan 2024 - Jun 2024",
                "description": "Worked on enterprise security architecture.",
            }
        ],
        "desired_job": "Cybersecurity Analyst",
        "portfolio_url": None,
    }

    demo_ai_results = {
        "skills": ["IDS, IPS, SIEM tools", "Python scripting, Risk Assessment", "Cloud Security, AWS"],
        "summary": [
            "Motivated Information Security student with hands-on experience in enterprise network defense.",
            "Detail-oriented cybersecurity enthusiast skilled in firewall and IDS/IPS configuration.",
            "Aspiring security analyst with practical NCS internship experience in threat detection.",
        ],
        "job_descriptions": [
            [
                "Configured and monitored firewalls, IDS, and IPS to protect enterprise infrastructure.",
                "Assisted in enterprise security architecture design, focusing on network defense layers.",
                "Analyzed network traffic for anomalies and supported incident response procedures.",
            ]
        ],
    }

    final_record = run_logic_manager(demo_record, demo_ai_results)
    print("\nFinal record:")
    print(final_record)

    #CHeck if the PDF was generated successfully