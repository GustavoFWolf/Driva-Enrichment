import os
import random
import psycopg2
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Driva Enrichment API")

security = HTTPBearer()

#se conecta com o banco de dados
def get_conn():
    return psycopg2.connect(DATABASE_URL)

#realiza a verificação da autenticação com a API_KEY
def auth(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
# endpoint : /people/v1/enrichments
@app.get("/people/v1/enrichments", dependencies=[Depends(auth)])
def enrichments(
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=100)
):
    if random.random() < 0.05:
        raise HTTPException(status_code=429, detail="Too Many Requests") #Simulaçao de erro

    offset = (page - 1) * limit
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM api_enrichments_seed")
    total_items = cur.fetchone()[0]
    total_pages = (total_items + limit - 1) // limit

    #le os dados da tabela

    cur.execute("""
        SELECT id, id_workspace, workspace_name, total_contacts,
               contact_type, status, created_at, updated_at
        FROM api_enrichments_seed
        ORDER BY created_at
        LIMIT %s OFFSET %s
    """, (limit, offset))

    rows = cur.fetchall()
    conn.close()

    #gera o arquivo JSON com a resposta

    data = [{
        "id": r[0],
        "id_workspace": r[1],
        "workspace_name": r[2],
        "total_contacts": r[3],
        "contact_type": r[4],
        "status": r[5],
        "created_at": r[6],
        "updated_at": r[7],
    } for r in rows]

    return {
        "meta": {
            "current_page": page,
            "items_per_page": limit,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "data": data
    }

#endpoint /analytics/overview

@app.get("/analytics/overview", dependencies=[Depends(auth)])
def overview():
    conn = get_conn()
    cur = conn.cursor()

    #retira e calcula alguns dados da tabela Gold

    cur.execute("""
        SELECT
          COUNT(*),
          AVG(duracao_processamento_minutos),
          SUM(CASE WHEN processamento_sucesso THEN 1 ELSE 0 END)::float / COUNT(*)
        FROM gold_enrichments
    """)

    total, avg_time, success_rate = cur.fetchone()
    conn.close()

    return {
        "total_jobs": total,
        "tempo_medio_minutos": avg_time,
        "taxa_sucesso": success_rate
    }
#endpoint /analytics/enrichments

@app.get("/analytics/enrichments", dependencies=[Depends(auth)])
def list_gold(
    page: int = 1,
    limit: int = 50
):
    offset = (page - 1) * limit

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM gold_enrichments")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT *
        FROM gold_enrichments
        ORDER BY data_criacao DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))

    cols = [desc[0] for desc in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()] #cria uma lista de dicionários com os dados da tabela GOLD.
    conn.close()

    return {
        "page": page,
        "total": total,
        "data": rows
    }
