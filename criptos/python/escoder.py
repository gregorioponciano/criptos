import base64
import zlib

# Esta é a senha para trancar e abrir o código
SECRET = b"secret!" 

def gerar_blob(codigo_limpo):
    # 1. Comprime para diminuir o tamanho
    comprimido = zlib.compress(codigo_limpo.encode("utf-8"))
    # 2. Aplica o XOR (embaralha os bits com a senha)
    embaralhado = bytes([b ^ SECRET[i % len(SECRET)] for i, b in enumerate(comprimido)])
    # 3. Transforma em texto Base64 (para você poder copiar e colar)
    return base64.b64encode(embaralhado).decode("utf-8")

# ESCREVA SEU CÓDIGO REAL AQUI DENTRO:
meu_projeto = """
print("--- SISTEMA INICIALIZADO ---")
usuario = input("Digite seu nome: ")
print(f"Ola {usuario}, este codigo estava escondido!")
"""

resultado = gerar_blob(meu_projeto)
print("--- COPIE O TEXTO ABAIXO ---")
print(resultado)
print("----------------------------")

