from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir chamadas de qualquer origem (pode restringir depois)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOVIDESK_TOKEN = "ce9f965b-35f5-4492-b805-b6b4a383946f"
API_URL = "https://api.movidesk.com/public/v1/knowledgeArticles"

@app.get("/buscar")
def buscar_artigos(termo: str = Query(..., description="Palavra-chave para busca")):
    try:
        params = {
            "token": MOVIDESK_TOKEN,
            "keywords": termo,
            "isActive": "true"
        }

        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        artigos = response.json()

        resultados = []
        for artigo in artigos:
            resultados.append({
                "titulo": artigo.get("title"),
                "link": artigo.get("portalUrl"),
                "resumo": artigo.get("content")[:300] + "..."
            })

        return {
            "quantidade_resultados": len(resultados),
            "resultados": resultados
        }

    except Exception as e:
        return {"erro": str(e)}
