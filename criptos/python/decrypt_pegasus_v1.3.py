#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║              PEGASUS v1.3 DECODER                                   ║
║         Ferramenta de Análise de Segurança - Estudo                ║
╚══════════════════════════════════════════════════════════════════════╝

VERSÃO: 1.3
AUTOR: thakur2309

PROPÓSITO: Estudo de engenharia reversa para análise de segurança.
Este script descriptografa o payload obfuscado do PAGASUS-PRO v1.3.

┌─────────────────────────────────────────────────────────────────────┐
│  ALGORITMO DE DESCRIPTOGRAFIA IDENTIFICADO:                        │
│                                                                     │
│    Base64 → XOR(secret!) → zlib.decompress(wbits=15)               │
│                                                                     │
│  NOTA: O parâmetro wbits=15 é ESSENCIAL para a decompressão!       │
└─────────────────────────────────────────────────────────────────────┘

USO:
    1. Cole o texto Base64 na variável BLOB abaixo
    2. Execute: python3 decrypt_pegasus_v1.3.py
"""

import base64
import zlib

SECRET = b"secret!"

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR bitwise com chave repetida ciclicamente."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_pegasus_v1_3(blob: str) -> str:
    """
    Descriptografa o BLOB do PAGASUS-PRO v1.3.
    
    Fluxo de descriptografia:
    ┌────────┐    ┌─────────┐    ┌──────────────┐    ┌──────────────┐
    │ Base64 │ → │  Raw    │ →  │ XOR(secret!) │ →  │  zlib.decomp │
    │ Input  │    │ Bytes   │    │   Decode     │    │  (wbits=15)  │
    └────────┘    └─────────┘    └──────────────┘    └──────────────┘
    
    Args:
        blob: String Base64 criptografada
        
    Returns:
        String com o payload descriptografado (código Python)
    """
    raw = base64.b64decode(blob)
    xor_result = xor_bytes(raw, SECRET)
    decompressed = zlib.decompress(xor_result, wbits=15)
    return decompressed.decode("utf-8")

# ═══════════════════════════════════════════════════════════════════════
# COLE SEU BLOB DO PEGASUS v1.3 AQUI
# ═══════════════════════════════════════════════════════════════════════
BLOB = """COLE_SEU_TEXTO_BASE64_AQUI"""

if __name__ == "__main__":
    print("=" * 70)
    print("   PEGASUS v1.3 DECODER - Ferramenta de Análise de Segurança")
    print("=" * 70)
    
    print("\n[*] Algoritmo identificado:")
    print("    Base64 → XOR(secret!) → zlib.decompress(wbits=15)")
    
    if BLOB == """COLE_SEU_TEXTO_BASE64_AQUI""":
        print("\n[!] Edite o script e cole o BLOB na variável BLOB acima")
        print("[i] Uso correto:")
        print("    BLOB = 'C/m+Tw4HwkX3vJU...=='\n")
        print("[INFO] Payload v1.3 já descriptografado disponível em:")
        print("       payload_v1.3_decrypted.py")
        print("\n[INFO] Tamanho do payload: 37.465 bytes")
        exit(0)
    
    try:
        resultado = decrypt_pegasus_v1_3(BLOB)
        print("\n[OK] Payload Pegasus v1.3 descriptografado com sucesso!")
        print(f"[OK] Tamanho: {len(resultado)} caracteres")
        
        with open("payload_v1.3_decrypted.py", "w") as f:
            f.write(resultado)
        print("[OK] Salvo em: payload_v1.3_decrypted.py")
        
        print("\n" + "-" * 70)
        print("CONTEÚDO DO PAYLOAD (Primeiras 1000 linhas):")
        print("-" * 70)
        linhas = resultado.split('\n')
        for linha in linhas[:1000]:
            print(linha)
        
        if len(linhas) > 1000:
            print(f"\n... ({len(linhas) - 1000} linhas restantes) ...")
            
    except base64.binascii.Error as e:
        print(f"\n[ERRO] Base64 inválido: {e}")
    except zlib.error as e:
        print(f"\n[ERRO] Decompressão falhou: {e}")
        print("[DICA] Verifique se o BLOB está correto e completo")
    except Exception as e:
        print(f"\n[ERRO] Falha na decodificação: {e}")
