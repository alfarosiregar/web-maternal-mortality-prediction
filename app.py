import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Prediksi Angka Kematian Ibu Berdasarkan Evaluasi Model")

# Load data angka kematian
try:
    df_data = pd.read_csv('angka_kematian.csv')
except FileNotFoundError:
    st.error("File 'angka_kematian.csv' tidak ditemukan.")
    st.stop()

# Load MSE results
try:
    df_mse = pd.read_csv('mse_results.csv')
except FileNotFoundError:
    st.error("File 'mse_results.csv' tidak ditemukan.")
    st.stop()

# Filter berdasarkan Tahun
st.subheader("1. Pilih Tahun Data")
available_years = sorted(df_data['Tahun'].unique())
selected_year = st.selectbox("Pilih Tahun", available_years)

# Filter data berdasarkan tahun yang dipilih
filtered_data = df_data[df_data['Tahun'] == selected_year]

# Pilih Kabupaten berdasarkan data yang difilter
st.subheader("2. Pilih Kabupaten")
selected_kabupaten = st.selectbox("Pilih Kabupaten", filtered_data['Kabupaten'])

# Menampilkan data yang dipilih
selected_row = filtered_data[filtered_data['Kabupaten'] == selected_kabupaten].iloc[0]
st.write("**Data yang dipilih:**")
st.write(f"Tahun: {selected_year}")
st.write(f"Pendarahan: {selected_row['Pendarahan']}, Hipertensi: {selected_row['Hipertensi']}, Infeksi: {selected_row['Infeksi']}")

# Pilihan learning rate dan epoch
st.subheader("3. Pilih Parameter Model")
learning_rates = sorted(df_mse['lr'].unique())
epochs_list = sorted(df_mse['epochs'].unique())

selected_lr = st.selectbox("Learning Rate", learning_rates)
selected_epochs = st.selectbox("Epochs", epochs_list)

# Tombol untuk menampilkan hasil
if st.button("Prediksi Angka Kematian"):
    result = df_mse[(df_mse['lr'] == selected_lr) & (df_mse['epochs'] == selected_epochs)]
    
    if not result.empty:
        mse_value = result.iloc[0]['mse']
        
        st.markdown("### **Hasil Evaluasi Model Prediksi Angka Kematian Ibu**")
        st.markdown(f"""
        🔍 **Detail Lokasi dan Waktu**
        - 📍 **Kabupaten**: `{selected_kabupaten}`
        - 📅 **Tahun**: `{selected_year}`

        ⚙️ **Parameter Model**
        - 🔁 **Learning Rate**: `{selected_lr}`
        - 🔂 **Epochs**: `{selected_epochs}`

        📊 **Hasil Evaluasi**
        - 📉 **Mean Squared Error (MSE)**: `{mse_value:.4f}`

        ---
        🧠 MSE (Mean Squared Error) menunjukkan seberapa besar kesalahan rata-rata model dalam memprediksi total kematian. 
        Semakin kecil nilainya, semakin baik performa model. 🎯
        """)
    else:
        st.warning("Kombinasi parameter tidak ditemukan.")
