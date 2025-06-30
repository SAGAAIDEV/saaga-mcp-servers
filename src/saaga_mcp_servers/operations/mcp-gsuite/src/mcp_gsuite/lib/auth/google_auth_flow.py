import os
import json
import fire  # Added import for python-fire
import pickle  # Added import for pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import sys
import subprocess  # Added for running shell commands
import platform  # Added for OS detection

# --- External ---
from mcp_gsuite.config.env import gsuite_config  # Added for config
import pydantic  # Added for AccountInfo
from loguru import logger  # Added logger
from .utils import (
    construct_credential_path,
    get_email_from_credentials,
)  # Added import for utils
from .credentials import get_stored_credentials  # Import the existing function

# Logger is now configured centrally in config/logging.py

# --- Configuration ---
# TODO: IMPORTANT - Replace these with the actual scopes you need!
DEFAULT_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/admin.reports.audit.readonly",
    "https://www.googleapis.com/auth/admin.reports.usage.readonly",
]

# USER_TOKEN_FILENAME = "token.json" # No longer a fixed filename


def authenticate(scopes=None, user_email=None):
    """
    Authenticates the user using the Google OAuth 2.0 installed app flow.
    First checks for existing credentials and uses them if valid.
    Only initiates new auth flow if no valid credentials exist.
    Saves the credentials to a file named .oauth2.[user_id].pickle and returns them.

    Args:
        scopes (list, optional): A list of OAuth scopes to request.
                                 Defaults to DEFAULT_SCOPES.
        user_email (str, optional): Email of the user to authenticate.
                                   If provided, will check for existing credentials first.

    Returns:
        google.oauth2.credentials.Credentials: The authenticated credentials,
                                               or None if authentication fails.
    """
    logger.info("Authenticating...")
    
    if scopes is None:
        scopes = DEFAULT_SCOPES

    try:
        client_secret_file_path = str(gsuite_config.get_client_secrets_file())
        credentials_storage_dir = gsuite_config.credentials_dir
        gsuite_config.verify_credentials_dir()  # Ensure the directory exists
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        return None

    os.makedirs(credentials_storage_dir, exist_ok=True)

    creds = None
    email = user_email

    # IMPORTANT FIX: First check for existing stored credentials
    if email:
        logger.info(f"Checking for existing credentials for {email}")
        creds = get_stored_credentials(email)
        if creds and creds.valid:
            logger.info(f"Found valid existing credentials for {email}")
            return creds
        elif creds:
            logger.info(f"Found expired credentials for {email}, will need to re-authenticate")

    # Only start new auth flow if we don't have valid credentials
    if not creds or not creds.valid:
        logger.info("Starting new authentication flow...")
        
        # Kill any existing auth server processes before starting
        kill_local_server(port=8080)
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file_path, scopes
            )
            # Request offline access to ensure we get a refresh token
            creds = flow.run_local_server(
                host="localhost",
                port=8080,
                access_type="offline",
                prompt="consent",  # Force consent screen to ensure refresh token
            )

            if not creds:
                logger.error("Authentication flow did not return credentials.")
                return None
            logger.info("Authentication successful.")

            # Get email if not provided
            if not email:
                email = get_email_from_credentials(creds)
                if not email:
                    logger.error(
                        "Auth successful, but could not extract user ID from credentials. Cannot save token."
                    )
                    return None

            final_token_path = construct_credential_path(email)
            with open(final_token_path, "wb") as token_file:  # Changed to wb for pickle
                pickle.dump(creds, token_file)  # Save as pickle
            logger.info(f"Credentials saved to {final_token_path}")

        except Exception as e:
            path_for_error_log = "unknown path"
            if email:
                try:
                    path_for_error_log = construct_credential_path(email)
                except Exception:
                    pass
                logger.error(
                    f"Error during authentication or saving credentials to {path_for_error_log}: {e}",
                    exc_info=True,
                )
            else:
                logger.error(
                    f"Error during authentication flow or user ID extraction: {e}",
                    exc_info=True,
                )
            return None

    return creds


def kill_local_server(port: int = 8080):
    """
    Attempts to find and kill processes running on the specified port.
    This is useful if the OAuth local server doesn't shut down correctly.
    """
    logger.info(f"Attempting to kill server processes on port {port}...")
    system = platform.system()
    pids_killed_count = 0

    try:
        if system == "Darwin" or system == "Linux":
            # Find PID using lsof
            find_pid_cmd = f"lsof -t -i:{port}"
            logger.debug(f"Executing: {find_pid_cmd}")
            # Setting shell=True can be a security risk if command is from untrusted input.
            # Here, 'port' is an int, so it's safer.
            pid_process = subprocess.run(
                find_pid_cmd, shell=True, capture_output=True, text=True, check=False
            )

            if pid_process.returncode == 0 and pid_process.stdout.strip():
                pids_to_kill = [
                    pid for pid in pid_process.stdout.strip().split("\\n") if pid
                ]
                if not pids_to_kill:
                    logger.info(
                        f"lsof found a match but no PIDs were extracted for port {port}."
                    )
                else:
                    for pid_str in pids_to_kill:
                        pid = pid_str.strip()
                        logger.info(f"Found process with PID {pid} on port {port}")
                        kill_cmd = f"kill -9 {pid}"
                        logger.debug(f"Executing: {kill_cmd}")
                        kill_process = subprocess.run(
                            kill_cmd,
                            shell=True,
                            check=False,
                            capture_output=True,
                            text=True,
                        )
                        if kill_process.returncode == 0:
                            logger.info(f"Successfully killed process with PID {pid}.")
                            pids_killed_count += 1
                        else:
                            logger.warning(
                                f"Failed to kill process with PID {pid}. Exit code: {kill_process.returncode}. Error: {kill_process.stderr.strip()}"
                            )
            elif pid_process.returncode == 1:  # lsof returns 1 if no process is found
                logger.info(f"No process found running on port {port}.")
            else:  # Other errors from lsof
                logger.error(
                    f"Error finding process on port {port} with lsof. Exit code: {pid_process.returncode}. Error: {pid_process.stderr.strip()}"
                )

        elif system == "Windows":
            # Command to find PIDs for connections on the specified port, in LISTENING state
            find_pid_cmd = f'netstat -ano | findstr ":{port}" | findstr "LISTENING"'
            logger.debug(f"Executing: {find_pid_cmd}")
            pid_process = subprocess.run(
                find_pid_cmd, shell=True, capture_output=True, text=True, check=False
            )

            if pid_process.returncode == 0 and pid_process.stdout.strip():
                lines = pid_process.stdout.strip().split("\\n")
                pids_found_on_windows = set()
                for line in lines:
                    parts = line.strip().split()
                    # Example line: TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       12345
                    if "LISTENING" in line.upper() and len(parts) > 0:
                        pid = parts[-1]  # PID is the last part
                        if pid.isdigit():
                            pids_found_on_windows.add(pid)

                if not pids_found_on_windows:
                    logger.info(
                        f"netstat found matches for port {port}, but no PIDs in LISTENING state were extracted."
                    )
                else:
                    for pid in pids_found_on_windows:
                        logger.info(
                            f"Found process with PID {pid} on port {port} (Windows)"
                        )
                        kill_cmd = f"taskkill /PID {pid} /F"
                        logger.debug(f"Executing: {kill_cmd}")
                        kill_process = subprocess.run(
                            kill_cmd,
                            shell=True,
                            check=False,
                            capture_output=True,
                            text=True,
                        )
                        if kill_process.returncode == 0:
                            logger.info(f"Successfully killed process with PID {pid}.")
                            pids_killed_count += 1
                        else:
                            # taskkill can return non-0 if process already terminated, check stderr
                            if "process not found" in kill_process.stderr.lower():
                                logger.info(
                                    f"Process with PID {pid} was already terminated or not found by taskkill."
                                )
                            else:
                                logger.warning(
                                    f"Failed to kill process with PID {pid}. Exit code: {kill_process.returncode}. Error: {kill_process.stderr.strip()}"
                                )
            elif (
                pid_process.returncode == 1
            ):  # findstr returns 1 if the string is not found
                logger.info(f"No process found listening on port {port}.")
            else:  # Other errors from netstat/findstr
                logger.error(
                    f"Error finding process on port {port} with netstat/findstr. Exit code: {pid_process.returncode}. Error: {pid_process.stderr.strip()}"
                )
        else:
            logger.warning(
                f"Unsupported operating system: {system}. Cannot automatically kill server."
            )

    except FileNotFoundError:
        logger.error(
            "Required command (e.g., lsof, netstat, kill, taskkill) not found. Ensure it's in your PATH. Cannot kill server."
        )
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while trying to kill server on port {port}: {e}",
            exc_info=True,
        )

    if pids_killed_count > 0:
        logger.info(
            f"Finished attempt to kill server on port {port}. {pids_killed_count} process(es) were targeted for termination."
        )
    else:
        logger.info(
            f"Finished attempt to kill server on port {port}. No processes were confirmed killed by this script (or none were found running)."
        )


def cli_authenticate_and_print_creds(user_email=None):
    """
    CLI command to authenticate and print credentials.
    
    Args:
        user_email: Optional email to check for existing credentials first
    """
    creds = authenticate(user_email=user_email)
    if creds:
        logger.info("Authentication was successful. Credentials object:")
        logger.info(f"Token: {creds.token}")
        logger.info(f"Refresh Token: {creds.refresh_token}")
        logger.info(f"Token URI: {creds.token_uri}")
        logger.info(f"Client ID: {creds.client_id}")
        logger.info(f"Client Secret: {creds.client_secret}")  # Be careful logging this
        logger.info(f"Scopes: {creds.scopes}")
        email = get_email_from_credentials(creds)
        logger.info(f"Email (from creds): {email if email else 'Not found'}")
    else:
        logger.error("Authentication failed or was cancelled.")


def main():
    logger.info("Google Auth Flow CLI")
    fire.Fire(
        {
            "auth": cli_authenticate_and_print_creds,
            "kill_server": kill_local_server,
        }
    )


if __name__ == "__main__":
    logger.info("Google Auth Flow CLI")
    main()
