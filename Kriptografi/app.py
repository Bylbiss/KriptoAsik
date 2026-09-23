import streamlit as st
import caesar
import rail_fence
import vernam
import blowfish
import super_enkripsi

# Konfig Halaman Streamlit
st.set_page_config(
    page_title="APLIKASI KRIPTOGRAFI",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        font-family: 'Courier New', Courier, monospace;
        background-color: #161b22;
        padding: 10px 20px;
        border-radius: 5px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .process-box {
        background-color: #161b22;
        border: 1px dashed #30363d;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama
st.markdown("""
<div class="main-header">
    <h3 style="margin:0; padding:0;">🔐 APLIKASI KRIPTOGRAFI</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📌 MENU")
    
    # Pilih Menu
    menu = st.radio(
        "Pilih Algoritma:",
        [
            "> **Caesar Cipher**",
            "> **Rail Fence Cipher**",
            "> **Vernam Cipher (OTP)**",
            "> **Blowfish Cipher**",
            "> **Super Enkripsi**"
        ]
    )
    
    st.markdown("---")
    st.title("👥 NAMA ANGGOTA")
    st.write("- **Bylbiss El Haqqie** 123240003")
    st.write("- **Muhammad Restu Firmansyah** 123240050")
    st.write("- **Alifah Chairul Munawar** 123240234")

# Halaman Utama

# Mode Enkripsi/Dekripsi
mode = st.radio("Mode Operasi:", ["Enkripsi", "Dekripsi"], horizontal=True)

st.markdown("---")

# Penentuan Label Dinamis berdasarkan Mode
input_label = "Input Plaintext (Teks Asli):" if mode == "Enkripsi" else "Input Ciphertext (Teks Terenkripsi):"
input_placeholder = "Masukkan pesan teks asli di sini..." if mode == "Enkripsi" else "Masukkan pesan cipher di sini..."
output_label = "Hasil Akhir (Ciphertext):" if mode == "Enkripsi" else "Hasil Akhir (Plaintext):"

# 1. Menu 1 - 4
if menu != "> **Super Enkripsi**":
    st.subheader(f"Form {menu.replace('> ', '').replace('**', '')}")
    
    # Input Teks
    text_input = st.text_area(
        input_label,
        placeholder=input_placeholder,
        height=100
    )
    
    # Input Kunci
    if "Caesar" in menu or "Rail" in menu:
        key_input = st.number_input("Kunci (Key Integer):", min_value=1, value=3, step=1)
    else:
        key_input = st.text_input("Kunci (Key Text/Hex):", placeholder="Masukkan kunci...")
        
    # Tombol Eksekusi
    btn_process = st.button(f"[ PROSES {mode.upper()} ]", type="primary")
    
    st.markdown("---")
    st.subheader("📊 PROSES DETAIL ALGORITMA")
    
    # Container Log Visualisasi Proses
    with st.container():
        if btn_process and text_input:
            if "Caesar" in menu:
                result, logs = caesar.process(text_input, key_input, mode)
            elif "Rail Fence" in menu:
                result, logs = rail_fence.process(text_input, key_input, mode)
            elif "Vernam" in menu:
                result, logs = vernam.process(text_input, key_input, mode)
            elif "Blowfish" in menu:
                result, logs = blowfish.process(text_input, key_input, mode)

            st.markdown('<div class="process-box">', unsafe_allow_html=True)
            for log in logs:
                st.write(log)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Tekan tombol proses untuk melihat visualisasi proses.")
            result = "Hasil akan tampil di sini..."
            
    st.markdown(f"### {output_label}")
    st.code(result, language="text")

# 2. Super Enkripsi
else:
    st.subheader("🔗 Form Super Enkripsi")
    
    text_input = st.text_area(
        "Input Teks Utama (Plaintext / Ciphertext):",
        placeholder="Masukkan pesan utama yang ingin di-super enkripsi...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        k_caesar = st.number_input("Kunci (1) Caesar Cipher:", min_value=1, value=7)
        k_vernam = st.text_input("Kunci (3) Vernam Cipher (OTP):", value="SECRET")
    with col2:
        k_rail = st.number_input("Kunci (2) Rail Fence Cipher:", min_value=2, value=3)
        k_blowfish = st.text_input("Kunci (4) Blowfish Cipher:", value="12345678")
        
    btn_super = st.button(f"[ PROSES SUPER {mode.upper()} ]", type="primary")
    
    st.markdown("---")
    st.subheader("📊 PROSES DETAIL ALGORITMA BERANTAI (Langkah demi Langkah)")
    
    if btn_super and text_input:
        result_super, logs_super = super_enkripsi.process(
            text_input, k_caesar, k_rail, k_vernam, k_blowfish, mode
        )
        st.markdown('<div class="process-box">', unsafe_allow_html=True)
        for log in logs_super:
            st.write(log)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        result_super = "Hasil super enkripsi akan tampil di sini..."
        
    st.markdown(f"### {output_label}")
    st.code(result_super, language="text")