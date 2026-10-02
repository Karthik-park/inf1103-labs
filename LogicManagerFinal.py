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

def process_job_descriptions(record, ai_job_descriptions):
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

def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric, spaces, underscores, or hyphens
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized