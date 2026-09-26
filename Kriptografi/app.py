import blowfish
import caesar
import rail_fence
import streamlit as st
import super_enkripsi
import vernam

# Konfig Halaman Streamlit
st.set_page_config(
    page_title="Kriptografi", layout="wide"
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
    <h3 style="margin:0; padding:0;">Aplikasi Kriptografi</h3>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("Menu")

    # Pilih Menu
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
    st.title("Anggota")
    st.write("- **Bylbiss El Haqqie** 123240003")
    st.write("- **Muhammad Restu Firmansyah** 123240050")
    st.write("- **Alifah Chairul Munawar** 123240234")

# Halaman Utama

# Mode Enkripsi/Dekripsi
mode = st.radio("Mode Operasi:", ["Enkripsi", "Dekripsi"], horizontal=True)

st.markdown("---")

# Penentuan Label Dinamis berdasarkan Mode
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
    else:
        key_input = st.text_input(
            "Kunci (Key Text/Hex):", placeholder="Masukkan kunci..."
        )

    # Tombol Eksekusi
    btn_process = st.button(f"Proses {mode}", type="primary")

    st.markdown("---")
    st.subheader("Langkah proses")

    # Container Log Visualisasi Proses
    with st.container():
        if btn_process and text_input:
            logs = None
            process_data = None

            if "Caesar" in menu:
                result, logs = caesar.process(text_input, key_input, mode)
            elif "Rail Fence" in menu:
                # rail_fence.process() mengembalikan dict berisi intro/steps/grid,
                # BUKAN list log seperti algoritma lain -> perlu render khusus.
                result, process_data = rail_fence.process(
                    text_input, key_input, mode
                )
            elif "Vernam" in menu:
                result, logs = vernam.process(text_input, key_input, mode)
            elif "Blowfish" in menu:
                result, logs = blowfish.process(text_input, key_input, mode)

            with st.container(border=True):
                if "Rail Fence" in menu:
                    st.write(process_data["intro"])
                    st.markdown("---")
                    for i, step in enumerate(process_data["steps"], 1):
                        with st.expander(step["title"], expanded=(i == 1)):
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
                    # Log Blowfish berisi blok HTML (<details>, style, dsb),
                    # jadi wajib unsafe_allow_html=True agar tidak muncul mentah.
                    for log in logs:
                        st.markdown(log, unsafe_allow_html=True)
                else:
                    # Caesar & Vernam: semua log berada di satu panel proses.
                    for log in logs:
                        st.write(log)
        else:
            st.info("Tekan tombol proses untuk melihat visualisasi proses.")
            result = "Hasil akan tampil di sini..."

    st.markdown(f"### {output_label}")
    st.code(result, language="text")

# 2. Super Enkripsi
else:
    st.subheader("Super Enkripsi")

    with st.expander("Tentang Super Enkripsi", expanded=False):
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

    text_input = st.text_area(
        "Input Teks Utama (Plaintext / Ciphertext):",
        placeholder="Masukkan pesan utama yang ingin di-super enkripsi...",
        height=100,
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Kunci utama")
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
                <b>Kunci turunan</b><br>
                • Caesar &nbsp;&nbsp;: <code>{k_caesar}</code><br>
                • Rail Fence : <code>{k_rail}</code> rail<br>
                • Vernam &nbsp;&nbsp;: <code>{k_vernam}</code><br>
                • Blowfish &nbsp;: <code>{k_blowfish}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("Kunci utama belum diisi.")

    with col2:
        st.markdown("#### Urutan algoritma")

        def _reset_algo_order():
            st.session_state["super_algo_order"] = []

        def _default_algo_order():
            st.session_state["super_algo_order"] = [
                "Caesar",
                "Rail Fence",
                "Vernam",
                "Blowfish",
            ]

        # Nilai awal diisi lewat session_state (bukan parameter default=)
        # supaya tidak bentrok dengan reset via tombol di bawah.
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
            # on_click dijalankan SEBELUM widget di-render ulang, jadi aman
            # mengubah session_state (tidak seperti mengubahnya sesudah
            # widget dengan key yang sama sudah dibuat di run yang sama).
            st.button(
                "Kosongkan",
                width="stretch",
                on_click=_reset_algo_order,
            )
        with col_default:
            st.button(
                "Urutan bawaan",
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
            st.warning("Pilih minimal satu algoritma untuk urutan eksekusi.")

    st.markdown("---")

    btn_super = st.button(
        f"Proses Super {mode}",
        type="primary",
        disabled=not (algo_order and master_key),
    )

    st.markdown("---")
    st.subheader("Langkah proses berantai")

    if btn_super and text_input and master_key and algo_order:
        result_super, logs_super = super_enkripsi.process(
            text_input, master_key, algo_order, mode
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
            elif log.startswith("--- **Tahap "):
                if current_stage_title is not None:
                    stage_logs.append((current_stage_title, current_stage_logs))
                current_stage_title = log.removeprefix("--- **").removesuffix("** ---")
                current_stage_logs = []
            elif log.startswith("--- **Proses super enkripsi selesai** ---"):
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

        with st.container(border=True):
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
                                    step["title"],
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
                            # Log Blowfish berisi blok HTML visualisasi.
                            st.markdown(log, unsafe_allow_html=True)

            for log in summary_logs:
                st.markdown(log, unsafe_allow_html=True)
    else:
        if not text_input:
            st.info("Tekan tombol proses untuk melihat visualisasi proses berantai.")
        elif not master_key:
            st.warning("Isi kunci utama terlebih dahulu.")
        elif not algo_order:
            st.warning("Pilih minimal satu algoritma untuk urutan eksekusi.")
        result_super = "Hasil super enkripsi akan tampil di sini..."

    st.markdown(f"### {output_label}")
    st.code(result_super, language="text")