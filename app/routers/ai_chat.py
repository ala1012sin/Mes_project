from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse

from core.templates import templates
from services import ai_chat as svc

router = APIRouter(tags=["ai_chat"])

# GET localhost:8080/ai_chat/llama
@router.get("/llama", response_class=HTMLResponse)
def show_llama_chat(request: Request):
    return templates.TemplateResponse(
        "llama_chat.html",
        {"request": request}
    )
    
    
# POST localhost:8000/ai_chat/llama
@router.post("/llama")
def generate_response_llama_chat(
    data: dict = Body(...)
):
	
    response = svc.generate_response(data)
    
    return {"reply": response}