import os
from ...config.env import gsuite_config
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from loguru import logger
import pickle


def _get_credential_filename(user_id: str) -> str:
    path = os.path.join(gsuite_config.credentials_dir, f".oauth2.{user_id}.pickle")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Credential file does not exist: {path}")
    return path


def save_credentials(user_email: str, creds: Credentials) -> None:
    """Save credentials to file."""
    try:
        cred_file_path = os.path.join(gsuite_config.credentials_dir, f".oauth2.{user_email}.pickle")
        with open(cred_file_path, "wb") as f:
            pickle.dump(creds, f)
        logger.info(f"Saved refreshed credentials for {user_email}")
    except Exception as e:
        logger.error(f"Error saving credentials for user {user_email}: {e}")
        raise


def get_stored_credentials(user_email: str) -> Credentials | None:
    """Retrieved stored credentials for the provided user ID.
    
    This function will automatically refresh expired tokens if a valid
    refresh token is available.

    Args:
    user_id: User's ID.
    Returns:
    Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
    """
    try:
        cred_file_path = _get_credential_filename(user_id=user_email)
        logger.info(f"Loading credentials from {cred_file_path}")
        with open(cred_file_path, "rb") as f:
            creds = pickle.load(f)
        
        # Check if credentials are expired and refresh if needed
        if creds and creds.expired and creds.refresh_token:
            logger.info(f"Access token expired for {user_email}, refreshing...")
            try:
                creds.refresh(Request())
                # Save the refreshed credentials back to file
                save_credentials(user_email, creds)
                logger.info(f"Successfully refreshed credentials for {user_email}")
            except Exception as e:
                logger.error(f"Failed to refresh credentials for {user_email}: {e}")
                # If refresh fails, return None so user can re-authenticate
                return None
        elif creds and not creds.valid:
            logger.warning(f"Credentials for {user_email} are not valid and cannot be refreshed")
            return None
            
        return creds
    except FileNotFoundError:
        logger.warning(
            f"No stored Oauth2 credentials yet at path for user: {user_email}"
        )
        return None
    except Exception as e:
        logger.error(f"Error loading credentials for user {user_email}: {e}")
        raise
