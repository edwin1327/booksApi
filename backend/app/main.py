from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pytesseract
from PIL import Image
import io
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

# Configura CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para la respuesta de libros
class BookResponse(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    publisher: Optional[str] = None
    isbn: Optional[str] = None
    language: Optional[str] = None
    volumes: Optional[int] = 1

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Book API ready for requests"}

# Endpoint de salud
@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}  # Mejoraremos esto después

# Endpoint para procesar imágenes de libros
@app.post("/process-book/", response_model=BookResponse)
async def process_book(
    images: List[UploadFile] = File(...),
    language: str = "es",
    volumes: int = 1
):
    try:
        # Validación: máximo 2 imágenes
        if len(images) > 2:
            raise HTTPException(status_code=400, detail="Máximo 2 imágenes permitidas")

        extracted_texts = []
        
        # Procesar cada imagen
        for image in images:
            # Leer imagen
            img_data = await image.read()
            img = Image.open(io.BytesIO(img_data))
            
            # Extraer texto (configurando idioma para OCR)
            custom_config = f'--psm 6 -l {language}'
            text = pytesseract.image_to_string(img, config=custom_config)
            extracted_texts.append(text)
        
        # Aquí iría la conexión con Deepseek (lo implementaremos después)
        # Por ahora simulamos una respuesta
        mock_response = {
            "title": " ".join(extracted_texts)[:50] + "...",
            "author": "Autor Ejemplo",
            "year": 2023,
            "publisher": "Editorial Mock",
            "isbn": "123-4567890123",
            "language": language,
            "volumes": volumes
        }
        
        return mock_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    