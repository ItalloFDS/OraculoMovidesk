from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOVIDESK_TOKEN = "ce9f965b-35f5-4492-b805-b6b4a383946f"
API_URL = "https://api.movidesk.com/public/v1/knowledgeArticles"

def busca_na_base(termo: str):
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
                "resumo": (artigo.get("content") or "")[:300] + "..."
            })

        return {
            "quantidade_resultados": len(resultados),
            "resultados": resultados
        }
    except Exception as e:
        return {"erro": str(e)}

@app.get("/buscar")
def buscar_artigos(termo: str):
    return busca_na_base(termo)

@app.post("/responder")
async def responder(req: Request):
    data = await req.json()
    pergunta = data.get("pergunta", "")

    resultados = busca_na_base(pergunta)
    if resultados.get("quantidade_resultados", 0) == 0:
        return {"resposta": "Desculpe, não encontrei nada sobre isso."}

    textos = []
    for r in resultados["resultados"][:3]:
        textos.append(f"**{r['titulo']}**\n{r['resumo']}\nLink: {r['link']}")

    resposta_formatada = "\n\n".join(textos)

    return {"resposta": resposta_formatada}
