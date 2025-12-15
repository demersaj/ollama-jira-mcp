#!/usr/bin/env python3
"""
Script to remove acceptance criteria from DEVEX user stories.
This script processes issues and removes acceptance criteria sections.
"""

import re
import sys

def remove_acceptance_criteria(description):
    """
    Remove acceptance criteria sections from description.
    Handles various formats:
    - h2. Acceptance Criteria
    - *Acceptance Criteria:*
    - Acceptance Criteria:
    - h2. Acceptance Criteria (with various markdown formats)
    """
    if not description:
        return description
    
    # Patterns to match acceptance criteria sections
    patterns = [
        # h2. Acceptance Criteria followed by content until next h2 or end
        r'\n\nh2\.\s*Acceptance\s+Criteria.*?(?=\n\nh2\.|\n\n\*|$)',
        # *Acceptance Criteria:* followed by bullet points
        r'\n\n\*Acceptance\s+Criteria:\*.*?(?=\n\n\*Success|\n\nh2\.|$)',
        # Acceptance Criteria: (without h2)
        r'\n\nAcceptance\s+Criteria:.*?(?=\n\n\*Success|\n\nh2\.|$)',
        # Success Metrics section (also remove if present)
        r'\n\n\*Success\s+Metrics:\*.*?(?=\n\nh2\.|$)',
        r'\n\nh2\.\s*Success\s+Metrics.*?(?=\n\nh2\.|$)',
    ]
    
    result = description
    for pattern in patterns:
        result = re.sub(pattern, '', result, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up any double newlines
    result = re.sub(r'\n\n\n+', '\n\n', result)
    
    return result.strip()

def format_description(description):
    """
    Ensure description follows the format:
    - User story line (As a...)
    - h2. Description
    - Description text
    """
    if not description:
        return description
    
    # Check if it starts with user story format
    user_story_match = re.match(r'^(\*?As\s+a\s+.*?so\s+.*?\*?)\n', description, re.IGNORECASE | re.DOTALL)
    
    if user_story_match:
        user_story_line = user_story_match.group(1).strip()
        # Remove asterisks if present
        user_story_line = user_story_line.strip('*')
        
        # Get the rest
        rest = description[user_story_match.end():].strip()
        
        # Check if h2. Description already exists
        if re.match(r'^h2\.\s*Description', rest, re.IGNORECASE):
            # Already formatted correctly, just clean it
            return f"{user_story_line}\n\n{rest}"
        else:
            # Need to add h2. Description
            return f"{user_story_line}\n\nh2. Description\n\n{rest}"
    
    return description

def process_description(description):
    """Process description: remove acceptance criteria and format correctly."""
    if not description:
        return description
    
    # First remove acceptance criteria
    cleaned = remove_acceptance_criteria(description)
    
    # Then format correctly
    formatted = format_description(cleaned)
    
    return formatted

if __name__ == "__main__":
    # This is a utility module - actual execution will be done via Jira API calls
    # Test with sample descriptions
    test_cases = [
        """As a developer, I want X so Y

h2. Description

Some description here.

h2. Acceptance Criteria
* Item 1
* Item 2""",
        """*As a developer, I want X so Y*

Description here.

*Acceptance Criteria:*
* Item 1
* Item 2

*Success Metrics:*
* Metric 1"""
    ]
    
    for test in test_cases:
        print("Original:")
        print(test)
        print("\nProcessed:")
        print(process_description(test))
        print("\n" + "="*50 + "\n")

