import streamlit as st
import caesar
import rail_fence
import vernam
import blowfish
import super_enkripsi
from session_manager import session_manager

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
            "Caesar Cipher",
            "Rail Fence Cipher",
            "Vernam Cipher (OTP)",
            "Blowfish Cipher",
            "Super Enkripsi"
        ]
    )
    
    st.markdown("---")
    
    # Tampilkan history di sidebar
    session_manager.display_history_widget(show_limit=5)
    
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

# 1. Menu Algoritma Individual (Caesar, Rail Fence, Vernam, Blowfish)
if menu != "Super Enkripsi":
    st.subheader(f"Form {menu}")
    
    # Input Teks langsung (tanpa pilihan history)
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
            # Simpan ke history sebelum proses
            algorithm_name = menu.replace(" (OTP)", "")
            
            if "Caesar" in menu:
                result, logs = caesar.process(text_input, key_input, mode)
            elif "Rail Fence" in menu:
                result, process_data = rail_fence.process(text_input, key_input, mode)
            elif "Vernam" in menu:
                result, logs = vernam.process(text_input, key_input, mode)
            elif "Blowfish" in menu:
                result, logs = blowfish.process(text_input, key_input, mode)

            # Simpan ke history setelah dapat result
            session_manager.add_to_history(
                text=text_input,
                algorithm=algorithm_name,
                mode=mode,
                key=str(key_input),
                result=result
            )

            st.markdown('<div class="process-box">', unsafe_allow_html=True)
            
            if "Rail Fence" in menu:
                # Tampilkan intro
                st.write(process_data["intro"])
                st.markdown("---")
                
                # Tampilkan setiap step dalam expander
                for i, step in enumerate(process_data["steps"], 1):
                    with st.expander(f"▶ {step['title']}", expanded=(i==1)):
                        if step['description']:
                            st.write(f"*{step['description']}*")
                            st.markdown("---")
                        
                        if step['grid'] is not None:
                            st.dataframe(step['grid'], use_container_width=True)
                            st.markdown("---")
                        
                        if step['content']:
                            for content in step['content']:
                                st.write(content)
            else:
                # Untuk algoritma lain (Caesar, Vernam, Blowfish)
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
    
    # Input Teks dengan opsi dari history
    st.write("### Input Teks")
    
    # Pilihan sumber input
    input_source = st.radio(
        "Pilih sumber input:",
        ["Input Manual", "Pilih dari History"],
        horizontal=True,
        key="super_input_source"
    )
    
    if input_source == "Input Manual":
        text_input = st.text_area(
            f"Utama — {input_label}",
            placeholder=input_placeholder,
            height=100
        )
    else:
        # Dropdown dari history
        unique_texts = session_manager.get_unique_texts()
        if unique_texts:
            selected_option = st.selectbox(
                "Pilih dari history:",
                options=range(len(unique_texts)),
                format_func=lambda i: f"[{unique_texts[i]['algorithm']}] {unique_texts[i]['text'][:50]}{'...' if len(unique_texts[i]['text']) > 50 else ''}"
            )
            text_input = unique_texts[selected_option]['text']
            st.text_area("Teks terpilih:", value=text_input, height=100, disabled=True)
        else:
            st.info("Belum ada history. Silakan gunakan Input Manual.")
            text_input = ""
    
    st.markdown("---")
    
    # Konfigurasi Super Enkripsi
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Master Key")
        master_key = st.text_input("Master Key untuk semua algoritma:", value="MYSECRETKEY")
        
        st.write("### Pilih Preset Urutan Algoritma")
        algorithm_presets = super_enkripsi.get_algorithm_presets()
        
        selected_preset = st.selectbox(
            "Pilih kombinasi urutan algoritma:",
            options=list(algorithm_presets.keys()),
            index=0
        )
        
        algorithm_order = algorithm_presets[selected_preset]
    
    with col2:
        st.write("### Preview Kunci Turunan")
        if master_key:
            caesar_key, rail_key, vernam_key, blowfish_key = super_enkripsi.derive_keys_from_master(master_key)
            
            st.info(f"""
            **Kunci yang akan digunakan:**
            - Caesar Cipher: `{caesar_key}`
            - Rail Fence Cipher: `{rail_key}` rails
            - Vernam Cipher: `{vernam_key}`
            - Blowfish Cipher: `{blowfish_key}`
            """)
        
        st.write("### Preview Urutan Terpilih")
        if algorithm_order:
            st.success(f"""
            **Urutan Enkripsi:**
            {' → '.join([f"{i+1}. {algo.replace(' Cipher', '')}" for i, algo in enumerate(algorithm_order)])}
            
            **Urutan Dekripsi:**
            {' → '.join([f"{i+1}. {algo.replace(' Cipher', '')}" for i, algo in enumerate(reversed(algorithm_order))])}
            """)
        
    btn_super = st.button(f"[ PROSES SUPER {mode.upper()} ]", type="primary")
    
    st.markdown("---")
    st.subheader("📊 PROSES DETAIL ALGORITMA BERANTAI (Langkah demi Langkah)")
    
    if btn_super and text_input and master_key:
        # Proses super enkripsi
        result_super, logs_super = super_enkripsi.process(
            text_input, master_key, algorithm_order, mode
        )
        
        # Simpan ke history
        session_manager.add_to_history(
            text=text_input,
            algorithm="Super Enkripsi",
            mode=mode,
            key=f"{master_key} | {' → '.join(algorithm_order)}",
            result=result_super
        )
        
        st.markdown('<div class="process-box">', unsafe_allow_html=True)
        for log in logs_super:
            st.write(log)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        result_super = "Hasil super enkripsi akan tampil di sini..."
        
    st.markdown(f"### {output_label}")
    st.code(result_super, language="text")
