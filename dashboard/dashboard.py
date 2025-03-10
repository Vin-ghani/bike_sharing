import matplotlib.lines as mlines
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
data = pd.read_csv('main_data.csv')

# Judul Dashboard
st.title('Bike Sharing Data Dashboard')

# Sidebar  
# Sidebar untuk Filtering
st.sidebar.header("Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim:", data['season'].unique(), default=data['season'].unique())
selected_weathersit = st.sidebar.multiselect("Pilih Kondisi Cuaca:", data['weathersit'].unique(), default=data['weathersit'].unique())
selected_date = st.sidebar.date_input("Pilih Rentang Tanggal", [pd.to_datetime(data['dteday']).min(), pd.to_datetime(data['dteday']).max()])

# Filter Data
# Konversi dteday ke datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Jika user memilih rentang tanggal
if isinstance(selected_date, tuple):
    start_date, end_date = selected_date
else:
    start_date, end_date = selected_date, selected_date

filtered_data = data[
    (data['season'].isin(selected_season)) & 
    (data['weathersit'].isin(selected_weathersit)) & 
    (data['dteday'].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
] 
# Perbandingan Penyewaan Casual vs Registered
st.subheader('Perbandingan Penyewaan Casual vs Registered')

# Membuat DataFrame baru untuk visualisasi
agg_data = pd.DataFrame({
    'Kategori': ['Casual', 'Registered'],
    'Jumlah Penyewaan': [filtered_data['casual'].sum(), filtered_data['registered'].sum()]
})

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=agg_data, x='Kategori', y='Jumlah Penyewaan', palette='coolwarm', ax=ax1)
ax1.set_title('Perbandingan Penyewaan: Casual vs Registered')
ax1.set_xlabel('Kategori Pengguna')
ax1.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig1)



# Dampak Hari Kerja vs Hari Libur
st.subheader('Dampak Hari Kerja vs Hari Libur terhadap Penyewaan Sepeda')
# Konversi nilai 'workingday' menjadi label yang lebih jelas
data['workingday_label'] = data['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

# Agregasi jumlah penyewaan berdasarkan hari kerja vs hari libur
agg_data = data.groupby('workingday_label')['cnt'].mean().reset_index()

# Bar chart
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=agg_data, x='workingday_label', y='cnt', palette= 'coolwarm', ax=ax2)
ax2.set_title('Perbandingan Rata-rata Penyewaan: Hari Kerja vs Hari Libur', fontsize=14)
ax2.set_xlabel('')
ax2.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
st.pyplot(fig2)

with st.expander("Penjelasan Grafik Hari Kerja vs Hari Libur"):
    st.write("""
    Grafik ini membandingkan jumlah penyewaan sepeda antara **hari kerja**  dan **hari libur** .
    - **Hari Kerja** menunjukkan jumlah penyewaan yang lebih tinggi karena banyak orang menggunakan sepeda untuk transportasi sehari-hari.
    - **Hari Libur** menunjukkan penurunan jumlah penyewaan, mungkin karena orang lebih memilih kendaraan pribadi atau tidak menggunakan sepeda.
    """)
    
# Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur
st.subheader('Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur')
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=data, x='mnth', y='cnt', hue='workingday', marker='o', palette=['blue', 'red'], ax=ax3)
ax3.set_title("Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur")
ax3.set_xlabel("Bulan")
ax3.set_ylabel("Jumlah Penyewaan")
ax3.set_xticks(range(12))
ax3.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.pyplot(fig3)

# Penjelasan
with st.expander("Penjelasan Grafik Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur"):
    st.write("""
    Grafik ini menunjukkan tren jumlah penyewaan sepeda **per bulan** berdasarkan **hari kerja** dan **hari libur**.
    - **Hari Kerja** memiliki tren yang lebih stabil dan cenderung lebih tinggi.
    - **Hari Libur** menunjukkan fluktuasi yang lebih besar, dengan penyewaan yang cenderung lebih rendah.
    Grafik ini memberikan gambaran tentang bagaimana pola penyewaan sepeda dipengaruhi oleh status hari kerja atau libur.
    """)

# Manual Grouping (Pengelompokan Penyewaan)
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Kelompok Jumlah Penyewaan')
fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.countplot(data=data, x='pengelompokan', palette='coolwarm', ax=ax4)
ax4.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kelompok Jumlah Penyewaan')
ax4.set_xlabel('Kelompok Penyewaan')
ax4.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig4)

# Penjelasan
with st.expander("Penjelasan Grafik Distribusi Penyewaan Berdasarkan Kelompok Jumlah Penyewaan"):
    st.write("""
    Grafik ini menunjukkan distribusi penyewaan sepeda berdasarkan **kelompok jumlah penyewaan** yang telah dibagi menjadi tiga kategori:
    - **Rendah**: Penyewaan dengan jumlah rendah, menunjukkan periode dengan sedikit permintaan.
    - **Sedang**: Penyewaan dengan jumlah moderat, mencerminkan periode dengan permintaan normal.
    - **Tinggi**: Penyewaan dengan jumlah tinggi, mungkin terjadi pada waktu-waktu tertentu seperti liburan atau cuaca cerah.
    """)


