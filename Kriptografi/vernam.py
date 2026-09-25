def process(text, key, mode):
    """
    Modul Pemroses Vernam Cipher / One-Time Pad (OTP)

    Kunci otomatis diulang (looping) jika lebih pendek dari pesan, sehingga
    proses Enkripsi & Dekripsi selalu konsisten dan bisa dibolak-balik
    selama kunci yang sama persis dipakai di kedua proses.
    """
    logs = []

    # ------------------------------------------------------------------
    # 1. Validasi input kunci
    # ------------------------------------------------------------------
    if not key:
        return "Error: Kunci tidak boleh kosong!", ["KUNCI TIDAK BOLEH KOSONG! Masukkan kunci teks."]

    # ------------------------------------------------------------------
    # 2. Tentukan jumlah karakter/blok yang benar-benar akan diproses
    #    - Enkripsi : dihitung dari jumlah karakter teks asli
    #    - Dekripsi : dihitung dari jumlah BLOK Hex (bukan panjang string
    #                 mentahnya, karena string hex mengandung spasi dan
    #                 tiap karakter aslinya diwakili 2 digit hex)
    # ------------------------------------------------------------------
    if mode == "Enkripsi":
        required_length = len(text)
        hex_blocks = None
    else:
        hex_blocks = text.split()
        required_length = len(hex_blocks)

    if required_length == 0:
        return "", ["Teks input kosong, tidak ada yang diproses."]

    logs.append("=" * 60)
    logs.append(f"MODE {mode.upper()} | Vernam Cipher (One-Time Pad / OTP)")
    logs.append("=" * 60)

    # ------------------------------------------------------------------
    # 3. PENYELARASAN KUNCI — dijelaskan sebagai langkah tersendiri
    #    agar terlihat jelas dari mana kunci final berasal.
    # ------------------------------------------------------------------
    logs.append("\n[ TAHAP 1 ] PENYELARASAN PANJANG KUNCI")
    logs.append(f"  Kunci asli     : '{key}'  (panjang {len(key)} karakter)")
    logs.append(f"  Panjang target : {required_length} karakter "
                f"({'teks asli' if mode == 'Enkripsi' else 'jumlah blok Hex'})")

    if len(key) < required_length:
        jumlah_ulang = (required_length // len(key)) + 1
        logs.append(f"  -> Kunci lebih pendek dari pesan, diulang {jumlah_ulang}x lalu dipotong pas.")
        extended_key = (key * jumlah_ulang)[:required_length]
    else:
        logs.append("  -> Kunci sudah cukup/lebih panjang, cukup dipotong pas dengan pesan.")
        extended_key = key[:required_length]

    logs.append(f"  Kunci final yang dipakai : '{extended_key}'")

    # ------------------------------------------------------------------
    # 4. PROSES XOR PER KARAKTER — bagian utama, dibuat lebih detail
    #    dengan menampilkan representasi biner tiap nilai supaya
    #    proses XOR terlihat jelas, bukan cuma angkanya saja.
    # ------------------------------------------------------------------
    logs.append("\n[ TAHAP 2 ] PROSES XOR PER KARAKTER")
    logs.append("  Rumus Enkripsi : Ciphertext = ASCII(Plaintext) XOR ASCII(Kunci)")
    logs.append("  Rumus Dekripsi : Plaintext  = ASCII(Ciphertext) XOR ASCII(Kunci)")
    logs.append("  (setiap nilai ASCII ditampilkan juga dalam biner 8-bit agar operasi XOR terlihat jelas)\n")

    result_chars = []

    if mode == "Enkripsi":
        for i in range(required_length):
            p = text[i]
            k = extended_key[i]

            p_ascii, k_ascii = ord(p), ord(k)
            p_bin, k_bin = format(p_ascii, "08b"), format(k_ascii, "08b")

            xor_val = p_ascii ^ k_ascii
            xor_bin = format(xor_val, "08b")
            hex_val = f"{xor_val:02X}"

            result_chars.append(hex_val)

            logs.append(
                f"  Langkah {i + 1:>3}: Teks  '{p}' = {p_ascii:>3}  = {p_bin}\n"
                f"             Kunci '{k}' = {k_ascii:>3}  = {k_bin}\n"
                f"             XOR        = {xor_val:>3}  = {xor_bin}  -> Hex: {hex_val}\n"
                f"             Progres hasil sejauh ini : {' '.join(result_chars)}"
            )

        final_result = " ".join(result_chars)

    else:
        # MODE DEKRIPSI (menerima input berupa blok Hex, contoh: "1A 2B 3C")
        for i, h in enumerate(hex_blocks):
            k = extended_key[i]
            k_ascii = ord(k)
            k_bin = format(k_ascii, "08b")

            try:
                c_val = int(h, 16)
                c_bin = format(c_val, "08b")

                p_val = c_val ^ k_ascii
                p_bin = format(p_val, "08b")
                p_char = chr(p_val)

                result_chars.append(p_char)

                logs.append(
                    f"  Langkah {i + 1:>3}: Hex   '{h}' = {c_val:>3}  = {c_bin}\n"
                    f"             Kunci '{k}' = {k_ascii:>3}  = {k_bin}\n"
                    f"             XOR        = {p_val:>3}  = {p_bin}  -> Karakter: '{p_char}'\n"
                    f"             Progres hasil sejauh ini : {''.join(result_chars)}"
                )
            except ValueError:
                result_chars.append("?")
                logs.append(f"  Langkah {i + 1:>3}: Blok Hex '{h}' tidak valid (bukan format heksadesimal)!")

        final_result = "".join(result_chars)

    # ------------------------------------------------------------------
    # 5. RINGKASAN AKHIR
    # ------------------------------------------------------------------
    logs.append("\n" + "=" * 60)
    logs.append("PROSES SELESAI")
    logs.append("=" * 60)
    logs.append(f"Teks Input : {text}")
    logs.append(f"Teks Hasil : {final_result}")

    return final_result, logs