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

MOVIDESK_TOKEN = "ce9f965b-35f5-4492-b805-b6b4a383946f"  # ⚠️ Em produção, use variável de ambiente!
API_URL = "https://api.movidesk.com/public/v1/article"

@app.get("/buscar")
def buscar_artigos(termo: str):
    headers = {
        "Authorization": MOVIDESK_TOKEN
    }
    params = {
        "q": termo,
        "pageSize": 5,
        "page": 0
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        return {
            "quantidade_resultados": 0,
            "resultados": [],
            "erro": f"Erro na requisição: {response.status_code}"
        }

    dados = response.json()
    resultados = []
    for item in dados.get("items", []):
        resultados.append({
            "id": item["id"],
            "titulo": item["title"],
            "resumo": item.get("summary") or "(sem resumo)",
            "link": f"https://atendimento.movidesk.com/kb/article/{item['id']}/{item['title'].replace(' ', '-').lower()}"
        })

    return {
        "quantidade_resultados": len(resultados),
        "resultados": resultados
    }

@app.post("/responder")
async def responder(req: Request):
    data = await req.json()
    pergunta = data.get("pergunta", "")
    resultados = buscar_artigos(termo=pergunta)

    if resultados.get("quantidade_resultados", 0) == 0:
        return {"resposta": "Não encontrei nada sobre isso."}

    textos = []
    for r in resultados["resultados"]:
        textos.append(f"{r['titulo']}: {r['resumo']} (Link: {r['link']})")

    resposta_formatada = "\n\n".join(textos[:3])
    return {"resposta": resposta_formatada}
