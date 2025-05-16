import logging
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from auth.auth_utils import get_authenticated_user_details
from services.history_service import HistoryService

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Single instance of HistoryService (if applicable)
history_service = HistoryService()


@router.post("/generate")
async def add_conversation(request: Request):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()

        response = await history_service.add_conversation(user_id, request_json)
        return response

    except Exception as e:
        logger.exception("Exception in /generate: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.post("/update")
async def update_conversation(request: Request):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()
        conversation_id = request_json.get("conversation_id")

        if not conversation_id:
            raise HTTPException(status_code=400, detail="No conversation_id found")

        # Call HistoryService to update conversation
        update_response = await history_service.update_conversation(user_id, request_json)

        if not update_response:
            raise HTTPException(status_code=500, detail="Failed to update conversation")

        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "title": update_response["title"],
                    "date": update_response["updatedAt"],
                    "conversation_id": update_response["id"],
                },
            },
            status_code=200,
        )
    except Exception as e:
        logger.exception("Exception in /history/update: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.post("/message_feedback")
async def update_message_feedback(request: Request):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()
        message_id = request_json.get("message_id")
        message_feedback = request_json.get("message_feedback")

        if not message_id:
            raise HTTPException(status_code=400, detail="message_id is required")

        if not message_feedback:
            raise HTTPException(status_code=400, detail="message_feedback is required")

        # Call HistoryService to update message feedback
        updated_message = await history_service.update_message_feedback(user_id, message_id, message_feedback)

        if updated_message:
            return JSONResponse(
                content={
                    "message": f"Successfully updated message with feedback {message_feedback}",
                    "message_id": message_id,
                },
                status_code=200,
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to update message {message_id}. It either does not exist or the user does not have access to it."
            )

    except Exception as e:
        logger.exception("Exception in /history/message_feedback: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.delete("/delete")
async def delete_conversation(request: Request):
    try:
        # Get the user ID from request headers
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]
        # Parse request body
        request_json = await request.json()
        conversation_id = request_json.get("conversation_id")
        if not conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")

        # Delete conversation using HistoryService
        deleted = await history_service.delete_conversation(user_id, conversation_id)
        if deleted:
            return JSONResponse(
                content={
                    "message": "Successfully deleted conversation and messages",
                    "conversation_id": conversation_id},
                status_code=200,
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} not found or user does not have permission.")
    except Exception as e:
        logger.exception("Exception in /history/delete: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.get("/list")
async def list_conversations(
    request: Request,
    offset: int = Query(0, alias="offset"),
    limit: int = Query(25, alias="limit")
):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        logger.info(f"user_id: {user_id}, offset: {offset}, limit: {limit}")

        # Get conversations
        conversations = await history_service.get_conversations(user_id, offset=offset, limit=limit)

        if not isinstance(conversations, list):
            return JSONResponse(
                content={
                    "error": f"No conversations for {user_id} were found"},
                status_code=404)

        return JSONResponse(content=conversations, status_code=200)

    except Exception as e:
        logger.exception("Exception in /history/list: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.post("/read")
async def get_conversation_messages(request: Request):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()
        conversation_id = request_json.get("conversation_id")

        if not conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")

        # Get conversation details
        conversationMessages = await history_service.get_conversation_messages(user_id, conversation_id)
        if not conversationMessages:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} was not found. It either does not exist or the user does not have access to it."
            )

        return JSONResponse(
            content={
                "conversation_id": conversation_id,
                "messages": conversationMessages},
            status_code=200)

    except Exception as e:
        logger.exception("Exception in /history/read: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.post("/rename")
async def rename_conversation(request: Request):
    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()
        conversation_id = request_json.get("conversation_id")
        title = request_json.get("title")

        if not conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")
        if not title:
            raise HTTPException(status_code=400, detail="title is required")

        rename_conversation = await history_service.rename_conversation(user_id, conversation_id, title)

        return JSONResponse(content=rename_conversation, status_code=200)

    except Exception as e:
        logger.exception("Exception in /history/rename: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.delete("/delete_all")
async def delete_all_conversations(request: Request):
    try:
        # Get the user ID from request headers
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Get all user conversations
        conversations = await history_service.get_conversations(user_id, offset=0, limit=None)
        if not conversations:
            raise HTTPException(status_code=404,
                                detail=f"No conversations for {user_id} were found")

        # Delete all conversations
        for conversation in conversations:
            await history_service.delete_conversation(user_id, conversation["id"])

        return JSONResponse(
            content={
                "message": f"Successfully deleted all conversations for user {user_id}"},
            status_code=200,
        )

    except Exception as e:
        logging.exception("Exception in /history/delete_all: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.post("/clear")
async def clear_messages(request: Request):
    try:
        # Get the user ID from request headers
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers)
        user_id = authenticated_user["user_principal_id"]

        # Parse request body
        request_json = await request.json()
        conversation_id = request_json.get("conversation_id")

        if not conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")

        # Delete conversation messages from CosmosDB
        success = await history_service.clear_messages(user_id, conversation_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Failed to clear messages or conversation not found")

        return JSONResponse(
            content={
                "message": "Successfully cleared messages"},
            status_code=200)

    except Exception as e:
        logger.exception("Exception in /history/clear: %s", str(e))
        return JSONResponse(content={"error": "An internal error has occurred!"}, status_code=500)


@router.get("/history/ensure")
async def ensure_cosmos():
    try:
        success, err = await history_service.ensure_cosmos()
        if not success:
            return JSONResponse(
                content={
                    "error": err or "Unknown error occurred"},
                status_code=422)
        return JSONResponse(
            content={
                "message": "CosmosDB is configured and working"},
            status_code=200)
    except Exception as e:
        logger.exception("Exception in /history/ensure: %s", str(e))
        cosmos_exception = str(e)

        if "Invalid credentials" in cosmos_exception:
            return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)
        elif "Invalid CosmosDB database name" in cosmos_exception or "Invalid CosmosDB container name" in cosmos_exception:
            return JSONResponse(content={"error": "Invalid CosmosDB configuration"}, status_code=422)
        else:
            return JSONResponse(
                content={
                    "error": "CosmosDB is not configured or not working"},
                status_code=500)
