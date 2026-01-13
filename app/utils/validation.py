"""
Input validation utilities.
"""

from typing import Optional, Dict, Any, List
from .url_parser import URLParser

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

def validate_inputs(
    github_url: Optional[str] = None,
    hackathon_url: Optional[str] = None,
    hackathon_context: Optional[str] = None,
    search_topic: Optional[str] = None,
    search_order: str = "projects_first"
) -> Dict[str, Any]:
    """
    Validate and normalize inputs for revamp functions.
    
    Args:
        github_url: GitHub repository URL
        hackathon_url: Hackathon website URL
        hackathon_context: Additional hackathon context
        search_topic: Search topic for discovery
        search_order: Discovery order
        
    Returns:
        Dictionary with validated and normalized inputs
        
    Raises:
        ValidationError: If validation fails
    """
    errors = []
    warnings = []
    
    # Validate GitHub URL
    if github_url:
        if not URLParser.validate_github_url(github_url):
            errors.append(f"Invalid GitHub URL: {github_url}")
        else:
            repo_name = URLParser.extract_github_repo(github_url)
            if not repo_name:
                errors.append(f"Could not extract repository name from: {github_url}")
    
    # Validate hackathon URL
    if hackathon_url:
        if not URLParser.validate_hackathon_url(hackathon_url):
            warnings.append(f"URL may not be a hackathon website: {hackathon_url}")
    
    # Validate search order
    valid_search_orders = ["projects_first", "hackathons_first"]
    if search_order not in valid_search_orders:
        errors.append(f"Invalid search_order: {search_order}. Must be one of: {valid_search_orders}")
    
    # Check if we have enough information
    if not github_url and not hackathon_url and not search_topic:
        errors.append("Must provide at least one of: github_url, hackathon_url, or search_topic")
    
    # Validate search topic
    if search_topic:
        if len(search_topic.strip()) < 2:
            errors.append("Search topic must be at least 2 characters long")
        if len(search_topic) > 100:
            warnings.append("Search topic is very long, consider shortening it")
    
    # Validate hackathon context
    if hackathon_context and len(hackathon_context) > 1000:
        warnings.append("Hackathon context is very long, consider shortening it")
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    return {
        "github_url": github_url,
        "hackathon_url": hackathon_url,
        "hackathon_context": hackathon_context,
        "search_topic": search_topic,
        "search_order": search_order,
        "warnings": warnings,
        "github_repo_name": URLParser.extract_github_repo(github_url) if github_url else None
    }

def validate_implementation_inputs(
    github_url: Optional[str] = None,
    implement_changes: bool = False,
    fork_repo: bool = False,
    branch_name: str = "hackathon-revamp"
) -> Dict[str, Any]:
    """
    Validate inputs specific to implementation functionality.
    
    Args:
        github_url: GitHub repository URL
        implement_changes: Whether to implement changes
        fork_repo: Whether to fork repository
        branch_name: Branch name for changes
        
    Returns:
        Dictionary with validated inputs
        
    Raises:
        ValidationError: If validation fails
    """
    errors = []
    warnings = []
    
    if implement_changes:
        if not github_url:
            errors.append("github_url is required when implement_changes=True")
        elif not URLParser.validate_github_url(github_url):
            errors.append(f"Invalid GitHub URL for implementation: {github_url}")
    
    # Validate branch name
    if branch_name:
        # Basic branch name validation
        if not re.match(r'^[a-zA-Z0-9._/-]+$', branch_name):
            errors.append(f"Invalid branch name: {branch_name}")
        if len(branch_name) > 100:
            errors.append("Branch name is too long (max 100 characters)")
        if branch_name.startswith('-') or branch_name.endswith('-'):
            errors.append("Branch name cannot start or end with hyphen")
    
    if fork_repo and not implement_changes:
        warnings.append("fork_repo=True has no effect when implement_changes=False")
    
    if errors:
        raise ValidationError(f"Implementation validation failed: {'; '.join(errors)}")
    
    return {
        "github_url": github_url,
        "implement_changes": implement_changes,
        "fork_repo": fork_repo,
        "branch_name": branch_name,
        "warnings": warnings,
        "github_repo_name": URLParser.extract_github_repo(github_url) if github_url else None
    }