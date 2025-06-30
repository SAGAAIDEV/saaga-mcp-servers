import json
import asyncio
from typing import Optional, List, Dict, Any
from mcp_gsuite.lib.accounts import format_docstring_with_user_id_arg
from ...lib import gmail
from loguru import logger


@format_docstring_with_user_id_arg
async def create_reply(
    user_id: str,
    original_message_id: str,
    reply_body: str,
    send: bool = False,
    cc: Optional[List[str]] = None,
) -> str:
    """
    Create a reply to an email message and either send it or save as draft.

    Args:
        user_id: {user_id_arg}
        original_message_id (str): The ID of the original message to reply to.
        reply_body (str): Body content of the reply
        send (bool): If True, sends the reply immediately. If False, saves as draft.
        cc (list[str], optional): List of email addresses to CC
    """
    logger.info(
        f"Creating reply for user_id: {user_id}, original_message_id: {original_message_id}, send: {send}"
    )
    try:
        gmail_service = gmail.GmailService(user_id=user_id)
        logger.debug(f"GmailService initialized for user_id: {user_id}")

        # The create_reply method will fetch the original message internally
        result = await asyncio.to_thread(
            gmail_service.create_reply,
            original_message_id=original_message_id,  # Fixed parameter name
            reply_body=reply_body,
            send=send,
            cc=cc,
        )

        if result is None:
            logger.warning(
                f"Failed to create reply for user_id: {user_id}, original_message_id: {original_message_id}"
            )
            return json.dumps(
                {
                    "message": "Failed to create reply.",
                    "user_id": user_id,
                    "original_message_id": original_message_id,
                },
                indent=2,
            )

        action = "sent" if send else "drafted"
        result_id = result.get("id") if send else result.get("id", result.get("draft", {}).get("id"))
        logger.info(
            f"Successfully {action} reply for user_id: {user_id}, result_id: {result_id}"
        )
        
        # Create a more informative response
        response = {
            "status": f"Reply {action} successfully",
            "action": action,
            "id": result_id,
            "original_message_id": original_message_id,
            "user_id": user_id,
            "details": result
        }
        
        return json.dumps(response, indent=2)

    except Exception as e:
        logger.error(
            f"Error in create_reply for user_id: {user_id}, original_message_id: {original_message_id}. Error: {str(e)}",
            exc_info=True,
        )
        error_details = {
            "error": f"Failed to create reply for {user_id}: {str(e)}",
            "user_id": user_id,
            "original_message_id": original_message_id,
            "error_type": type(e).__name__
        }
        raise Exception(json.dumps(error_details, indent=2))
