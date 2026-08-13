"""
Job-to-profile matching engine.

Version 0.1 uses deterministic rules rather than an LLM.
This makes the scoring transparent and easy to test.
"""

from typing import Any

from .rules import (
    APPLY_THRESHOLD,
    EXPERIENCE_MATCH_POINTS,
    EXPERIENCE_PENALTY_2_PLUS,
    EXPERIENCE_PENALTY_3_PLUS,
    EXPERIENCE_PENALTY_SENIOR,
    JOB_TYPE_MATCH_POINTS,
    LOCATION_MATCH_POINTS,
    ROLE_MATCH_POINTS,
    REVIEW_THRESHOLD,
    SKILL_MATCH_POINTS,
    get_decision,
)


def normalize(value: str) -> str:
    """Normalize text for comparison."""
    return value.strip().lower()


def calculate_role_match(
    job_title: str,
    target_roles: list[str],
) -> tuple[int, list[str]]:
    """Calculate role-match points."""

    normalized_title = normalize(job_title)

    for role in target_roles:
        normalized_role = normalize(role)

        if normalized_role in normalized_title:
            return ROLE_MATCH_POINTS, [f"Target role match: {role}"]

    return 0, []


def calculate_skill_match(
    job_skills: list[str],
    candidate_skills: list[str],
) -> tuple[int, list[str]]:
    """Calculate skill-match points."""

    candidate_skill_set = {
        normalize(skill)
        for skill in candidate_skills
    }

    matched_skills = []

    for skill in job_skills:
        if normalize(skill) in candidate_skill_set:
            matched_skills.append(skill)

    if not job_skills:
        return 0, []

    # Skill points are proportional to the number of matched skills.
    points = round(
        (len(matched_skills) / len(job_skills))
        * SKILL_MATCH_POINTS
    )

    reasons = [
        f"Skill match: {skill}"
        for skill in matched_skills
    ]

    return points, reasons


def calculate_experience_match(
    required_years: float | None,
    candidate_years: float,
    seniority: str | None = None,
) -> tuple[int, list[str], int]:
    """Calculate experience points and penalties."""

    reasons = []
    penalty = 0

    seniority_normalized = normalize(seniority or "")

    if "senior" in seniority_normalized:
        penalty = EXPERIENCE_PENALTY_SENIOR
        reasons.append("Senior-level role")

    elif required_years is not None:

        if required_years >= 3:
            penalty = EXPERIENCE_PENALTY_3_PLUS
            reasons.append(
                f"Requires {required_years:g}+ years"
            )

        elif required_years >= 2:
            penalty = EXPERIENCE_PENALTY_2_PLUS
            reasons.append(
                f"Requires {required_years:g}+ years"
            )

        elif required_years <= candidate_years:
            reasons.append("Experience requirement satisfied")

        else:
            reasons.append(
                "Experience requirement may exceed candidate level"
            )

    else:
        reasons.append("No explicit experience requirement")

    points = EXPERIENCE_MATCH_POINTS if penalty == 0 else 0

    return points, reasons, penalty


def calculate_location_match(
    job_location: str,
    candidate_location: str,
    remote_allowed: bool,
) -> tuple[int, list[str]]:
    """Calculate location-match points."""

    location = normalize(job_location)
    candidate = normalize(candidate_location)

    if remote_allowed and (
        "remote" in location
        or "work from home" in location
        or "wfh" in location
    ):
        return LOCATION_MATCH_POINTS, ["Remote role"]

    if candidate in location:
        return LOCATION_MATCH_POINTS, [
            f"Location match: {candidate_location}"
        ]

    return 0, []


def calculate_job_type_match(
    job_type: str,
    accepted_job_types: list[str],
) -> tuple[int, list[str]]:
    """Calculate job-type points."""

    normalized_type = normalize(job_type)

    for accepted_type in accepted_job_types:
        if normalize(accepted_type) in normalized_type:
            return JOB_TYPE_MATCH_POINTS, [
                f"Job type accepted: {accepted_type}"
            ]

    return 0, []


def calculate_match(
    job: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate the overall job match.

    Returns:
        A dictionary containing score, decision and explanations.
    """

    score = 0
    reasons: list[str] = []
    penalties: list[str] = []

    # Role
    role_points, role_reasons = calculate_role_match(
        job.get("title", ""),
        profile.get("target_roles", []),
    )

    score += role_points
    reasons.extend(role_reasons)

    # Skills
    skill_points, skill_reasons = calculate_skill_match(
        job.get("skills", []),
        profile.get("skills", []),
    )

    score += skill_points
    reasons.extend(skill_reasons)

    # Experience
    experience = profile.get("experience", {})

    experience_points, experience_reasons, experience_penalty = (
        calculate_experience_match(
            job.get("required_years"),
            experience.get("years", 0),
            job.get("seniority"),
        )
    )

    score += experience_points
    score -= experience_penalty

    reasons.extend(experience_reasons)

    if experience_penalty:
        penalties.extend(experience_reasons)

    # Location
    location = profile.get("location", {})

    location_points, location_reasons = calculate_location_match(
        job.get("location", ""),
        location.get("primary", ""),
        location.get("remote", False),
    )

    score += location_points
    reasons.extend(location_reasons)

    # Job type
    job_type_points, job_type_reasons = calculate_job_type_match(
        job.get("job_type", ""),
        profile.get("job_types", []),
    )

    score += job_type_points
    reasons.extend(job_type_reasons)

    # Keep score within 0–100.
    score = max(0, min(100, score))

    decision = get_decision(score)

    return {
        "score": score,
        "decision": decision,
        "reasons": reasons,
        "penalties": penalties,
    }