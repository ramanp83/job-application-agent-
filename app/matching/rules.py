"""
Matching rules for the personal job application agent.

These rules define how job requirements are compared
against the candidate profile.
"""

# Maximum points available for each matching category.
ROLE_MATCH_POINTS = 25
EXPERIENCE_MATCH_POINTS = 20
SKILL_MATCH_POINTS = 40
LOCATION_MATCH_POINTS = 10
JOB_TYPE_MATCH_POINTS = 5

# Penalties
EXPERIENCE_PENALTY_2_PLUS = 30
EXPERIENCE_PENALTY_3_PLUS = 40
EXPERIENCE_PENALTY_SENIOR = 50


# Decision thresholds
APPLY_THRESHOLD = 80
REVIEW_THRESHOLD = 70


def get_decision(score: int) -> str:
    """Return an application recommendation from a match score."""

    if score >= APPLY_THRESHOLD:
        return "APPLY"

    if score >= REVIEW_THRESHOLD:
        return "REVIEW"

    return "SKIP"