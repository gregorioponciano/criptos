#!/usr/bin/env python3
"""
PAGASUS-PRO Decoder - Ferramenta de Análise de Segurança
========================================================

PROPÓSITO: Estudo de engenharia reversa para análise de segurança.
Este script descriptografa o payload obfuscado do PAGASUS-PRO.

LÓGICA DE DECODIFICAÇÃO IDENTIFICADA:
┌─────────────────────────────────────────────────────────────┐
│  1. Base64 decode                                          │
│  2. XOR com chave "secret!" (7 bytes, repetida ciclicamente)│
│  3. zlib decompression (DEFLATE)                            │
└─────────────────────────────────────────────────────────────┘

USO:
    1. Cole o texto Base64 na variável BLOB
    2. Execute: python3 decrypt_pegasus.py
"""

import base64
import zlib

SECRET = b"secret!"

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR bitwise com chave repetida ciclicamente."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_pegasus_blob(blob: str) -> str:
    """
    Descriptografa o BLOB do PAGASUS-PRO.
    
    Fluxo reverso:
    ┌────────┐    ┌─────────┐    ┌──────────────┐    ┌─────────┐
    │ Base64 │ → │  Base64  │ →  │ XOR(secret!) │ →  │  zlib   │
    │ Input  │    │ Decode  │    │   Decode     │    │  Decom  │
    └────────┘    └─────────┘    └──────────────┘    └─────────┘
    
    Args:
        blob: String Base64 criptografada
        
    Returns:
        String com o payload descriptografado (código Python)
    """
    raw = base64.b64decode(blob)
    decompressed = zlib.decompress(xor_bytes(raw, SECRET))
    return decompressed.decode("utf-8")

# ============================================================
# COLE SEU BLOB AQUI
# ============================================================
BLOB = """COLE_SEU_TEXTO_BASE64_AQUI"""

if __name__ == "__main__":
    print("=" * 70)
    print("PAGASUS-PRO DECODER - Ferramenta de Análise de Segurança")
    print("=" * 70)
    
    print("\n[*] Algoritmo identificado:")
    print("    Base64 → XOR(secret!) → zlib.decompress")
    
    if BLOB == """COLE_SEU_TEXTO_BASE64_AQUI""":
        print("\n[!] Edite o script e cole o BLOB na variável BLOB")
        print("[i] Exemplo de uso:")
        print("    BLOB = 'C/m+Tw4HwkX3vJU...=='\n")
        exit(0)
    
    try:
        resultado = decrypt_pegasus_blob(BLOB)
        print("\n[OK] Payload descriptografado com sucesso!")
        print(f"[OK] Tamanho: {len(resultado)} caracteres")
        
        # Salvar em arquivo
        with open("payload_decrypted.py", "w") as f:
            f.write(resultado)
        print("[OK] Salvo em: payload_decrypted.py")
        
        print("\n" + "-" * 70)
        print("CONTEÚDO DO PAYLOAD:")
        print("-" * 70)
        print(resultado)
        
    except base64.binascii.Error as e:
        print(f"\n[ERRO] Base64 inválido: {e}")
    except zlib.error as e:
        print(f"\n[ERRO] Decompressão falhou (dados corrompidos ou chave incorreta): {e}")
    except Exception as e:
        print(f"\n[ERRO] Falha na decodificacao: {e}")
