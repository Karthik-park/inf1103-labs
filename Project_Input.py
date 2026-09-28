import re
import calendar
from datetime import date


# ---------------------------------------------------------------------------
# Basic field collectors
# ---------------------------------------------------------------------------

def get_name():
    """Collects and validates the user's full name."""
    while True:
        name = input("Enter your full name: ").strip()
        if not name:
            print("Name cannot be empty. Try again.")
            continue
        if not all(part.isalpha() or part in " -'" for part in name):
            print("Name should only contain letters, spaces, hyphens, or apostrophes. Try again.")
            continue
        return name


def get_age():
    """Collects and validates the user's age."""
    while True:
        entry = input("Enter your age: ").strip()
        try:
            age = int(entry)
        except ValueError:
            print("Invalid number entered. Try again.")
            continue
        if age < 16 or age > 100:
            print("Please enter a realistic age (16-100). Try again.")
            continue
        return age


def get_email():
    """Collects and validates an email address (simple format check)."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    while True:
        email = input("Enter your email address: ").strip()
        if not re.match(pattern, email):
            print("That doesn't look like a valid email. Try again.")
            continue
        return email


def get_phone():
    """Collects and validates a phone number (digits, spaces, + allowed)."""
    pattern = r"^[\d\s\+\-\(\)]{8,10}$"
    while True:
        phone = input("Enter your phone number: ").strip()
        if not re.match(pattern, phone):
            print("Invalid phone number format. Try again.")
            continue
        return phone


def get_location():
    """Collects the user's current location/city."""
    while True:
        location = input("Enter your city/location: ").strip()
        if not location:
            print("Location cannot be empty. Try again.")
            continue
        return location


def get_qualification():
    """Collects the user's highest qualification from a fixed set of options."""
    options = {
        "1": "High School Diploma",
        "2": "Associate's Degree",
        "3": "Bachelor's Degree",
        "4": "Master's Degree",
        "5": "Doctorate (PhD)",
        "6": "Other",
    }
    print("\nSelect your highest qualification:")
    for key, value in options.items():
        print(f"  {key}. {value}")

    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice not in options:
            print("Invalid choice. Try again.")
            continue
        if options[choice] == "Other":
            custom = input("Please specify your qualification: ").strip()
            if not custom:
                print("Qualification cannot be empty. Try again.")
                continue
            return custom
        return options[choice]


def get_desired_job_description():
    """Collects a free-text description of the job the user wants."""
    while True:
        description = input("Describe the job you're looking for (title/field/role): ").strip()
        if not description:
            print("Job description cannot be empty. Try again.")
            continue
        return description


def get_skills():
    """Collects a list of skills, one per line, until the user types 'done'."""
    print("\nEnter your skills one at a time. Type 'done' when finished.")
    skills = []
    while True:
        skill = input(f"Skill #{len(skills) + 1} (or 'done'): ").strip()
        if skill.lower() == "done":
            if not skills:
                print("You must enter at least one skill before finishing.")
                continue
            return skills
        if not skill:
            print("Skill cannot be blank. Try again.")
            continue
        skills.append(skill)


def get_linkedin_or_portfolio():
    """Collects an optional LinkedIn/portfolio URL."""
    while True:
        url = input("Enter LinkedIn or portfolio URL (optional, press Enter to skip): ").strip()
        if not url:
            return None
        if not url.startswith(("http://", "https://")):
            print("URL should start with http:// or https://. Try again.")
            continue
        return url


# ---------------------------------------------------------------------------
# Job experience (repeatable entry, optional overall)
# ---------------------------------------------------------------------------

def get_month(prompt="Month (1-12): "):
    """Collects and validates a month number (1-12)."""
    while True:
        entry = input(prompt).strip()
        try:
            month_num = int(entry)
        except ValueError:
            print("Please enter a valid month number (1-12). Try again.")
            continue
        if month_num < 1 or month_num > 12:
            print("Month must be between 1 and 12. Try again.")
            continue
        return month_num


def get_year(prompt=None, min_year=1950):
    """Collects and validates a year, no later than the current year."""
    current_year = date.today().year
    if prompt is None:
        prompt = f"Year (e.g., {current_year}): "
    while True:
        entry = input(prompt).strip()
        try:
            year_num = int(entry)
        except ValueError:
            print("Please enter a valid year. Try again.")
            continue
        if year_num < min_year or year_num > current_year:
            print(f"Please enter a realistic year ({min_year}-{current_year}). Try again.")
            continue
        return year_num


def get_duration():
    """
    Collects a sanitized duration by asking for a start month/year,
    whether the job is current, and (if not) an end month/year.
    Returns a formatted string, e.g. "Jan 2022 - Present" or
    "Jan 2022 - Mar 2024".
    """
    print("Start date:")
    start_month = get_month("Starting month (1-12): ")
    start_year = get_year("Starting year (e.g., 2022): ")

    while True:
        currently_working = input("Are you currently working here? (yes/no): ").strip().lower()
        if currently_working in ("yes", "y"):
            start_label = f"{calendar.month_abbr[start_month]} {start_year}"
            return f"{start_label} - Present"
        elif currently_working in ("no", "n"):
            print("End date:")
            while True:
                end_month = get_month("Ending month (1-12): ")
                end_year = get_year("Ending year (e.g., 2024): ")
                if (end_year, end_month) < (start_year, start_month):
                    print("End date cannot be before the start date. Try again.")
                    continue
                break
            start_label = f"{calendar.month_abbr[start_month]} {start_year}"
            end_label = f"{calendar.month_abbr[end_month]} {end_year}"
            return f"{start_label} - {end_label}"
        else:
            print("Please enter 'yes' or 'no'.")


def get_single_job_experience(index):
    """Collects one job experience record: company, role, duration, description."""
    print(f"\n--- Job Experience #{index} ---")

    while True:
        company = input("Company name: ").strip()
        if not company:
            print("Company name cannot be empty. Try again.")
            continue
        break

    while True:
        role = input("Job title/role: ").strip()
        if not role:
            print("Job title cannot be empty. Try again.")
            continue
        break

    duration = get_duration()

    while True:
        description = input("Brief description of responsibilities/achievements: ").strip()
        if not description:
            print("Description cannot be empty. Try again.")
            continue
        break

    return {
        "company": company,
        "role": role,
        "duration": duration,
        "description": description,
    }


def get_job_experiences():
    """
    Collects a list of job experiences by repeatedly calling
    get_single_job_experience(). This field is optional overall:
    the user can choose to skip it entirely and end up with an
    empty list.
    """
    experiences = []

    while True:
        has_experience = input(
            "\nDo you have any work experience you'd like to add? (yes/no): "
        ).strip().lower()
        if has_experience in ("yes", "y"):
            break
        elif has_experience in ("no", "n"):
            return experiences
        else:
            print("Please enter 'yes' or 'no'.")

    print("\nLet's add your work experience.")
    while True:
        experiences.append(get_single_job_experience(len(experiences) + 1))
        while True:
            again = input("\nAdd another job experience? (yes/no): ").strip().lower()
            if again in ("yes", "y"):
                break
            elif again in ("no", "n"):
                return experiences
            else:
                print("Please enter 'yes' or 'no'.")


# ---------------------------------------------------------------------------
# Top-level collector
# ---------------------------------------------------------------------------

def collect_resume_input():
    """
    Runs the full input flow and returns a single dict containing
    all validated resume data, ready to be handed off to the
    AI Manager / Logic Manager / Data Manager.
    """
    print("=" * 50)
    print("       RESUME CREATOR — LET'S GET STARTED")
    print("=" * 50)

    name = get_name()
    age = get_age()
    email = get_email()
    phone = get_phone()
    location = get_location()
    qualification = get_qualification()
    skills = get_skills()
    job_experiences = get_job_experiences()
    desired_job = get_desired_job_description()
    portfolio_url = get_linkedin_or_portfolio()

    record = {
        "name": name,
        "age": age,
        "email": email,
        "phone": phone,
        "location": location,
        "qualification": qualification,
        "skills": skills,
        "job_experiences": job_experiences,
        "desired_job": desired_job,
        "portfolio_url": portfolio_url,
    }

    record = review_and_confirm(record)
    return record


# ---------------------------------------------------------------------------
# Review, edit, and final confirmation
# ---------------------------------------------------------------------------

def edit_field(record):
    """Displays a menu of fields and lets the user re-collect the one they pick."""
    fields = {
        "1": "name",
        "2": "age",
        "3": "email",
        "4": "phone",
        "5": "location",
        "6": "qualification",
        "7": "skills",
        "8": "job_experiences",
        "9": "desired_job",
        "10": "portfolio_url",
    }

    print("\nWhich field would you like to fix?")
    for key, value in fields.items():
        print(f"  {key}. {value.replace('_', ' ').title()}")

    while True:
        choice = input("Enter choice: ").strip()
        if choice not in fields:
            print("Invalid choice. Try again.")
            continue
        break

    field = fields[choice]

    if field == "name":
        record["name"] = get_name()
    elif field == "age":
        record["age"] = get_age()
    elif field == "email":
        record["email"] = get_email()
    elif field == "phone":
        record["phone"] = get_phone()
    elif field == "location":
        record["location"] = get_location()
    elif field == "qualification":
        record["qualification"] = get_qualification()
    elif field == "skills":
        record["skills"] = get_skills()
    elif field == "job_experiences":
        record["job_experiences"] = get_job_experiences()
    elif field == "desired_job":
        record["desired_job"] = get_desired_job_description()
    elif field == "portfolio_url":
        record["portfolio_url"] = get_linkedin_or_portfolio()

    return record


def review_and_confirm(record):
    """
    Shows the collected data, lets the user correct any field as many
    times as needed, then issues a final warning that the next
    confirmation locks the submission in before returning the record.
    """
    while True:
        print_summary(record)

        choice = input(
            "\nWould you like to correct any information above? (yes/no): "
        ).strip().lower()
        while choice not in ("yes", "y", "no", "n"):
            choice = input("Please enter 'yes' or 'no': ").strip().lower()

        if choice in ("yes", "y"):
            record = edit_field(record)
            continue

        print("\n" + "!" * 50)
        print("WARNING: This is your LAST CHANCE to make changes.")
        print("Once confirmed, your submission will be final.")
        print("!" * 50)

        final_confirm = input(
            "Are you sure you want to submit this information as final? (yes/no): "
        ).strip().lower()
        while final_confirm not in ("yes", "y", "no", "n"):
            final_confirm = input("Please enter 'yes' or 'no': ").strip().lower()

        if final_confirm in ("yes", "y"):
            print("\nYour information has been submitted successfully.")
            return record
        # If "no", loop back to show the summary and allow more edits.


# ---------------------------------------------------------------------------
# Output / formatting
# ---------------------------------------------------------------------------

def print_summary(record):
    """Formats and prints a summary of the collected resume data."""
    print("\n" + "=" * 50)
    print("             INPUT SUMMARY")
    print("=" * 50)
    print(f"Name:            {record['name']}")
    print(f"Age:             {record['age']}")
    print(f"Email:           {record['email']}")
    print(f"Phone:           {record['phone']}")
    print(f"Location:        {record['location']}")#Optional
    print(f"Qualification:   {record['qualification']}")
    print(f"Skills:          {', '.join(record['skills'])}")
    print(f"Desired Job:     {record['desired_job']}")
    print(f"Portfolio/URL:   {record['portfolio_url'] or 'Not provided'}")#Optional
    if record["job_experiences"]:
        print(f"\nWork Experience ({len(record['job_experiences'])} entries):")#Optional
        for i, job in enumerate(record["job_experiences"], start=1):
            print(f"  {i}. {job['role']} at {job['company']} ({job['duration']})")
            print(f"     {job['description']}")
    else:
        print("\nWork Experience:  None provided")
    print("=" * 50)