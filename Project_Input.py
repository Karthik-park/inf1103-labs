import re


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
    """Collects and validates a phone number (digits, spaces, +, -, () allowed)."""
    pattern = r"^[\d\s\+\-\(\)]{7,20}$"
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
# Job experience (repeatable entry)
# ---------------------------------------------------------------------------

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

    while True:
        duration = input("Duration (e.g., 'Jan 2022 - Mar 2024'): ").strip()
        if not duration:
            print("Duration cannot be empty. Try again.")
            continue
        break

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
    """Collects a list of job experiences by repeatedly calling get_single_job_experience()."""
    experiences = []
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

    print_summary(record)
    return record


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
    print(f"Location:        {record['location']}")
    print(f"Qualification:   {record['qualification']}")
    print(f"Skills:          {', '.join(record['skills'])}")
    print(f"Desired Job:     {record['desired_job']}")
    print(f"Portfolio/URL:   {record['portfolio_url'] or 'Not provided'}")
    print(f"\nWork Experience ({len(record['job_experiences'])} entries):")
    for i, job in enumerate(record["job_experiences"], start=1):
        print(f"  {i}. {job['role']} at {job['company']} ({job['duration']})")
        print(f"     {job['description']}")
    print("=" * 50)