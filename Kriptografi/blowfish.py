import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pad_pkcs7(data: bytes, block_size: int = 8) -> tuple[bytes, int]:
    # Menambahkan padding PKCS7 agar ukuran data menjadi kelipatan 8 bytes.
    padding_len = block_size - (len(data) % block_size)
    padded_data = data + bytes([padding_len] * padding_len)
    return padded_data, padding_len

def unpad_pkcs7(data: bytes) -> tuple[bytes, int]:
    # Menghapus padding PKCS7 setelah dekripsi.
    padding_len = data[-1]
    if padding_len < 1 or padding_len > 8:
        raise ValueError("Padding PKCS7 tidak valid!")
    return data[:-padding_len], padding_len

def process(text: str, key: str, mode: str) -> tuple[str, list[str]]:
    logs = []
    
    # Validasi Input Teks
    if not text.strip():
        return "Input teks kosong!", ["⚠️ Input teks tidak boleh kosong."]
    
    # Validasi Panjang Kunci Blowfish (4 - 56 Bytes / 32 - 448 Bit)
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 4 or len(key_bytes) > 56:
        return "Error: Kunci Tidak Valid!", [
            "❌ <b>Gagal Inisialisasi Kunci Blowfish!</b>",
            f"• Panjang Kunci Input : {len(key_bytes)} bytes ({len(key_bytes)*8} bit)",
            "• Syarat Kunci Blowfish : 4 hingga 56 bytes (32 hingga 448 bit)."
        ]

    # Inisialisasi Engine Cipher Blowfish Mode ECB
    cipher = Cipher(algorithms.Blowfish(key_bytes), modes.ECB(), backend=default_backend())

    # MODE ENKRIPSI
    if mode == "Enkripsi":
        plain_bytes = text.encode('utf-8')
        
        # LOG PEMBENTUKAN KUNCI & INPUT
        logs.append("🔑 <b>[LANGKAH 1] ANALISIS INPUT & INSIALISASI KUNCI</b>")
        logs.append(f"• Plaintext Asli   : \"{text}\"")
        logs.append(f"• Plaintext (Hex)  : <code>{' '.join(f'{b:02X}' for b in plain_bytes)}</code> ({len(plain_bytes)} bytes)")
        logs.append(f"• Kunci Text       : \"{key}\"")
        logs.append(f"• Kunci Hex (Key)  : <code>{' '.join(f'{b:02X}' for b in key_bytes)}</code> ({len(key_bytes)} bytes / {len(key_bytes)*8} bit)")
        logs.append("--------------------------------------------------------------------------------")

        # LOG PENAMBAHAN PKCS7 PADDING
        padded_bytes, p_len = pad_pkcs7(plain_bytes, 8)
        num_blocks = len(padded_bytes) // 8
        logs.append("🧱 <b>[LANGKAH 2] PEMBAGIAN BLOK & PKCS7 PADDING (64-BIT / 8-BYTE)</b>")
        logs.append(f"• Tambahan Padding : {p_len} byte(s) bernilai <code>0x{p_len:02X}</code>")
        logs.append(f"• Data Ber-padding : <code>{' '.join(f'{b:02X}' for b in padded_bytes)}</code> ({len(padded_bytes)} bytes)")
        logs.append(f"• Total Blok Data  : {num_blocks} Blok (Tiap blok berukuran 64-bit / 8 bytes)")
        
        # Tampilkan rincian pembagian blok L (32-bit Kiri) dan R (32-bit Kanan)
        for i in range(num_blocks):
            block = padded_bytes[i*8 : (i+1)*8]
            L = block[:4]
            R = block[4:]
            logs.append(f"  └─ <b>Blok ke-{i+1}</b>: L0 = <code>{L.hex().upper()}</code> | R0 = <code>{R.hex().upper()}</code>")
        logs.append("--------------------------------------------------------------------------------")

        # LOG EKSEKUSI FEISTEL NETWORK 16 PUTARAN
        logs.append("⚙️ <b>[LANGKAH 3] URAIAN FEISTEL NETWORK & STRUKTUR SUBKEY</b>")
        logs.append("<b>1. Ekstrimasi P-Array (18 Subkeys 32-bit):</b>")
        for i in range(1, 19):
            start_idx = ((i - 1) * 4) % len(key_bytes)
            end_idx = start_idx + 4
            k_chunk = key_bytes[start_idx:end_idx]
            if len(k_chunk) < 4:
                k_chunk = (k_chunk + key_bytes)[:4]
            
            logs.append(f"   • <b>P{i:<2}</b> : P{i:<2} ⊕ <code>0x{k_chunk.hex().upper()}</code> (Kunci byte ke-{start_idx+1} s.d {start_idx+len(k_chunk)})")
            
        logs.append("<br><b>2. Struktur Fungsi F(L) Menggunakan 4 S-Boxes:</b>")
        logs.append("   • Blok L (32-bit) dipecah menjadi 4 byte: L = [a] [b] [c] [d]")
        logs.append("   • Perhitungan Substitusi: <code>F(L) = ((S1[a] + S2[b] mod 2^32) ^ S3[c]) + S4[d] mod 2^32</code>")
        logs.append("     - S1, S2, S3, S4 masing-masing berisi 256 elemen 32-bit")
        
        logs.append("<br><b>3. Simulasi Alur 16 Putaran Feistel Network per Blok:</b>")
        for i in range(1, 17):
            logs.append(f"   • <b>Putaran {i:<2} :</b> L{i}' = L{i-1} ⊕ P{i} | R{i} = F(L{i}') ⊕ R{i-1} | Swap(L{i}, R{i})")
            
        logs.append("   • <b>Penutupan  :</b> L_final = R16 ⊕ P17 | R_final = L16' ⊕ P18")
        
        encryptor = cipher.encryptor()
        encrypted_bytes = encryptor.update(padded_bytes) + encryptor.finalize()
        logs.append(f"<br>• <b>Hasil Akhir Cipher Hex :</b> <code>{' '.join(f'{b:02X}' for b in encrypted_bytes)}</code>")
        logs.append("--------------------------------------------------------------------------------")

        # LOG FORMATTING OUTPUT BASE64
        result_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        logs.append("📦 <b>[LANGKAH 4] ENCODING HASIL AKHIR (BASE64)</b>")
        logs.append("• Mengonversi byte mentah menjadi string Base64 agar aman ditampilkan.")
        logs.append(f"• <b>Final Ciphertext : {result_base64}</b>")

        return result_base64, logs

    # MODE DEKRIPSI
    else:
        try:
            # LOG PARSING INPUT CIPHERTEXT
            logs.append("📥 <b>[LANGKAH 1] DECODE CIPHERTEXT (BASE64 TO HEX)</b>")
            encrypted_bytes = base64.b64decode(text.strip().encode('utf-8'))
            
            logs.append(f"• Input Ciphertext : \"{text.strip()}\"")
            logs.append(f"• Raw Bytes (Hex)  : <code>{' '.join(f'{b:02X}' for b in encrypted_bytes)}</code> ({len(encrypted_bytes)} bytes)")
            logs.append(f"• Kunci Hex (Key)  : <code>{' '.join(f'{b:02X}' for b in key_bytes)}</code> ({len(key_bytes)} bytes)")

            if len(encrypted_bytes) % 8 != 0:
                return "Error: Ciphertext Rusak!", ["❌ Ukuran bytes ciphertext mentah harus kelipatan 8 (64-bit)."]
            logs.append("--------------------------------------------------------------------------------")

            # LOG EKSEKUSI DEKRIPSI FEISTEL
            logs.append("🔓 <b>[LANGKAH 2] PROSES DEKRIPSI FEISTEL NETWORK (REVERSE ROUNDS)</b>")
            logs.append("• Menjalankan 16 Putaran Feistel dengan urutan P-Array dibalik (P18 s.d. P1).")
            
            decryptor = cipher.decryptor()
            padded_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()
            logs.append(f"• Data Hasil Dekripsi + Padding (Hex): <code>{' '.join(f'{b:02X}' for b in padded_bytes)}</code>")
            logs.append("--------------------------------------------------------------------------------")

            # LOG UNPADDING PKCS7 & OUTPUT PLAINTEXT
            unpadded_bytes, p_len = unpad_pkcs7(padded_bytes)
            plaintext = unpadded_bytes.decode('utf-8')
            
            logs.append("✂️ <b>[LANGKAH 3] UNPADDING PKCS7 & REKONSTRUKSI PLAINTEXT</b>")
            logs.append(f"• Membuang {p_len} byte(s) padding <code>0x{p_len:02X}</code> di akhir data.")
            logs.append(f"• Hex Plaintext Murni : <code>{' '.join(f'{b:02X}' for b in unpadded_bytes)}</code>")
            logs.append(f"• <b>Final Plaintext   : \"{plaintext}\"</b>")

            return plaintext, logs

        except Exception as e:
            return "Gagal Dekripsi!", [
                "❌ <b>PROSES DEKRIPSI GAGAL!</b>",
                f"• Error Rincian : {str(e)}",
                "• Pastikan Kunci yang dimasukkan benar dan format Ciphertext Base64 valid."
            ]
