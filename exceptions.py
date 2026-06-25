class JarvisException(Exception):
    """Root fallback catch classification domain."""
    pass

class AudioHardwareError(JarvisException):
    """Raised when hardware capture profiles encounter failures."""
    pass

class ExternalAPIError(JarvisException):
    """Raised when network handshakes fail to return valid payloads."""
    pass