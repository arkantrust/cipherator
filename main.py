from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from cipher import encode, decode, gen_key

app = FastAPI()

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
async def main():
    return FileResponse('public/index.html')

class CipherRequest(BaseModel):
    action: str
    file: UploadFile = File(...)
    key: str | None = None

class CipherResponse(BaseModel):
    file: str
    key: str

@app.post('/')
async def handle_file(data: CipherRequest) -> CipherResponse:
    
    file: UploadFile = data.file
    
    key = data.key
    if not key:
        if data.action == "decode":
            raise HTTPException(status_code=400, detail="Key is required for decoding.")
        else:
            key = gen_key()
    
    file_content = await file.read()

    new_file = ""
    
    if data.action == "encode":
        new_file = encode(file_content, key)
    elif data.action == "decode":
        new_file = decode(file_content, key)
    else:
        raise ValueError("Invalid action: must be 'encode' or 'decode'.")
    
    return CipherResponse(file=new_file, key=key)

# run the app
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)