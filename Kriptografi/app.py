import random
import smtplib
import string
from email.mime.text import MIMEText

import blowfish
import caesar
import rail_fence
import streamlit as st
from session_manager import session_manager
import super_enkripsi
import vernam

# ==============================================================================
# FUNGSI OTP GMAIL (LANGSUNG DITULIS DI SINI TANPA FILE PENDUKUNG BARU)
# ==============================================================================
SENDER_EMAIL = "isi_email@gmail.com"  # Ganti dengan email pengirim
SENDER_PASSWORD = (
    "xxxx xxxx xxxx xxxx"  # Ganti dengan App Password Gmail 16 digit
)


def generate_otp_key(length):
    """Menghasilkan kunci acak sepanjang teks."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def send_otp_email(recipient_email, otp_key, text_length):
    """Mengirim kunci Vernam (OTP) ke Gmail penerima via SMTP SSL."""
    subject = "🔑 KUNCI OTP VERNAM CIPHER (SANGAT RAHASIA)"
    body = f"""Halo,

Berikut adalah Kunci OTP (One-Time Pad) Vernam Cipher Anda:

🔑 KUNCI OTP : {otp_key}
📏 PANJANG   : {text_length} karakter

⚠️ PERHATIAN:
- Kunci ini HANYA BISA DIPAKAI 1 KALI untuk proses Dekripsi.
- Setelah digunakan, kunci ini akan otomatis HANGUS / DIHAPUS oleh sistem.

Salam,
Tim KriptoAsik
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        return True, "Email OTP berhasil dikirim!"
    except Exception as e:
        return False, f"Gagal mengirim email: {str(e)}"


# ==============================================================================
# KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="APLIKASI KRIPTOGRAFI", page_icon="🔐", layout="wide"
)

st.markdown(
    """
<style>
    :root {
        --app-bg: #151a17;
        --sidebar-bg: #191f1b;
        --surface: #202722;
        --surface-raised: #29322c;
        --line: #3a463e;
        --text: #e9efeb;
        --muted: #a5b0a8;
        --accent: #47a879;
        --accent-soft: #20372a;
        --accent-alt: #d1ad67;
    }

    .stApp {
        background: var(--app-bg);
        color: var(--text);
    }
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        border-right: 1px solid var(--line);
    }
    .main-header {
        padding: 0 0 14px;
        margin-bottom: 22px;
        border-bottom: 1px solid var(--line);
        color: var(--text);
        font-family: "Segoe UI", sans-serif;
    }
    .main-header h3 {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .process-box {
        background: var(--surface);
        border: 1px solid var(--line);
        padding: 16px;
        border-radius: 6px;
    }
    .key-preview-box {
        background: var(--surface);
        border: 1px solid var(--line);
        border-left: 3px solid var(--accent);
        padding: 12px 14px;
        border-radius: 4px;
        line-height: 1.8;
    }
    .algo-chip {
        display: inline-block;
        background: var(--accent-soft);
        color: #a9dfbf;
        padding: 4px 9px;
        border-radius: 4px;
        margin: 3px 0;
        font-weight: 600;
        font-size: 0.85em;
        border: 1px solid #42644d;
    }
    .algo-chip-dec {
        background: #353126;
        color: #e4cf9e;
        border-color: #65583b;
    }
    .algo-arrow {
        color: var(--muted);
        margin: 0 5px;
        font-size: 1em;
    }
    [data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 5px;
        background: var(--surface);
    }
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background: var(--surface);
        border-color: var(--line);
        border-radius: 4px;
    }
    .stButton > button {
        min-height: 2.5rem;
        border-radius: 4px;
        border-color: var(--line);
        font-weight: 600;
    }
    .stButton > button[kind="primary"] {
        background: var(--accent);
        border-color: var(--accent);
        color: #101713;
    }
    .stButton > button[kind="primary"]:hover {
        background: #59b989;
        border-color: #59b989;
        color: #101713;
    }
    [data-testid="stCode"] pre {
        border: 1px solid var(--line);
        border-radius: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header Utama
st.markdown(
    """
<div class="main-header">
    <h3 style="margin:0; padding:0;"> APLIKASI KRIPTOGRAFI</h3>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("MENU")

    menu = st.radio(
        "Pilih Algoritma:",
        [
            "Caesar Cipher",
            "Rail Fence Cipher",
            "Vernam Cipher (OTP)",
            "Blowfish Cipher",
            "Super Enkripsi",
        ],
    )

    st.markdown("---")
    session_manager.display_history_widget(show_limit=50)
    st.markdown("---")

    st.title("Anggota")
    st.write("- **Bylbiss El Haqqie** 123240003")
    st.write("- **Muhammad Restu Firmansyah** 123240050")
    st.write("- **Alifah Chairul Munawar** 123240234")

# Mode Enkripsi/Dekripsi
mode = st.radio("Mode Operasi:", ["Enkripsi", "Dekripsi"], horizontal=True)

st.markdown("---")

# Penentuan Label Dinamis
input_label = (
    "Input Plaintext (Teks Asli):"
    if mode == "Enkripsi"
    else "Input Ciphertext (Teks Terenkripsi):"
)
input_placeholder = (
    "Masukkan pesan teks asli di sini..."
    if mode == "Enkripsi"
    else "Masukkan pesan cipher di sini..."
)
output_label = (
    "Hasil Akhir (Ciphertext):"
    if mode == "Enkripsi"
    else "Hasil Akhir (Plaintext):"
)

# 1. Menu 1 - 4 (Algoritma Individual)
if menu != "Super Enkripsi":
    st.subheader(f"Form {menu}")

    # Input Teks
    text_input = st.text_area(
        input_label, placeholder=input_placeholder, height=100
    )

    # Input Kunci
    if "Caesar" in menu or "Rail" in menu:
        key_input = st.number_input(
            "Kunci (Key Integer):", min_value=1, value=3, step=1
        )
    elif "Vernam" in menu:
        st.markdown("---")
        st.markdown("#### 📧 Integrasi OTP Gmail (Kunci 1x Pakai)")
        col_email, col_btn = st.columns([2, 1])

        with col_email:
            recipient_email = st.text_input(
                "Alamat Gmail Penerima OTP:", placeholder="contoh@gmail.com"
            )

        with col_btn:
            st.write("")
            st.write("")
            btn_send_otp = st.button("📩 Generate & Kirim OTP")

        if btn_send_otp:
            if not text_input:
                st.warning("⚠️ Masukkan teks terlebih dahulu!")
            elif not recipient_email:
                st.warning("⚠️ Masukkan email penerima!")
            else:
                # Menggunakan fungsi lokal generate_otp_key
                generated_key = generate_otp_key(len(text_input))
                success, msg = send_otp_email(
                    recipient_email, generated_key, len(text_input)
                )

                if success:
                    st.session_state["vernam_active_otp"] = generated_key
                    st.success(f"✅ {msg} Cek inbox {recipient_email}.")
                else:
                    st.error(f"❌ {msg}")

        key_input = st.text_input(
            "Kunci Vernam / Paste OTP dari Gmail:",
            placeholder="Masukkan kunci...",
            type="password" if mode == "Dekripsi" else "default",
        )
        st.markdown("---")
    else:
        key_input = st.text_input(
            "Kunci (Key Text/Hex):", placeholder="Masukkan kunci..."
        )

    # Tombol Eksekusi
    btn_process = st.button(f"[ PROSES {mode.upper()} ]", type="primary")

    st.markdown("---")
    st.subheader("📊 PROSES DETAIL ALGORITMA")

    with st.container():
        if btn_process and text_input:
            logs = None
            process_data = None

            if "Caesar" in menu:
                result, logs = caesar.process(text_input, key_input, mode)
            elif "Rail Fence" in menu:
                result, process_data = rail_fence.process(
                    text_input, key_input, mode
                )
            elif "Vernam" in menu:
                active_otp = st.session_state.get("vernam_active_otp")

                # Cek Mekanisme One-Time Use jika menggunakan OTP
                if mode == "Dekripsi" and active_otp:
                    if key_input != active_otp:
                        result = "Error: Kunci OTP Salah atau Sudah Kadaluarsa!"
                        logs = [
                            "❌ Kunci tidak cocok dengan OTP yang dikirim atau kunci sudah pernah digunakan!"
                        ]
                    else:
                        result, logs = vernam.process(
                            text_input, key_input, mode
                        )
                        # Hanguskan kunci setelah 1x pakai
                        del st.session_state["vernam_active_otp"]
                        logs.append(
                            "\n⚠️ **SISTEM OTP:** Kunci OTP ini telah **HANGUS / DIHAPUS** dari memory dan tidak dapat digunakan kembali!"
                        )
                else:
                    result, logs = vernam.process(text_input, key_input, mode)

            elif "Blowfish" in menu:
                result, logs = blowfish.process(text_input, key_input, mode)

            session_manager.add_to_history(
                text=text_input,
                algorithm=menu,
                mode=mode,
                key=str(key_input),
                result=result,
            )

            st.markdown('<div class="process-box">', unsafe_allow_html=True)

            if "Rail Fence" in menu:
                st.write(process_data["intro"])
                st.markdown("---")
                for i, step in enumerate(process_data["steps"], 1):
                    with st.expander(f"▶ {step['title']}", expanded=(i == 1)):
                        if step["description"]:
                            st.write(f"*{step['description']}*")
                            st.markdown("---")
                        if step["grid"] is not None:
                            st.dataframe(step["grid"], width="stretch")
                            st.markdown("---")
                        if step["content"]:
                            for content in step["content"]:
                                st.write(content)
            elif "Blowfish" in menu:
                for log in logs:
                    st.markdown(log, unsafe_allow_html=True)
            else:
                for log in logs:
                    st.write(log)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Tekan tombol proses untuk melihat visualisasi proses.")
            result = "Hasil akan tampil di sini..."

    st.markdown(f"### {output_label}")
    st.code(result, language="text")

# 2. Super Enkripsi
else:
    st.subheader("🔗 Form Super Enkripsi (Multi-Cipher)")

    with st.expander("💡 Apa itu Super Enkripsi?", expanded=False):
        st.markdown(
            """
            **Super Enkripsi** menggabungkan 4 algoritma (Caesar, Rail Fence,
            Vernam, Blowfish) secara berantai, cukup menggunakan **1 kunci
            utama**. Kunci utama ini otomatis diturunkan menjadi parameter
            kunci untuk masing-masing algoritma.

            - Urutan yang kamu pilih dipakai persis saat **Enkripsi**.
            - Saat **Dekripsi**, urutan tersebut otomatis **dibalik** supaya
              hasilnya bisa kembali ke teks semula.
            """
        )

    input_source = st.radio(
        "Pilih sumber input:",
        ["Input Manual", "Pilih dari History"],
        horizontal=True,
        key="super_input_source",
    )

    if input_source == "Input Manual":
        text_input = st.text_area(
            "Input Teks Utama (Plaintext / Ciphertext):",
            placeholder="Masukkan pesan utama yang ingin di-super enkripsi...",
            height=100,
            key="super_text_input",
        )
    else:
        history_texts = session_manager.get_unique_texts()
        if history_texts:
            selected_history = st.selectbox(
                "Pilih teks dari history:",
                options=range(len(history_texts)),
                format_func=lambda index: (
                    f"[{history_texts[index]['algorithm']}] "
                    f"{history_texts[index]['text'][:50]}"
                    f"{'...' if len(history_texts[index]['text']) > 50 else ''}"
                ),
                key="super_history_selection",
            )
            text_input = history_texts[selected_history]["text"]
            st.text_area("Teks terpilih:", value=text_input, height=100, disabled=True)
        else:
            st.info("Belum ada history. Silakan gunakan Input Manual.")
            text_input = ""

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔑 Kunci Utama (Master Key)")
        master_key = st.text_input(
            "Satu kunci untuk semua algoritma:",
            value="KRIPTO2026",
            placeholder="Masukkan 1 kunci utama...",
        )

        if master_key:
            k_caesar, k_rail, k_vernam, k_blowfish = super_enkripsi.derive_keys(
                master_key
            )
            st.markdown(
                f"""
                <div class="key-preview-box">
                <b>🔧 Kunci turunan otomatis:</b><br>
                • Caesar &nbsp;&nbsp;: <code>{k_caesar}</code><br>
                • Rail Fence : <code>{k_rail}</code> rail<br>
                • Vernam &nbsp;&nbsp;: <code>{k_vernam}</code><br>
                • Blowfish &nbsp;: <code>{k_blowfish}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ Kunci utama belum diisi.")

    with col2:
        st.markdown("#### 🔀 Urutan Eksekusi Algoritma")

        def _reset_algo_order():
            st.session_state["super_algo_order"] = []

        def _default_algo_order():
            st.session_state["super_algo_order"] = [
                "Caesar",
                "Rail Fence",
                "Vernam",
                "Blowfish",
            ]

        st.session_state.setdefault(
            "super_algo_order", ["Caesar", "Rail Fence", "Vernam", "Blowfish"]
        )

        algo_order = st.multiselect(
            "Klik sesuai urutan yang diinginkan (klik pertama = tahap 1):",
            options=["Caesar", "Rail Fence", "Vernam", "Blowfish"],
            help="Saat Mode Dekripsi, urutan ini otomatis dibalik.",
            key="super_algo_order",
        )

        col_reset, col_default = st.columns(2)
        with col_reset:
            st.button(
                "🗑️ Kosongkan",
                width="stretch",
                on_click=_reset_algo_order,
            )
        with col_default:
            st.button(
                "↩️ Urutan Bawaan",
                width="stretch",
                on_click=_default_algo_order,
            )

        if algo_order:
            chips_enc = "".join(
                f'<span class="algo-chip">{i + 1}. {a}</span>'
                + (
                    ' <span class="algo-arrow">→</span> '
                    if i < len(algo_order) - 1
                    else ""
                )
                for i, a in enumerate(algo_order)
            )
            chips_dec = "".join(
                f'<span class="algo-chip algo-chip-dec">{i + 1}. {a}</span>'
                + (
                    ' <span class="algo-arrow">→</span> '
                    if i < len(algo_order) - 1
                    else ""
                )
                for i, a in enumerate(reversed(algo_order))
            )
            st.markdown(
                f"**Urutan Enkripsi:**<br>{chips_enc}", unsafe_allow_html=True
            )
            st.markdown(
                f"**Urutan Dekripsi:**<br>{chips_dec}", unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Pilih minimal 1 algoritma untuk urutan eksekusi.")

    st.markdown("---")

    btn_super = st.button(
        f"[ PROSES SUPER {mode.upper()} ]",
        type="primary",
        disabled=not (algo_order and master_key),
    )

    st.markdown("---")
    st.subheader("📊 PROSES DETAIL ALGORITMA BERANTAI (Langkah demi Langkah)")

    if btn_super and text_input and master_key and algo_order:
        result_super, logs_super = super_enkripsi.process(
            text_input, master_key, algo_order, mode
        )
        session_manager.add_to_history(
            text=text_input,
            algorithm="Super Enkripsi",
            mode=mode,
            key=f"{master_key} | {' → '.join(algo_order)}",
            result=result_super,
        )

        intro_logs = []
        stage_logs = []
        current_stage_title = None
        current_stage_logs = []
        summary_logs = []

        for log in logs_super:
            if isinstance(log, dict) and "rail_fence_process_data" in log:
                if current_stage_title is not None:
                    current_stage_logs.append(log)
            elif log.startswith("--- **TAHAP "):
                if current_stage_title is not None:
                    stage_logs.append((current_stage_title, current_stage_logs))
                current_stage_title = log.removeprefix("--- **").removesuffix("** ---")
                current_stage_logs = []
            elif log.startswith("--- **PROSES SUPER-ENKRIPSI SELESAI** ---"):
                if current_stage_title is not None:
                    stage_logs.append((current_stage_title, current_stage_logs))
                    current_stage_title = None
                    current_stage_logs = []
                summary_logs.append(log)
            elif current_stage_title is None:
                if stage_logs:
                    summary_logs.append(log)
                else:
                    intro_logs.append(log)
            else:
                current_stage_logs.append(log)

        if current_stage_title is not None:
            stage_logs.append((current_stage_title, current_stage_logs))

        with st.container():
            for log in intro_logs:
                st.markdown(log, unsafe_allow_html=True)

            for index, (stage_title, logs) in enumerate(stage_logs):
                with st.expander(stage_title, expanded=(index == 0)):
                    for log in logs:
                        if isinstance(log, dict) and "rail_fence_process_data" in log:
                            process_data = log["rail_fence_process_data"]
                            st.markdown(process_data["intro"])
                            st.markdown("---")

                            for step_index, step in enumerate(process_data["steps"], 1):
                                with st.expander(
                                    f"▶ {step['title']}",
                                    expanded=(step_index == 1),
                                ):
                                    if step["description"]:
                                        st.write(f"*{step['description']}*")
                                        st.markdown("---")
                                    if step["grid"] is not None:
                                        st.dataframe(step["grid"], width="stretch")
                                        st.markdown("---")
                                    if step["content"]:
                                        for content in step["content"]:
                                            st.write(content)
                        else:
                            st.markdown(log, unsafe_allow_html=True)

            for log in summary_logs:
                st.markdown(log, unsafe_allow_html=True)
    else:
        if not text_input:
            st.info("Tekan tombol proses untuk melihat visualisasi proses berantai.")
        elif not master_key:
            st.warning("⚠️ Isi kunci utama terlebih dahulu.")
        elif not algo_order:
            st.warning("⚠️ Pilih minimal 1 algoritma untuk urutan eksekusi.")
        result_super = "Hasil super enkripsi akan tampil di sini..."

    st.markdown(f"### {output_label}")
    st.code(result_super, language="text")
