from fastapi import APIRouter

router = APIRouter(prefix="/ai-process", tags=["ai-process"])


@router.post("/")
def process_ai():
    # TODO: Implement the LangGraph + Mistral integration
    return {"message": "AI processing endpoint not implemented yet."}
