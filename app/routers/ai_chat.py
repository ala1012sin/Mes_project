from fastapi import APIRouter, Request, Body, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse

from core.templates import templates
from services import ai_chat as svc

from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(tags=["ai_chat"])

@router.get("/rag", response_class=HTMLResponse)
async def show_rag_page(request: Request):
    return templates.TemplateResponse("rag.html", {"request": request})

@router.post("/rag/upload", response_class=HTMLResponse)
async def upload_rag_document(
    request: Request,
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = await svc.process_document_and_store_vectors(db=db, upload_file=upload_file)

    return templates.TemplateResponse("rag.html", {
        "request": request,
        "upload_result": result,
    })
    
    
@router.post("/rag/chat", response_class=HTMLResponse)
async def rag_chat(
    request: Request,
    user_input: str = Form(...),
    model: str = Form(...),
    db: Session = Depends(get_db)
):
    response = svc.generate_rag_response(db, user_input, model)

    return templates.TemplateResponse("rag.html", {
        "request": request,
        "user_input": user_input,
        "response": response,
        "selected_model": model
    })    
    
@router.get("/sql", response_class=HTMLResponse)
async def show_sql_page(request: Request):
    return templates.TemplateResponse("sql.html", {"request": request})

@router.post("/sql/query", response_class=HTMLResponse)
async def sql_query(
    request: Request,
    user_input: str = Form(...),
    db: Session = Depends(get_db),
    model: str = Form(...)
):
    response = svc.generate_sql_response(db, user_input, model)
    
    print("SQL Response:", response.get("result"))
    
    result = response.get("result")

    return templates.TemplateResponse("sql.html", {
        "request": request,
        "user_input": user_input,
        "response": result,
    })


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

@router.get("/chatbot", response_class=HTMLResponse)
async def show_chatbot(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})



@router.post("/chatbot", response_class=HTMLResponse)
async def process_chatbot(
    request: Request, 
    user_input: str = Form(...),
    model: str = Form(...)
):
    messages = [{"role": "user", "content": user_input}]
    
    if model == "gpt":
        response = svc.generate_gpt_chat_response(messages)
    elif model == "gemini":
        response = svc.generate_gemini_chat_response(messages)
    elif model == "qwen2.5:7b" or model == "gemma3:4b":
        response = svc.generate_local_llm_chat_response(model, messages)
    else:
        response = "Invalid model selected."
    
    return templates.TemplateResponse("chatbot.html", {
        "request": request, 
	    "user_input": user_input, 
	    "response": response,
        "selected_model": model
	})