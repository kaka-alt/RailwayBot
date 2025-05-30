import os
import pandas as pd
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from utils import conectar_banco

load_dotenv()

def exportar_csvs():
    conn = conectar_banco()
    if not conn:
        return
    registros = pd.read_sql("SELECT * FROM registros", conn)
    demandas = pd.read_sql("SELECT * FROM demandas", conn)
    os.makedirs("backup", exist_ok=True)
    registros.to_csv("backup/registros.csv", index=False)
    demandas.to_csv("backup/demandas.csv", index=False)
    conn.close()

def autenticar_graph():
    app = ConfidentialClientApplication(
        os.getenv("CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}",
        client_credential=os.getenv("CLIENT_SECRET")
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token.get("access_token")

def enviar_para_onedrive(filepath, nome_destino, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }
    with open(filepath, "rb") as f:
        r = requests.put(
            f"https://graph.microsoft.com/v1.0/me/drive/root:/Backup/{nome_destino}:/content",
            headers=headers,
            data=f
        )
    print(f"{nome_destino} =>", r.status_code, r.reason)

def executar_backup():
    exportar_csvs()
    token = autenticar_graph()
    enviar_para_onedrive("backup/registros.csv", "registros.csv", token)
    enviar_para_onedrive("backup/demandas.csv", "demandas.csv", token)

if __name__ == "__main__":
    executar_backup()
