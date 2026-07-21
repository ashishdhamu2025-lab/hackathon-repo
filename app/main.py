# app/main.py
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from app.environment import APP_NAME

from app.agents.root_agent import root_agent

app = FastAPI(title="ADK Document Extraction API")

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


def _guess_mime_type(filename: str, fallback: str) -> str:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    return {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
    }.get(ext, fallback)

@app.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file upload")

    mime_type = _guess_mime_type(file.filename or "", file.content_type or "application/octet-stream")

    user_id = "api_user"
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    # Build multimodal content: instruction text + the document bytes inline
    content = types.Content(
        role="user",
        parts=[
            types.Part(text="Please process this document."),
            types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
        ],
    )

    final_state = None
    async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
    ):
        # Optional: inspect intermediate events for logging/streaming
        if event.is_final_response():
            session = await session_service.get_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
            final_state = session.state

    if not final_state or "final_result" not in final_state:
        raise HTTPException(status_code=500, detail="Pipeline did not produce a result")

    # final_result was written by the validator_agent's output_schema/output_key
    result = final_state["final_result"]
    return JSONResponse(content=result)


@app.get("/health")
async def health():
    return {"status": "ok"}