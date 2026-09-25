import pandas as pd

def encrypt(text, rails):
    """
    Enkripsi teks menggunakan Rail Fence Cipher.
    
    Args:
        text: Plaintext yang akan dienkripsi
        rails: Jumlah rail (kunci)
    
    Returns:
        Ciphertext yang terenkripsi
    """
    if rails <= 1:
        return text
    
    # Hapus spasi dan ubah ke uppercase
    text = text.replace(" ", "").upper()
    
    # Buat list untuk setiap rail
    fence = [[] for _ in range(rails)]
    
    rail = 0
    direction = 1  # 1 untuk down, -1 untuk up
    
    # Menempatkan karakter ke dalam rail dengan pola zigzag
    for char in text:
        fence[rail].append(char)
        
        # Ubah arah jika mencapai rail pertama atau terakhir
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    # Gabungkan semua rail untuk membentuk ciphertext
    ciphertext = "".join("".join(row) for row in fence)
    return ciphertext


def decrypt(text, rails):
    """
    Dekripsi teks yang terenkripsi dengan Rail Fence Cipher.
    
    Args:
        text: Ciphertext yang akan didekripsi
        rails: Jumlah rail (kunci)
    
    Returns:
        Plaintext yang terdekripsi
    """
    if rails <= 1:
        return text
    
    # Hitung panjang teks dan tentukan pola fence
    text_len = len(text)
    fence = [[] for _ in range(rails)]
    
    # Tentukan jumlah karakter di setiap rail
    rail = 0
    direction = 1
    fence_len = [0] * rails
    
    for i in range(text_len):
        fence_len[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    # Isi fence dengan karakter dari ciphertext
    idx = 0
    for i in range(rails):
        for j in range(fence_len[i]):
            fence[i].append(text[idx])
            idx += 1
    
    # Baca kembali dengan pola zigzag untuk mendapatkan plaintext
    plaintext = []
    rail = 0
    direction = 1
    fence_idx = [0] * rails
    
    for i in range(text_len):
        plaintext.append(fence[rail][fence_idx[rail]])
        fence_idx[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        
        rail += direction
    
    return "".join(plaintext)


def create_grid_visualization(text, rails, mode="display"):
    """
    Membuat grid untuk visualisasi.
    
    Args:
        text: Teks input
        rails: Jumlah rail
        mode: "encryption" atau "decryption"
    
    Returns:
        DataFrame grid
    """
    
    text = text.replace(" ", "").upper()
    text_len = len(text)
    
    if mode == "encryption":
        # Buat grid untuk enkripsi
        grid = [['' for _ in range(text_len)] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for col, char in enumerate(text):
            grid[rail][col] = char
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        # Buat DataFrame dengan kolom berisi indeks
        df_data = {}
        for col in range(text_len):
            df_data[col] = [grid[row][col] for row in range(rails)]
        
        df = pd.DataFrame(df_data, index=[f"Rail {i+1}" for i in range(rails)])
        df = df.fillna('')
        return df
    
    else:  # decryption
        # Hitung jumlah karakter per rail
        fence_len = [0] * rails
        rail = 0
        direction = 1
        
        for i in range(text_len):
            fence_len[rail] += 1
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        # Distribusi karakter ke rail
        fence = [[] for _ in range(rails)]
        idx = 0
        for i in range(rails):
            for j in range(fence_len[i]):
                fence[i].append(text[idx])
                idx += 1
        
        # Rekonstruksi grid
        grid = [['' for _ in range(text_len)] for _ in range(rails)]
        rail = 0
        direction = 1
        fence_idx = [0] * rails
        
        for col in range(text_len):
            if fence_idx[rail] < len(fence[rail]):
                grid[rail][col] = fence[rail][fence_idx[rail]]
                fence_idx[rail] += 1
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        # Buat DataFrame
        df_data = {}
        for col in range(text_len):
            df_data[col] = [grid[row][col] for row in range(rails)]
        
        df = pd.DataFrame(df_data, index=[f"Rail {i+1}" for i in range(rails)])
        df = df.fillna('')
        return df


def process(text, rails, mode):
    """
    Proses enkripsi atau dekripsi dengan visualisasi langkah-langkah.
    
    Args:
        text: Teks input
        rails: Jumlah rail (kunci)
        mode: "Enkripsi" atau "Dekripsi"
    
    Returns:
        Tuple(result, process_data) dimana process_data berisi:
        - result: Hasil enkripsi/dekripsi
        - intro: Informasi awal
        - steps: List of steps, setiap step berisi {'title', 'description', 'grid', 'content'}
    """
    normalized_text = text.replace(" ", "").upper()
    steps = []
    result = ""
    
    if mode == "Enkripsi":
        # Pengantar
        intro = f"""📝 **Plaintext Asli:** `{text}`
🔑 **Jumlah Rail:** `{rails}`
✏️ **Teks Setelah Normalisasi:** `{normalized_text}`"""
        
        # ===== STEP 1: Pola Penulisan Zigzag =====
        step1_title = "📊 STEP 1: Pola Penulisan Zigzag"
        step1_desc = "Karakter ditulis secara zigzag dengan arah naik-turun pada setiap kolom"
        
        grid_df = create_grid_visualization(text, rails, "encryption")
        
        steps.append({
            "title": step1_title,
            "description": step1_desc,
            "grid": grid_df,
            "content": None
        })
        
        # ===== STEP 2: Pembacaan per Rail =====
        step2_title = "🔐 STEP 2: Pembacaan Karakter per Rail"
        step2_desc = "Ciphertext dibentuk dengan membaca setiap rail dari kiri ke kanan"
        
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in normalized_text:
            fence[rail].append(char)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        # Visualisasi pembacaan
        step2_content = []
        for i, row in enumerate(fence):
            if len(row) > 0:
                rail_chars = " + ".join(row)
                rail_result = "".join(row)
                step2_content.append(f"**Rail {i+1}:** {rail_chars} → `{rail_result}`")
        
        steps.append({
            "title": step2_title,
            "description": step2_desc,
            "grid": None,
            "content": step2_content
        })
        
        # ===== STEP 3: Hasil Akhir =====
        result = encrypt(text, rails)
        step3_title = "✅ STEP 3: Hasil Akhir"
        concatenated = " + ".join(["".join(row) for row in fence])
        step3_content = [
            f"**Penggabungan Rail:** {concatenated}",
            f"**Ciphertext:** `{result}`"
        ]
        
        steps.append({
            "title": step3_title,
            "description": None,
            "grid": None,
            "content": step3_content
        })
        
    else:  # Dekripsi
        # Pengantar
        intro = f"""🔓 **Ciphertext Input:** `{text}`
🔑 **Jumlah Rail:** `{rails}`

Untuk mendekripsi, kita perlu merekonstruksi grid zigzag dari ciphertext, kemudian membaca ulang sesuai pola zigzag."""
        
        text_len = len(text)
        
        # ===== STEP 1: Hitung dan Rekonstruksi =====
        step1_title = "📊 STEP 1: Hitung Karakter per Rail & Rekonstruksi Grid"
        step1_desc = "Hitung berapa karakter di setiap rail, distribusikan ciphertext, dan masukkan ke grid"
        
        fence_len = [0] * rails
        rail = 0
        direction = 1
        
        for i in range(text_len):
            fence_len[rail] += 1
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        # Konten step 1
        step1_content = []
        step1_content.append("**Langkah 1a: Hitung berapa karakter di setiap rail**")
        for i, count in enumerate(fence_len):
            step1_content.append(f"- Rail {i+1}: **{count} karakter**")
        
        step1_content.append("")
        step1_content.append("**Langkah 1b: Distribusikan ciphertext ke setiap rail**")
        
        # Distribusi ciphertext ke rail
        fence = [[] for _ in range(rails)]
        idx = 0
        for i in range(rails):
            for j in range(fence_len[i]):
                fence[i].append(text[idx])
                idx += 1
        
        for i, row in enumerate(fence):
            if len(row) > 0:
                rail_result = "".join(row)
                step1_content.append(f"- Rail {i+1}: `{rail_result}`")
        
        step1_content.append("")
        step1_content.append("**Langkah 1c: Grid Rekonstruksi**")
        
        grid_df = create_grid_visualization(text, rails, "decryption")
        
        steps.append({
            "title": step1_title,
            "description": step1_desc,
            "grid": grid_df,
            "content": step1_content
        })
        
        # ===== STEP 2: Pembacaan Plaintext =====
        step2_title = "📖 STEP 2: Baca Grid Sesuai Pola Zigzag"
        step2_desc = "Membaca grid dengan mengikuti pola zigzag yang sama saat enkripsi"
        
        step2_content = []
        step2_content.append("**Cara membaca:**")
        step2_content.append("- Mulai dari Rail 1, bergerak ke bawah")
        step2_content.append("- Ketika sampai Rail terakhir, bergerak ke atas")
        step2_content.append("- Lanjutkan pola ini sampai semua karakter terbaca")
        step2_content.append("")
        
        result = decrypt(text, rails)
        
        # Visualisasi pembacaan karakter
        plaintext_chars = []
        rail = 0
        direction = 1
        fence_idx = [0] * rails
        
        for i in range(text_len):
            plaintext_chars.append(fence[rail][fence_idx[rail]])
            fence_idx[rail] += 1
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        char_trace = " + ".join(plaintext_chars)
        step2_content.append(f"**Urutan pembacaan:** `{char_trace}`")
        
        steps.append({
            "title": step2_title,
            "description": step2_desc,
            "grid": None,
            "content": step2_content
        })
        
        # ===== STEP 3: Hasil Akhir =====
        step3_title = "✅ STEP 3: Hasil Akhir"
        step3_content = [f"**Plaintext:** `{result}`"]
        
        steps.append({
            "title": step3_title,
            "description": None,
            "grid": None,
            "content": step3_content
        })
    
    process_data = {
        "result": result,
        "intro": intro,
        "steps": steps
    }
    
    return result, process_data
