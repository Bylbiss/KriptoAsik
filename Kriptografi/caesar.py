def process(text, key, mode):
    logs = []
    result_chars = []
    
    # penentuan mode enkripsi atau dekripsi
    if mode == "Enkripsi":
        shift = key % 26
        logs.append(f"**MODE ENKRIPSI** | Kunci Pergeseran (Shift) = {key} (mod 26 = {shift})")
        logs.append("Rumus Enkripsi: Chiper = (Plaintext + kunci) mod 26\n")
    else:
        shift = (-key) % 26
        logs.append(f"**MODE DEKRIPSI** | Kunci Pergeseran (Shift) = -{key} (mod 26 = {shift})")
        logs.append("Rumus Dekripsi: P = (C - k) mod 26\n")

    # pergeseran karakter
    logs.append("--- **LANGKAH PERGESERAN** ---")
    
    for idx, char in enumerate(text, start=1):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            orig_pos = ord(char) - base
            new_pos = (orig_pos + shift) % 26
            new_char = chr(base + new_pos)
            
            result_chars.append(new_char)
            logs.append(
                f"Langkah {idx}: '{char}' (Posisi: {orig_pos}) "
                f"-> Digeser {shift} posisi -> '{new_char}' (Posisi Baru: {new_pos})"
            )
        else:
            result_chars.append(char)
            logs.append(f"Langkah {idx}: '{char}' -> Karakter Non-Alfabet (Tidak diubah)")

    #gabung + pengembalian hasil
    final_result = "".join(result_chars)
    
    logs.append("\n--- **PROSES SELESAI** ---")
    logs.append(f"Teks Input  : {text}")
    logs.append(f"Teks Hasil  : {final_result}")

    return final_result, logs
