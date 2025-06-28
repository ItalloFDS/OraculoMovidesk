# arquivo: movidesk_kb_api.py

from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Substitua aqui com seu token de API pessoal
MOVIDESK_TOKEN = "ce9f965b-35f5-4492-b805-b6b4a383946f"
BASE_URL = "https://exati.movidesk.com/kb/pt-br/article/110718/bem-vindo-a-base-de-conhecimento-da-exati-tecnologia"

@app.get("/kb/search")
def buscar_artigos(q: str = Query(..., description="Texto a ser buscado na base de conhecimento")):
    try:
        params = {
            "token": MOVIDESK_TOKEN,
            "keywords": q,
            "isActive": "true",
            "isFaq": "false"
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        artigos = response.json()

        resultado = [
            {
                "titulo": artigo.get("title"),
                "conteudo": artigo.get("content"),
                "link": artigo.get("portalUrl")
            }
            for artigo in artigos
        ]

        return {
            "total_resultados": len(resultado),
            "resultados": resultado
        }

    except Exception as e:
        return {"erro": str(e)}
