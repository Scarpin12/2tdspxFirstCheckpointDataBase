from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connection import get_connection

app = FastAPI()

class EventoRequest(BaseModel):
    evento: str
    setor: str

@app.post("/processar")
def processar_evento(dados: EventoRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        plsql = """
        DECLARE
            v_fator NUMBER;
            v_evento VARCHAR2(30) := :evento;
            v_setor VARCHAR2(30) := :setor;

            -- Cursor para buscar ativos do setor específico
            CURSOR c_ativos IS
                SELECT id_ativo, preco_base
                FROM TB_ATIVOS_GALACTICOS
                WHERE setor = v_setor;
        BEGIN
            -- Definindo o fator baseado na estória de Kepler-186f
            IF v_evento = 'RADIACAO' THEN
                v_fator := 1.25; -- Preço sobe 25% pela escassez
            ELSIF v_evento = 'DESCOBERTA' THEN
                v_fator := 0.70; -- Preço cai 30% pela abundância
            ELSE
                v_fator := 1.0;
            END IF;

            -- Loop para processar cada ativo do setor
            FOR r IN c_ativos LOOP
                UPDATE TB_ATIVOS_GALACTICOS
                SET preco_base = r.preco_base * v_fator
                WHERE id_ativo = r.id_ativo;
            END LOOP;

            COMMIT;
        END;
        """

        cursor.execute(plsql, evento=dados.evento, setor=dados.setor)
        cursor.close()
        
        return {"status": "Sucesso", "detalhes": f"Setor {dados.setor} atualizado."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()