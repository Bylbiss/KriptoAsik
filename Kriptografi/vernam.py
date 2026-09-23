def process(text, key, mode):
    """
    Modul Pemroses Vernam Cipher / One-Time Pad (OTP)
    """
    logs = []
    
    # Validasi input kunci
    if not key:
        return "Error: Kunci tidak boleh kosong!", ["KUNCI TIDAK BOLEH KOSONG! Masukkan kunci teks."]

    logs.append(f"**MODE {mode.upper()}** | Vernam Cipher (One-Time Pad)")
    
    # Penyelarasan panjang kunci dengan panjang teks
    extended_key = (key * (len(text) // len(key) + 1))[:len(text)]
    if len(key) < len(text):
        logs.append("*Catatan: Panjang kunci lebih pendek dari teks, kunci otomatis diulang.*")
        
    logs.append(f"Kunci yang dipakai : {extended_key}")
    logs.append("Rumus              : Nilai ASCII Teks XOR (^) Nilai ASCII Kunci\n")
    logs.append("--- **LANGKAH DEMI LANGKAH (XOR ASCII)** ---")

    result_chars = []

    if mode == "Enkripsi":
        for i in range(len(text)):
            p = text[i]
            k = extended_key[i]
            
            # Operasi XOR berbasis nilai ASCII
            xor_val = ord(p) ^ ord(k)
            hex_val = f"{xor_val:02X}" 
            
            result_chars.append(hex_val)
            logs.append(
                f"Langkah {i+1}: '{p}' (ASCII: {ord(p)}) XOR '{k}' (ASCII: {ord(k)}) "
                f"->Desimal: {xor_val} (Hex: {hex_val})"
            )
        
        # Format keluaran dipisah spasi agar mudah dibaca/disalin
        final_result = " ".join(result_chars)

    else:
        # MODE DEKRIPSI (Menerima input berupa blok Hex, contoh: 1A 2B 3C)
        hex_blocks = text.split()
        for i, h in enumerate(hex_blocks):
            if i >= len(extended_key):
                break
            
            k = extended_key[i]
            try:
                c_val = int(h, 16)
                p_val = c_val ^ ord(k)
                p_char = chr(p_val)
                
                result_chars.append(p_char)
                logs.append(
                    f"Langkah {i+1}: Hex {h} ({c_val}) XOR '{k}' ({ord(k)}) "
                    f"-> {p_val} (Karakter: '{p_char}')"
                )
            except ValueError:
                result_chars.append("?")
                logs.append(f"Langkah {i+1}: Hex '{h}' tidak valid!")
                
        final_result = "".join(result_chars)

    logs.append("\n--- **PROSES SELESAI** ---")
    logs.append(f"Teks Input : {text}")
    logs.append(f"Teks Hasil : {final_result}")

    return final_result, logs
