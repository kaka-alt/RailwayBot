import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# CAMINHO_BASE -  Relative to the project root (where Procfile is)
CAMINHO_BASE = "."  # Current directory
CSV_ORGAOS = os.path.join(CAMINHO_BASE, "listas", "orgaos.csv")
CSV_PATH = os.path.join(CAMINHO_BASE, "data")
FOTO_PATH = os.path.join(CAMINHO_BASE, "fotos")
CSV_ASSUNTOS = os.path.join(CAMINHO_BASE, "listas", "assuntos.csv")
CSV_REGISTRO = os.path.join(CAMINHO_BASE, "data", "registros.csv")
PAGINACAO_TAMANHO = 5
COLABORADORES = ["Orlando", "Derielle", "Ricardo", "Vania", "Danillo"]


# Ensure directories exist (this is VERY important)
os.makedirs(os.path.dirname(CSV_ORGAOS), exist_ok=True)
os.makedirs(CSV_PATH, exist_ok=True)
os.makedirs(FOTO_PATH, exist_ok=True)
os.makedirs(os.path.dirname(CSV_ASSUNTOS), exist_ok=True)
os.makedirs(os.path.dirname(CSV_REGISTRO), exist_ok=True)