// ═══════════════════════════════════════════════════════
// CRYPTO STUDIO - BIBLIOTECA DE CRIPTOGRAFIA
// ═══════════════════════════════════════════════════════

class CryptoAPI {
  // Cifra de César
  static cifraCesar(texto, shift = 3) {
    return texto.split('').map(c => {
      if (/[a-z]/i.test(c)) {
        const base = c.charCodeAt(0) >= 97 ? 97 : 65;
        return String.fromCharCode((c.charCodeAt(0) - base + shift) % 26 + base);
      }
      return c;
    }).join('');
  }

  static decifrarCesar(texto, shift = 3) {
    return this.cifraCesar(texto, -shift);
  }

  // Base64
  static encodeBase64(texto) {
    try {
      return btoa(unescape(encodeURIComponent(texto)));
    } catch (e) {
      return null;
    }
  }

  static decodeBase64(cripto) {
    try {
      return decodeURIComponent(escape(atob(cripto)));
    } catch (e) {
      return null;
    }
  }

  // XOR Cipher
  static xorCipher(texto, chave) {
    return texto.split('').map((c, i) => 
      String.fromCharCode(c.charCodeAt(0) ^ chave.charCodeAt(i % chave.length))
    ).join('');
  }

  // SHA-256
  static async sha256(texto) {
    const encoder = new TextEncoder();
    const data = encoder.encode(texto);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // SHA-512
  static async sha512(texto) {
    const encoder = new TextEncoder();
    const data = encoder.encode(texto);
    const hashBuffer = await crypto.subtle.digest('SHA-512', data);
    return Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // ROT13
  static rot13(texto) {
    return texto.replace(/[a-z]/gi, c => {
      const base = c.charCodeAt(0) >= 97 ? 97 : 65;
      return String.fromCharCode((c.charCodeAt(0) - base + 13) % 26 + base);
    });
  }

  // Vigenère
  static cifraVigenere(texto, chave) {
    let resultado = '', indexChave = 0;
    for (let i = 0; i < texto.length; i++) {
      const c = texto[i];
      if (/[a-z]/i.test(c)) {
        const base = c.charCodeAt(0) >= 97 ? 97 : 65;
        const deslocamento = chave.charCodeAt(indexChave % chave.length) - 97;
        resultado += String.fromCharCode((c.charCodeAt(0) - base + deslocamento) % 26 + base);
        indexChave++;
      } else {
        resultado += c;
      }
    }
    return resultado;
  }

  // Gerar Senha
  static gerarSenha(tamanho = 16, opcoes = {}) {
    const { maiusculas = true, minusculas = true, numeros = true, simbolos = true } = opcoes;
    let chars = '';
    if (maiusculas) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (minusculas) chars += 'abcdefghijklmnopqrstuvwxyz';
    if (numeros) chars += '0123456789';
    if (simbolos) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
    const array = new Uint32Array(tamanho);
    crypto.getRandomValues(array);
    return Array.from(array).map(n => chars[n % chars.length]).join('');
  }

  // Calcular Entropia
  static calcularEntropia(texto) {
    const freq = {};
    for (const c of texto) freq[c] = (freq[c] || 0) + 1;
    const len = texto.length;
    let entropia = 0;
    for (const c in freq) {
      const p = freq[c] / len;
      entropia -= p * Math.log2(p);
    }
    return entropia;
  }
}

// ═══════════════════════════════════════════════════════
// TESTES AUTOMÁTICOS
// ═══════════════════════════════════════════════════════

function runTests() {
  console.log('═══════════════════════════════════════════');
  console.log('🔐 CRYPTO STUDIO - TESTES');
  console.log('═══════════════════════════════════════════');

  let passed = 0, failed = 0;

  function test(nome, fn) {
    try {
      fn();
      passed++;
      console.log('✅ ' + nome);
    } catch (e) {
      failed++;
      console.log('❌ ' + nome + ': ' + e.message);
    }
  }

  test('Base64 encode/decode', () => {
    const original = 'Hello World!';
    const encoded = CryptoAPI.encodeBase64(original);
    const decoded = CryptoAPI.decodeBase64(encoded);
    if (decoded !== original) throw new Error('Falhou');
  });

  test('César cipher', () => {
    const original = 'HELLO';
    const encrypted = CryptoAPI.cifraCesar(original, 3);
    const decrypted = CryptoAPI.decifrarCesar(encrypted, 3);
    if (decrypted !== original) throw new Error('Falhou');
  });

  test('XOR cipher', () => {
    const original = 'SECRET';
    const encrypted = CryptoAPI.xorCipher(original, 'KEY');
    const decrypted = CryptoAPI.xorCipher(encrypted, 'KEY');
    if (decrypted !== original) throw new Error('Falhou');
  });

  test('ROT13', () => {
    const original = 'HELLO';
    const encrypted = CryptoAPI.rot13(original);
    const decrypted = CryptoAPI.rot13(encrypted);
    if (decrypted !== original) throw new Error('Falhou');
  });

  test('SHA-256 hash', async () => {
    const hash = await CryptoAPI.sha256('test');
    if (hash.length !== 64) throw new Error('Hash inválido');
  });

  test('Gerador de senhas', () => {
    const senha = CryptoAPI.gerarSenha(16);
    if (senha.length !== 16) throw new Error('Tamanho inválido');
  });

  console.log('');
  console.log('═══════════════════════════════════════════');
  console.log('📊 RESULTADO: ' + passed + '/' + (passed + failed) + ' testes');
  if (failed === 0) console.log('✅ TODOS OS TESTES PASSARAM!');
  console.log('═══════════════════════════════════════════');
}

runTests();
