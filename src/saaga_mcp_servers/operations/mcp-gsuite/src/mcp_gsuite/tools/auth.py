from mcp_gsuite.lib.auth.google_auth_flow import authenticate
from mcp_gsuite.lib.auth.utils import get_email_from_credentials


async def auth(user_email=None):
    """
    Authenticate with Google services. If user_email is provided, will check
    for existing credentials first before starting a new auth flow.
    
    Args:
        user_email: Optional email to check for existing credentials
    """
    creds = authenticate(user_email=user_email)
    if creds:
        email = get_email_from_credentials(creds)
        if email:
            return f"Successfully authenticated {email}"
        else:
            return "Authentication successful, but failed to retrieve email."
    else:
        return None
