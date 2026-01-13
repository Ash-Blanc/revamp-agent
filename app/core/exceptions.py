"""
Custom exceptions for the Revamp Agent.
"""

class RevampError(Exception):
    """Base exception for all revamp-related errors."""
    pass

class ConfigurationError(RevampError):
    """Raised when there's a configuration issue."""
    pass

class APIError(RevampError):
    """Raised when there's an API-related error."""
    pass

class DiscoveryError(RevampError):
    """Raised when discovery tools fail."""
    pass

class ImplementationError(RevampError):
    """Raised when code implementation fails."""
    pass