def process(text, key, mode):
    logs = []
    result_chars = []

    # Penentuan mode enkripsi atau dekripsi
    if mode == "Enkripsi":
        shift = key % 26
        logs.append(
            f"**MODE ENKRIPSI** | Kunci Pergeseran (Shift) = {key} (mod 26 = {shift})"
        )
        logs.append("Rumus Enkripsi: Chiper = (Plaintext + kunci) mod 26\n")
    else:
        shift = (-key) % 26
        logs.append(
            f"**MODE DEKRIPSI** | Kunci Pergeseran (Shift) = -{key} (mod 26 = {shift})"
        )
        logs.append("Rumus Dekripsi: P = (C - k) mod 26\n")

    # Tabel pemetaan alfabet

    alphabet_orig = [chr(i) for i in range(65, 91)]  # A - Z
    alphabet_shifted = [chr((i - 65 + shift) % 26 + 65) for i in range(65, 91)]

    row_orig = "Plain  | " + " | ".join(alphabet_orig) + " |"
    row_shift = "Cipher | " + " | ".join(alphabet_shifted) + " |"
    line_sep = "-" * len(row_orig)
    matrix_table = (
        f"```\n{line_sep}\n{row_orig}\n{line_sep}\n{row_shift}\n{line_sep}\n```"
    )

    logs.append("--- **TABEL PEMETAAN ALFABET** ---")
    logs.append(matrix_table)

    # Pergeseran karakter
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
            logs.append(
                f"Langkah {idx}: '{char}' -> Karakter Non-Alfabet (Tidak diubah)"
            )

    # Gabung + pengembalian hasil
    final_result = "".join(result_chars)

    logs.append("\n--- **PROSES SELESAI** ---")
    logs.append(f"Teks Input  : {text}")
    logs.append(f"Teks Hasil  : {final_result}")

    return final_result, logs
