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

#Process_job_descriptions uses previous functions to allow user to choose options and make edits if he wants.
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

#Cleans the end product pdf file to remove any unwanted characters.
def sanitize_filename(filename):
    