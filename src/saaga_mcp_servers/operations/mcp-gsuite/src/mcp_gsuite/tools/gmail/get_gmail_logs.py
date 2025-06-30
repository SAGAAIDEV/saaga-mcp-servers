import json
import asyncio
from typing import Optional, List
from datetime import datetime, timedelta
from mcp_gsuite.lib.accounts import format_docstring_with_user_id_arg
from googleapiclient.discovery import build
from mcp_gsuite.lib.auth import credentials as cred_module
from loguru import logger


@format_docstring_with_user_id_arg
async def get_gmail_logs(
    user_id: str,
    user_key: Optional[str] = "all",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_name: Optional[str] = None,
    filters: Optional[str] = None,
    max_results: int = 100,
) -> str:
    """
    Retrieve Gmail audit logs from Google Admin Reports API.
    
    Args:
        user_id: {user_id_arg}
        user_key: The user whose activities to retrieve (email or 'all' for all users)
        start_time: Start time in ISO format (e.g., '2024-01-01T00:00:00Z'). Defaults to 24 hours ago.
        end_time: End time in ISO format. Defaults to now.
        event_name: Specific Gmail event to filter (e.g., 'email_sent', 'email_received', 'email_deleted')
        filters: Additional filters in the format "parameter==value" (e.g., "message_id==123")
        max_results: Maximum number of log entries to retrieve (1-1000, default 100)
    
    Common Gmail event names:
    - email_sent: Email sent by user
    - email_received: Email received
    - email_deleted: Email permanently deleted
    - email_trash: Email moved to trash
    - email_untrash: Email removed from trash
    - email_spam: Email marked as spam
    - email_unspam: Email unmarked as spam
    - download_attachment: Attachment downloaded
    - upload_attachment: Attachment uploaded
    """
    logger.info(
        f"Retrieving Gmail logs for admin user: {user_id}, target user: {user_key}"
    )
    
    try:
        # Get credentials for the admin user
        creds_obj = cred_module.get_stored_credentials(user_email=user_id)
        if not creds_obj:
            raise RuntimeError(f"No OAuth2 credentials stored for admin user: {user_id}")
        
        # Build the Admin Reports service
        service = build("admin", "reports_v1", credentials=creds_obj)
        
        # Set default time range if not provided
        if not end_time:
            end_time = datetime.utcnow().isoformat() + "Z"
        if not start_time:
            start_time = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
        
        # Build the request parameters
        params = {
            "userKey": user_key,
            "applicationName": "gmail",
            "startTime": start_time,
            "endTime": end_time,
            "maxResults": min(max_results, 1000)
        }
        
        # Add optional parameters
        if event_name:
            params["eventName"] = event_name
        if filters:
            params["filters"] = filters
        
        logger.debug(f"Request parameters: {params}")
        
        # Execute the request
        activities = []
        request = service.activities().list(**params)
        
        while request and len(activities) < max_results:
            response = await asyncio.to_thread(request.execute)
            
            if "items" in response:
                activities.extend(response["items"])
                logger.info(f"Retrieved {len(response['items'])} log entries")
            
            # Check for next page
            request = service.activities().list_next(request, response)
            
            # Stop if we've reached max_results
            if len(activities) >= max_results:
                activities = activities[:max_results]
                break
        
        # Process and format the activities
        formatted_logs = []
        for activity in activities:
            log_entry = {
                "id": activity.get("id", {}).get("uniqueQualifier"),
                "time": activity.get("id", {}).get("time"),
                "user": activity.get("actor", {}).get("email"),
                "ip_address": activity.get("ipAddress"),
                "events": []
            }
            
            # Extract event details
            for event in activity.get("events", []):
                event_info = {
                    "name": event.get("name"),
                    "type": event.get("type"),
                    "parameters": {}
                }
                
                # Extract parameters
                for param in event.get("parameters", []):
                    param_name = param.get("name")
                    param_value = param.get("value") or param.get("multiValue")
                    event_info["parameters"][param_name] = param_value
                
                log_entry["events"].append(event_info)
            
            formatted_logs.append(log_entry)
        
        result = {
            "total_logs": len(formatted_logs),
            "time_range": {
                "start": start_time,
                "end": end_time
            },
            "user_filter": user_key,
            "event_filter": event_name,
            "logs": formatted_logs
        }
        
        logger.info(
            f"Successfully retrieved {len(formatted_logs)} Gmail logs for admin: {user_id}"
        )
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(
            f"Error retrieving Gmail logs for admin: {user_id}. Error: {str(e)}",
            exc_info=True,
        )
        error_response = {
            "error": f"Failed to retrieve Gmail logs: {str(e)}",
            "user_id": user_id,
            "user_key": user_key
        }
        raise Exception(json.dumps(error_response, indent=2))