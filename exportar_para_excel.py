import pandas as pd
from sqlalchemy import create_engine
import os
from msal import ConfidentialClientApplication
import requests


# Dados do Railway via variável de ambiente
user = os.getenv("PGUSER")
password = os.getenv("PGPASSWORD")
host = os.getenv("PGHOST")
port = os.getenv("PGPORT")
database = os.getenv("PGDATABASE")

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

# Exportar tabelas
df_registros = pd.read_sql("SELECT * FROM registros", engine)
df_demandas = pd.read_sql("SELECT * FROM demandas", engine)

df_registros.to_excel("registros.xlsx", index=False)
df_demandas.to_excel("demandas.xlsx", index=False)

# Credenciais do app no Azure (você precisa criar um app no Azure Portal)
client_id = os.getenv("MS_CLIENT_ID")
client_secret = os.getenv("MS_CLIENT_SECRET")
tenant_id = os.getenv("MS_TENANT_ID")

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

token_response = app.acquire_token_for_client(scopes=scope)
access_token = token_response['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/octet-stream'
}

# Função para enviar arquivos
def upload_to_onedrive(nome_arquivo, pasta_destino):
    with open(nome_arquivo, 'rb') as f:
        response = requests.put(
            f'https://graph.microsoft.com/v1.0/me/drive/root:/{pasta_destino}/{nome_arquivo}:/content',
            headers=headers,
            data=f
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")  # Imprime o conteúdo da resposta
        if response.status_code != 200 and response.status_code != 201:  # Verifica se não foi sucesso
            print(f"Erro ao enviar {nome_arquivo} para o OneDrive!")

# Envia ambos
upload_to_onedrive("registros.xlsx", "DadosBot")
upload_to_onedrive("demandas.xlsx", "DadosBot")