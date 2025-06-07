from ambient.config.settings import config


def get_procurement_prompt(issue_key: str) -> str:
    """
    Generate procurement prompt by reading the procurement.md template
    and formatting it with the issue key.

    Args:
        issue_key: The Jira issue key to include in the prompt

    Returns:
        Formatted prompt string
    """
    procurement_prompt_path = config.prompt_dir / "procurement.md"

    with open(procurement_prompt_path, "r") as f:
        procurement_template = f.read()

    prompt = f"""
{procurement_template}

Complete jira issue: {issue_key}
"""

    return prompt
