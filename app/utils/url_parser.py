"""
URL parsing and validation utilities.
"""

import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse

class URLParser:
    """
    Utility class for parsing and validating URLs.
    """
    
    @staticmethod
    def extract_github_repo(url: str) -> Optional[str]:
        """
        Extract repository name from GitHub URL.
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Repository name in format 'owner/repo' or None if invalid
        """
        if not url:
            return None
        
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com/([^/]+/[^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+/[^/]+?)(?:/.*)?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                repo_name = match.group(1)
                # Remove trailing .git if present
                if repo_name.endswith('.git'):
                    repo_name = repo_name[:-4]
                return repo_name
        
        return None
    
    @staticmethod
    def validate_github_url(url: str) -> bool:
        """
        Validate if URL is a valid GitHub repository URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid GitHub URL, False otherwise
        """
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            if parsed.netloc.lower() not in ['github.com', 'www.github.com']:
                return False
            
            # Check if we can extract a repo name
            return URLParser.extract_github_repo(url) is not None
        except Exception:
            return False
    
    @staticmethod
    def validate_hackathon_url(url: str) -> bool:
        """
        Validate if URL looks like a hackathon website.
        
        Args:
            url: URL to validate
            
        Returns:
            True if likely a hackathon URL, False otherwise
        """
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
            
            # Check for common hackathon domains
            hackathon_domains = [
                'devpost.com',
                'hackathon.com',
                'mlh.io',
                'hackerearth.com',
                'eventbrite.com'
            ]
            
            domain = parsed.netloc.lower()
            for hackathon_domain in hackathon_domains:
                if hackathon_domain in domain:
                    return True
            
            # Check for hackathon-related keywords in URL
            hackathon_keywords = ['hack', 'hackathon', 'challenge', 'competition']
            url_lower = url.lower()
            
            return any(keyword in url_lower for keyword in hackathon_keywords)
        except Exception:
            return False
    
    @staticmethod
    def parse_url_info(url: str) -> Dict[str, Any]:
        """
        Parse URL and extract useful information.
        
        Args:
            url: URL to parse
            
        Returns:
            Dictionary with URL information
        """
        if not url:
            return {"valid": False, "type": "unknown"}
        
        try:
            parsed = urlparse(url)
            
            info = {
                "valid": True,
                "original_url": url,
                "domain": parsed.netloc.lower(),
                "path": parsed.path,
                "type": "unknown"
            }
            
            # Determine URL type
            if URLParser.validate_github_url(url):
                info["type"] = "github"
                info["repo_name"] = URLParser.extract_github_repo(url)
            elif URLParser.validate_hackathon_url(url):
                info["type"] = "hackathon"
            else:
                info["type"] = "website"
            
            return info
        except Exception as e:
            return {
                "valid": False,
                "type": "unknown",
                "error": str(e)
            }