def process(text, key, mode):
    """
    Modul Pemroses Vernam Cipher / One-Time Pad (OTP)
    Diformat dengan Code Block agar sejajar dan rapi di Streamlit.
    """
    logs = []
    
    # Validasi input kunci
    if not key:
        return "Error: Kunci tidak boleh kosong!", ["Kunci tidak boleh kosong. Masukkan kunci teks."]

    if mode == "Dekripsi":
        if any(char.isspace() for char in text):
            hex_blocks = text.split()
        else:
            compact_text = text.strip()
            if len(compact_text) % 2:
                return "Error: Ciphertext HEX tidak lengkap!", [
                    "Ciphertext tanpa spasi harus berisi pasangan HEX lengkap (2 digit per blok)."
                ]
            hex_blocks = [
                compact_text[index:index + 2]
                for index in range(0, len(compact_text), 2)
            ]
        data_length = len(hex_blocks)
    else:
        hex_blocks = []
        data_length = len(text)

    logs.append(f"**MODE {mode.upper()}** | Vernam Cipher (One-Time Pad)")
    
    # Penyelarasan panjang kunci dengan panjang teks
    extended_key = (key * (data_length // len(key) + 1))[:data_length]
    if len(key) < data_length:
        logs.append("*Catatan: Panjang kunci lebih pendek dari teks, kunci otomatis diulang.*")
        
    logs.append(f"Kunci yang dipakai : {extended_key}")
    logs.append("Rumus Operasi      : Nilai Biner Teks XOR (^) Nilai Biner Kunci\n")
    logs.append("--- **LANGKAH DEMI LANGKAH (OPERASI XOR BINER)** ---")

    result_chars = []

    if mode == "Enkripsi":
        for i in range(len(text)):
            p = text[i]
            k = extended_key[i]
            
            p_ascii = ord(p)
            k_ascii = ord(k)
            
            p_bin = f"{p_ascii:08b}"
            k_bin = f"{k_ascii:08b}"
            
            xor_val = p_ascii ^ k_ascii
            xor_bin = f"{xor_val:08b}"
            hex_val = f"{xor_val:02X}" 
            
            result_chars.append(hex_val)
            
            # Format blok monospaced yang sejajar dan rapi
            block = (
                f"```text\n"
                f"Langkah {i+1}:\n"
                f"  Teks  : '{p}' (ASCII: {p_ascii:3d}) -> Biner: {p_bin}\n"
                f"  Kunci : '{k}' (ASCII: {k_ascii:3d}) -> Biner: {k_bin}\n"
                f"  --------------------------------------- (XOR)\n"
                f"  Hasil : Hex {hex_val} (ASCII: {xor_val:3d}) -> Biner: {xor_bin}\n"
                f"```"
            )
            logs.append(block)
        
        final_result = " ".join(result_chars)

    else:
        # Ciphertext tanpa pemisah dibaca sebagai blok HEX dua digit.
        if not any(char.isspace() for char in text):
            logs.append(
                "*Ciphertext tanpa spasi dibaca per 2 digit HEX. Ini sesuai "
                "untuk input ASCII; pertahankan pemisah jika mengenkripsi "
                "karakter non-ASCII.*"
            )

        # MODE DEKRIPSI
        for i, h in enumerate(hex_blocks):
            if i >= len(extended_key):
                break
            
            k = extended_key[i]
            k_ascii = ord(k)
            k_bin = f"{k_ascii:08b}"
            
            try:
                c_val = int(h, 16)
                c_bin = f"{c_val:08b}"
                
                p_val = c_val ^ k_ascii
                p_bin = f"{p_val:08b}"
                p_char = chr(p_val)
                
                result_chars.append(p_char)
                
                block = (
                    f"```text\n"
                    f"Langkah {i+1}:\n"
                    f"  Cipher: Hex {h} (Desimal: {c_val:3d}) -> Biner: {c_bin}\n"
                    f"  Kunci : '{k}'    (ASCII:   {k_ascii:3d}) -> Biner: {k_bin}\n"
                    f"  ------------------------------------------- (XOR)\n"
                    f"  Hasil : '{p_char}'   (ASCII:   {p_val:3d}) -> Biner: {p_bin}\n"
                    f"```"
                )
                logs.append(block)
            except ValueError:
                result_chars.append("?")
                logs.append(f"**Langkah {i+1}: Hex '{h}' tidak valid.**")
                
        final_result = "".join(result_chars)

    logs.append("\n--- **PROSES SELESAI** ---")
    logs.append(f"Teks Input  : `{text}`")
    logs.append(f"Teks Hasil  : `{final_result}`")

    return final_result, logs