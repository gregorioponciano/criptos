import base64
import zlib

# A mesma senha e a mesma lógica de abrir
SECRET = b"secret!"

def abrir_codigo(blob):
    raw = base64.b64decode(blob)
    # Desembaralha
    descomprimido = bytes([b ^ SECRET[i % len(SECRET)] for i, b in enumerate(raw)])
    # Descomprime e devolve o texto original
    return zlib.decompress(descomprimido).decode("utf-8")

# AQUI VOCÊ COLA O RESULTADO QUE O 'codificador.py' GEROU
BLOB_PROTEGIDO = "C/mAWE2+7Vi0M6CwoXR7k298FIFUJ5WXgRGCVYeU7wARhXZzL0sbF+E35EN1F4Nf+VkBhWfxdvTIAcUV89ALZ8L1WIGRxtU/SnJwNa05NpG9LCCJ9Y/LpzQ8DHVPL7wqvW28YtJhrmagJxcdLC8Sa81HM2llRZhazQ=="

if __name__ == "__main__":
    try:
        # Aqui acontece a mágica:
        codigo_final = abrir_codigo(BLOB_PROTEGIDO)
        
        # O comando exec() roda o texto como se fosse código Python vivo
        exec(codigo_final)
        
    except Exception as e:
        print("Erro ao carregar o sistema.")