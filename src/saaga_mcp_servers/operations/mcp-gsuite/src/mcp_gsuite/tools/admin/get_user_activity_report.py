import json
import asyncio
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from mcp_gsuite.lib.accounts import format_docstring_with_user_id_arg
from googleapiclient.discovery import build
from mcp_gsuite.lib.auth import credentials as cred_module
from loguru import logger


@format_docstring_with_user_id_arg
async def get_user_activity_report(
    user_id: str,
    user_key: Optional[str] = "all",
    application_name: Optional[str] = "gmail",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    max_results: int = 100,
) -> str:
    """
    Retrieve user activity reports from Google Admin Reports API for any Google Workspace application.

    Args:
        user_id: {user_id_arg}
        user_key: The user whose activities to retrieve (email or 'all' for all users)
        application_name: Application to get logs for ('gmail', 'drive', 'calendar', 'login', 'admin', etc.)
                         If not specified, returns activities for all applications
        start_time: Start time in ISO format (e.g., '2024-01-01T00:00:00Z'). Defaults to 24 hours ago.
        end_time: End time in ISO format. Defaults to now.
        max_results: Maximum number of log entries to retrieve (1-1000, default 100)

    Available applications:
    - gmail: Email activities (send, receive, delete, etc.)
    - drive: Drive activities (create, edit, share, delete files)
    - calendar: Calendar activities (create, edit, delete events)
    - login: Login activities (successful login, failed login, logout)
    - admin: Admin console activities (user management, settings changes)
    - token: OAuth token activities (authorize, revoke)
    - groups: Groups activities (create, delete, membership changes)
    - mobile: Mobile device activities
    - meet: Google Meet activities
    """
    logger.info(
        f"Retrieving activity report for admin user: {user_id}, target user: {user_key}, app: {application_name}"
    )

    try:
        # Get credentials for the admin user
        creds_obj = cred_module.get_stored_credentials(user_email=user_id)
        if not creds_obj:
            raise RuntimeError(
                f"No OAuth2 credentials stored for admin user: {user_id}"
            )

        # Build the Admin Reports service
        service = build("admin", "reports_v1", credentials=creds_obj)

        # Set default time range if not provided
        if not end_time:
            end_time = datetime.utcnow().isoformat() + "Z"
        if not start_time:
            start_time = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"

        all_activities = []

        # If no specific application, get activities for common applications
        applications = (
            [application_name]
            if application_name
            else ["gmail", "drive", "calendar", "login", "admin"]
        )

        for app in applications:
            try:
                # Build the request parameters
                params = {
                    "userKey": user_key,
                    "applicationName": app,
                    "startTime": start_time,
                    "endTime": end_time,
                    "maxResults": min(max_results, 1000),
                }

                logger.debug(f"Fetching {app} activities with params: {params}")

                # Execute the request
                activities = []
                request = service.activities().list(**params)

                while request and len(activities) < max_results:
                    response = await asyncio.to_thread(request.execute)

                    if "items" in response:
                        activities.extend(response["items"])
                        logger.info(
                            f"Retrieved {len(response['items'])} {app} activities"
                        )

                    # Check for next page
                    request = service.activities().list_next(request, response)

                    # Stop if we've reached max_results for this app
                    if len(activities) >= max_results:
                        activities = activities[:max_results]
                        break

                # Add application name to each activity
                for activity in activities:
                    activity["applicationName"] = app

                all_activities.extend(activities)

            except Exception as e:
                logger.warning(f"Failed to get {app} activities: {str(e)}")
                continue

        # Sort all activities by time (newest first)
        all_activities.sort(key=lambda x: x.get("id", {}).get("time", ""), reverse=True)

        # Limit to max_results
        if len(all_activities) > max_results:
            all_activities = all_activities[:max_results]

        # Process and format the activities
        formatted_activities = []
        for activity in all_activities:
            activity_entry = {
                "id": activity.get("id", {}).get("uniqueQualifier"),
                "time": activity.get("id", {}).get("time"),
                "application": activity.get("applicationName"),
                "user": activity.get("actor", {}).get("email"),
                "ip_address": activity.get("ipAddress"),
                "events": [],
            }

            # Extract event details
            for event in activity.get("events", []):
                event_info = {
                    "name": event.get("name"),
                    "type": event.get("type"),
                    "parameters": {},
                }

                # Extract parameters with better formatting
                for param in event.get("parameters", []):
                    param_name = param.get("name")
                    param_value = (
                        param.get("value")
                        or param.get("multiValue")
                        or param.get("boolValue")
                    )

                    # Special handling for common parameters
                    if param_name in ["doc_title", "doc_name", "message_subject"]:
                        event_info["parameters"][param_name] = param_value
                    elif param_name == "visibility":
                        event_info["parameters"]["visibility"] = param_value
                    else:
                        event_info["parameters"][param_name] = param_value

                activity_entry["events"].append(event_info)

            formatted_activities.append(activity_entry)

        # Group activities by application
        activities_by_app = {}
        for activity in formatted_activities:
            app = activity["application"]
            if app not in activities_by_app:
                activities_by_app[app] = []
            activities_by_app[app].append(activity)

        result = {
            "total_activities": len(formatted_activities),
            "time_range": {"start": start_time, "end": end_time},
            "user_filter": user_key,
            "applications_queried": applications,
            "activities_by_application": {
                app: len(activities) for app, activities in activities_by_app.items()
            },
            "activities": formatted_activities,
        }

        logger.info(
            f"Successfully retrieved {len(formatted_activities)} activities for admin: {user_id}"
        )
        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(
            f"Error retrieving user activity report for admin: {user_id}. Error: {str(e)}",
            exc_info=True,
        )
        error_response = {
            "error": f"Failed to retrieve user activity report: {str(e)}",
            "user_id": user_id,
            "user_key": user_key,
        }
        raise Exception(json.dumps(error_response, indent=2))
