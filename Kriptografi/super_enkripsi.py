import caesar
import rail_fence
import vernam
import blowfish


def derive_keys(user_key):
    """
    Menderivasi 1 Kunci Utama menjadi parameter kunci untuk 4 algoritma.

    Catatan penyesuaian dengan modul yang sudah ada:
    - caesar.process(text, key:int, mode)      -> butuh int
    - rail_fence.encrypt/decrypt(text, rails:int) -> butuh int (>= 2)
    - vernam.process(text, key:str, mode)      -> butuh str (vernam.py SUDAH
      otomatis mengulang kunci jika lebih pendek dari teks, jadi cukup
      dikirim apa adanya di sini)
    - blowfish.process(text, key:str, mode)    -> butuh STRING (bukan bytes!)
      dengan panjang 4-56 byte setelah di-encode UTF-8
    """
    # 1. Caesar: total nilai ASCII modulo 26
    k_caesar = sum(ord(c) for c in user_key) % 26 if user_key else 3

    # 2. Rail Fence: panjang kunci (minimal 2 rail)
    k_rail = max(2, (len(user_key) % 5) + 2) if user_key else 3

    # 3. Vernam: teks kunci apa adanya (vernam.py akan mengulang otomatis
    #    jika panjangnya lebih pendek dari teks yang diproses)
    k_vernam = user_key if user_key else "KEY"

    # 4. Blowfish: HARUS string (blowfish.py yang sudah ada menerima
    #    `key: str` lalu meng-encode sendiri ke UTF-8), panjang 4-56 byte
    k_blowfish = user_key if user_key else "KEY1"
    if len(k_blowfish.encode("utf-8")) < 4:
        k_blowfish = k_blowfish.ljust(4, "0")
    while len(k_blowfish.encode("utf-8")) > 56:
        k_blowfish = k_blowfish[:-1]

    return k_caesar, k_rail, k_vernam, k_blowfish


def _is_error(hasil):
    """Deteksi apakah output sebuah tahap sebenarnya adalah pesan error,
    supaya tidak ikut dirantai ke tahap berikutnya seolah-olah data valid."""
    if not isinstance(hasil, str):
        return False
    penanda_error = ("Error:", "Gagal!", "Gagal Dekripsi!", "Kunci Tidak Valid")
    return any(hasil.startswith(p) or p in hasil for p in penanda_error)


def _rail_fence_stage(current_text, k_rail, mode):
    """
    Menjalankan Rail Fence Cipher sebagai satu tahap di dalam rantai
    Super Enkripsi.

    rail_fence.py yang sudah ada MEMAKSA uppercase & menghapus spasi
    (`text.replace(" ", "").upper()`). Ini aman untuk teks biasa, tapi akan
    MERUSAK output Vernam (berformat "AB CD EF" berspasi) dan output
    Blowfish (Base64 yang case-sensitive: huruf besar/kecil dan '+ / ='
    berarti berbeda) jika Rail Fence berada tepat sesudahnya dalam rantai.

    Solusi tanpa mengubah rail_fence.py: teks diubah dulu ke representasi
    HEX (otomatis uppercase, tanpa spasi) sebelum masuk Rail Fence, lalu
    dikembalikan ke bentuk aslinya sesudahnya. Dengan begitu Rail Fence
    hanya "mengacak posisi" tanpa pernah menyentuh karakter asli secara
    langsung, sehingga aman dipakai di urutan manapun.
    """
    logs = [f"Kunci Rail Fence : {k_rail} rail"]

    if mode == "Enkripsi":
        utf8_bytes = current_text.encode("utf-8")
        hex_input = utf8_bytes.hex().upper()
        byte_conversions = " | ".join(
            f"{byte} -> {byte:02X}" for byte in utf8_bytes
        )
        logs.extend(
            [
                "**Konversi teks ke HEX (UTF-8):**",
                f"1. Teks sebelum Rail Fence: `{current_text}`",
                f"2. Encode ke byte UTF-8 (desimal): `{list(utf8_bytes)}`",
                f"3. Ubah setiap byte ke 2 digit HEX: `{byte_conversions}`",
                f"4. Gabungkan byte HEX tanpa spasi: `{hex_input}`",
                "HEX dipakai agar huruf besar/kecil dan spasi pada data asli "
                "tetap aman dari normalisasi Rail Fence.",
            ]
        )
        hasil_rail, process_data = rail_fence.process(hex_input, k_rail, mode)
        logs.append({"rail_fence_process_data": process_data})
        logs.append(f"Hasil pengacakan Rail Fence (atas data HEX) : `{hasil_rail}`")
        return hasil_rail, logs

    # Dekripsi
    hasil_rail, process_data = rail_fence.process(current_text, k_rail, mode)
    logs.append({"rail_fence_process_data": process_data})
    logs.append(f"Hasil susun-ulang Rail Fence (masih berbentuk HEX) : `{hasil_rail}`")
    logs.append("**Konversi HEX kembali ke teks (UTF-8):**")
    try:
        decoded_bytes = bytes.fromhex(hasil_rail)
        hex_pairs = [
            hasil_rail[index:index + 2]
            for index in range(0, len(hasil_rail), 2)
        ]
        byte_conversions = " | ".join(
            f"{hex_pair} -> {byte}"
            for hex_pair, byte in zip(hex_pairs, decoded_bytes)
        )
        logs.append(f"1. Pisahkan HEX per 2 digit: `{' '.join(hex_pairs)}`")
        logs.append(f"2. Ubah pasangan HEX menjadi byte desimal: `{byte_conversions}`")
        hasil_akhir = decoded_bytes.decode("utf-8")
        logs.append(f"3. Decode byte UTF-8 menjadi teks: `{hasil_akhir}`")
        return hasil_akhir, logs
    except (ValueError, UnicodeDecodeError) as e:
        logs.append(f"⚠️ Gagal mengonversi HEX kembali ke teks: {e}")
        return f"Error: Gagal konversi HEX pada tahap Rail Fence ({e})", logs


def process(text, user_key, algo_order, mode):
    """
    Memproses Super-Enkripsi / Super-Dekripsi secara berantai, dengan
    urutan algoritma bebas ditentukan pengguna (algo_order).
    """
    if not user_key:
        return "Error: Kunci tidak boleh kosong!", ["⚠️ KUNCI UTAMA TIDAK BOLEH KOSONG!"]

    if not algo_order:
        return "Error: Pilih minimal 1 algoritma!", ["⚠️ PILIH MINIMAL 1 ALGORITMA UNTUK DIPROSES!"]

    # Derivasi Kunci Utama
    k_caesar, k_rail, k_vernam, k_blowfish = derive_keys(user_key)

    all_logs = []
    current_text = text

    all_logs.append(f"**SUPER-ENKRIPSI ({mode.upper()})**")
    all_logs.append(f"• Kunci Utama User : `{user_key}`")
    all_logs.append("• Derivasi Kunci   :")
    all_logs.append(f"  - Caesar Key     : {k_caesar}")
    all_logs.append(f"  - Rail Fence Key : {k_rail}")
    all_logs.append(f"  - Vernam Key     : {k_vernam}")
    all_logs.append(f"  - Blowfish Key   : {k_blowfish}")

    # Mode Dekripsi: urutan otomatis dibalik (reversed)
    execution_order = algo_order if mode == "Enkripsi" else list(reversed(algo_order))
    all_logs.append(f"• Urutan Eksekusi  : {' -> '.join(execution_order)}\n")

    for step, algo in enumerate(execution_order, start=1):
        all_logs.append(f"--- **TAHAP {step}: {algo.upper()} CIPHER ({mode.upper()})** ---")
        all_logs.append(f"Input Tahap Ini : `{current_text}`")

        if algo == "Caesar":
            current_text, logs = caesar.process(current_text, k_caesar, mode)
        elif algo == "Rail Fence":
            current_text, logs = _rail_fence_stage(current_text, k_rail, mode)
        elif algo == "Vernam":
            current_text, logs = vernam.process(current_text, k_vernam, mode)
        elif algo == "Blowfish":
            # blowfish.py sudah punya CSS + expander HTML sendiri di dalam
            # logs-nya, jadi cukup diteruskan apa adanya.
            current_text, logs = blowfish.process(current_text, k_blowfish, mode)
        else:
            logs = [f"⚠️ Algoritma '{algo}' tidak dikenali!"]

        all_logs.extend(logs)
        all_logs.append(f"Output Tahap {step} : `{current_text}`\n")

        # Hentikan rantai lebih awal jika satu tahap gagal, supaya pesan
        # error tidak ikut "dienkripsi" oleh tahap berikutnya seolah data
        # yang valid (bug yang pernah terjadi sebelumnya).
        if _is_error(current_text):
            all_logs.append(
                f"❌ **PROSES DIHENTIKAN** pada Tahap {step} ({algo}) karena terjadi error di atas."
            )
            return current_text, all_logs

    all_logs.append("--- **PROSES SUPER-ENKRIPSI SELESAI** ---")
    all_logs.append(f"Teks Awal  : `{text}`")
    all_logs.append(f"Hasil Akhir: `{current_text}`")

    return current_text, all_logs