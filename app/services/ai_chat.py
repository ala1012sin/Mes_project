
import torch
import os
from transformers import pipeline
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

HG_token = os.getenv("HG_token")
os.environ['HF_TOKEN'] = "{HG_token}"


model_id = "meta-llama/Llama-3.2-1B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    dtype=torch.bfloat16,
    device_map="auto",
)

def generate_response(data: dict):
    prompt = data.get("message", "")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Always respond in Korean only. 한국어로만 답변하세요."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        responses = pipe(
            messages,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
            # num_return_sequences=3
        )
        print(f"Full response: {responses}")
        reply = responses[0]['generated_text'][-1]['content']
        
        # 원본 프롬프트 제거
        if prompt in reply:
            reply = reply.replace(prompt, "").strip() 
        
        return reply
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"