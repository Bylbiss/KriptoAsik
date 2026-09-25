import streamlit as st
from datetime import datetime

class SessionManager:
    """
    Mengelola session history untuk aplikasi kriptografi
    """
    
    def __init__(self):
        # Inisialisasi session state jika belum ada
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'history_counter' not in st.session_state:
            st.session_state.history_counter = 0
    
    def add_to_history(self, text, algorithm, mode, key=None, result=None):
        """
        Menambahkan entry baru ke history
        
        Args:
            text: Input text yang diproses
            algorithm: Nama algoritma yang digunakan
            mode: "Enkripsi" atau "Dekripsi"
            key: Kunci yang digunakan (opsional)
            result: Hasil proses (opsional)
        """
        if not text or text.strip() == "":
            return  # Jangan simpan input kosong
        
        # Increment counter
        st.session_state.history_counter += 1
        
        # Buat entry baru
        entry = {
            'id': st.session_state.history_counter,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': text.strip(),
            'algorithm': algorithm,
            'mode': mode,
            'key': key,
            'result': result,
            'text_length': len(text.strip())
        }
        
        # Tambahkan ke history (di awal list untuk urutan terbaru di atas)
        st.session_state.history.insert(0, entry)
        
        # Batasi history maksimal 50 entry untuk performa
        if len(st.session_state.history) > 50:
            st.session_state.history = st.session_state.history[:50]
    
    def get_history(self):
        """
        Mendapatkan semua history yang tersimpan
        
        Returns:
            List of history entries
        """
        return st.session_state.history
    
    def get_history_by_algorithm(self, algorithm):
        """
        Mendapatkan history berdasarkan algoritma tertentu
        
        Args:
            algorithm: Nama algoritma (misal: "Caesar Cipher")
        
        Returns:
            List of filtered history entries
        """
        return [entry for entry in st.session_state.history if entry['algorithm'] == algorithm]
    
    def get_history_by_mode(self, mode):
        """
        Mendapatkan history berdasarkan mode tertentu
        
        Args:
            mode: "Enkripsi" atau "Dekripsi"
        
        Returns:
            List of filtered history entries
        """
        return [entry for entry in st.session_state.history if entry['mode'] == mode]
    
    def get_unique_texts(self):
        """
        Mendapatkan list teks unik dari history (untuk dropdown selection)
        
        Returns:
            List of unique texts from history
        """
        seen = set()
        unique_texts = []
        
        for entry in st.session_state.history:
            text = entry['text']
            if text not in seen and len(text) <= 200:  # Batasi panjang untuk dropdown
                seen.add(text)
                unique_texts.append({
                    'text': text,
                    'algorithm': entry['algorithm'],
                    'timestamp': entry['timestamp'],
                    'mode': entry['mode']
                })
        
        return unique_texts
    
    def clear_history(self):
        """
        Menghapus semua history
        """
        st.session_state.history = []
        st.session_state.history_counter = 0
    
    def get_statistics(self):
        """
        Mendapatkan statistik penggunaan
        
        Returns:
            Dictionary dengan statistik
        """
        history = self.get_history()
        
        if not history:
            return {
                'total_entries': 0,
                'algorithms_used': {},
                'modes_used': {},
                'most_recent': None
            }
        
        # Hitung statistik
        algorithms = {}
        modes = {}
        
        for entry in history:
            # Count algorithms
            algo = entry['algorithm']
            algorithms[algo] = algorithms.get(algo, 0) + 1
            
            # Count modes
            mode = entry['mode']
            modes[mode] = modes.get(mode, 0) + 1
        
        return {
            'total_entries': len(history),
            'algorithms_used': algorithms,
            'modes_used': modes,
            'most_recent': history[0] if history else None
        }
    
    def display_history_widget(self, show_limit=10):
        """
        Menampilkan widget history dalam sidebar atau container
        
        Args:
            show_limit: Jumlah maksimal entry yang ditampilkan
        """
        history = self.get_history()
        
        if not history:
            st.info("📝 Belum ada history")
            return
        
        st.subheader("📚 History Session")
        
        # Statistik singkat
        stats = self.get_statistics()
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Entry", stats['total_entries'])
        
        with col2:
            if stats['most_recent']:
                st.metric("Terakhir", stats['most_recent']['algorithm'])
        
        # Tombol clear history
        if st.button("🗑️ Clear History", type="secondary"):
            self.clear_history()
            st.rerun()
        
        st.markdown("---")
        
        # Tampilkan history entries
        for i, entry in enumerate(history[:show_limit]):
            with st.expander(f"#{entry['id']} - {entry['algorithm']} ({entry['mode']})", expanded=False):
                st.write(f"**⏰ Waktu:** {entry['timestamp']}")
                st.write(f"**📝 Input:** `{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}`")
                if entry['key']:
                    st.write(f"**🔑 Kunci:** `{entry['key']}`")
                if entry['result']:
                    st.write(f"**📤 Hasil:** `{entry['result'][:100]}{'...' if len(entry['result']) > 100 else ''}`")
        
        # Jika ada lebih banyak entry
        if len(history) > show_limit:
            st.info(f"... dan {len(history) - show_limit} entry lainnya")

# Instance global untuk kemudahan akses
session_manager = SessionManager()