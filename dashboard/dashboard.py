import matplotlib.lines as mlines
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
data = pd.read_csv('main_data.csv')

# Judul Dashboard
st.title('Bike Sharing Data Dashboard')
 
# Perbandingan Penyewaan Casual vs Registered
st.subheader('Perbandingan Penyewaan Casual vs Registered')
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.boxplot(data=data[['casual', 'registered']], ax=ax1, palette='coolwarm')
ax1.set_title('Perbandingan Penyewaan: Casual vs Registered')
ax1.set_xlabel('Kategori Pengguna')
ax1.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig1)

# Penjelasan
with st.expander("Penjelasan Grafik Perbandingan Penyewaan Casual vs Registered"):
    st.write("""
    Grafik ini menunjukkan perbandingan jumlah penyewaan sepeda antara pengguna **casual** dan **registered**.
    - **Pengguna Casual** menunjukkan lebih banyak variasi dalam jumlah penyewaan, yang cenderung lebih rendah.
    - **Pengguna Registered** menunjukkan pola penyewaan yang lebih konsisten dan lebih tinggi.
    Penjelasan ini dapat memberikan wawasan tentang bagaimana perilaku penggunaan sepeda berbeda antara pengguna yang terdaftar dan tidak.
    """)

# Dampak Hari Kerja vs Hari Libur
st.subheader('Dampak Hari Kerja vs Hari Libur terhadap Penyewaan Sepeda')
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.boxplot(data=data, x='workingday', y='cnt', palette='coolwarm', ax=ax2)
ax2.set_title('Perbandingan Penyewaan: Hari Kerja vs Hari Libur')
ax2.set_xlabel('Hari Kerja  vs Hari Libur ')
ax2.set_ylabel('Jumlah Penyewaan')
ax2.set_xticklabels(['Hari Libur', 'Hari Kerja'])
st.pyplot(fig2)

with st.expander("Penjelasan Grafik Hari Kerja vs Hari Libur"):
    st.write("""
    Grafik ini membandingkan jumlah penyewaan sepeda antara **hari kerja** (1) dan **hari libur** (0).
    - **Hari Kerja** menunjukkan jumlah penyewaan yang lebih tinggi karena banyak orang menggunakan sepeda untuk transportasi sehari-hari.
    - **Hari Libur** menunjukkan penurunan jumlah penyewaan, mungkin karena orang lebih memilih kendaraan pribadi atau tidak menggunakan sepeda.
    """)
    
# Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur
st.subheader('Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur')
fig3, ax3 = plt.subplots(figsize=(12, 6))

# Plot untuk Hari Kerja
sns.lineplot(data=data[data['workingday'] == 1], x='mnth', y='cnt', label='Hari Kerja', color='red', marker='o', ax=ax3)
# Plot untuk Hari Libur
sns.lineplot(data=data[data['workingday'] == 0], x='mnth', y='cnt', label='Hari Libur', color='blue', marker='o', ax=ax3)

ax3.set_title("Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur")
ax3.set_xlabel("Bulan")
ax3.set_ylabel("Jumlah Penyewaan")
ax3.set_xticks(range(12))
ax3.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

# Menyesuaikan legend dengan warna dan marker
legend_labels = ['Hari Kerja', 'Hari Libur']
legend_handles = [
    mlines.Line2D([], [], color='red', marker='o', markersize=8, label='Hari Kerja'),
    mlines.Line2D([], [], color='blue', marker='o', markersize=8, label='Hari Libur')
]
ax3.legend(handles=legend_handles, title="Kategori Hari", loc="upper left")
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


