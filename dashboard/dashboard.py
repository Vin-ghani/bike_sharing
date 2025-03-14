import matplotlib.lines as mlines
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
data = pd.read_csv('dashboard/main_data.csv')

data['dteday'] = pd.to_datetime(data['dteday'])

def filter_data(data, selected_weathersit, selected_date):
    start_date, end_date = selected_date if isinstance(selected_date, tuple) else (selected_date, selected_date)
    return data[(data['weathersit'].isin(selected_weathersit)) &
                (data['dteday'].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))]

# Judul Dashboard
st.title('Bike Sharing Data Dashboard')

# Sidebar Filter
st.sidebar.header("Filter Data")
selected_weathersit = st.sidebar.multiselect("Pilih Kondisi Cuaca:", data['weathersit'].unique(), default=data['weathersit'].unique())
selected_date = st.sidebar.date_input("Pilih Rentang Tanggal", [data['dteday'].min(), data['dteday'].max()])

filtered_data = filter_data(data, selected_weathersit, selected_date)

# Perbandingan Rata-rata Penyewaan Casual vs Registered
st.subheader('Rata-rata Penyewaan Casual vs Registered')
agg_data = pd.DataFrame({
    'Kategori': ['Casual', 'Registered'],
    'Rata-rata Penyewaan': [filtered_data['casual'].mean(), filtered_data['registered'].mean()]
})

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=agg_data, x='Kategori', y='Rata-rata Penyewaan', palette='coolwarm', ax=ax1)
ax1.set_title('Rata-rata Penyewaan: Casual vs Registered')
ax1.set_xlabel('Kategori Pengguna')
ax1.set_ylabel('Rata-rata Penyewaan')
ax1.set_ylim(0, None)
st.pyplot(fig1)

# Dampak Hari Kerja vs Hari Libur
st.subheader('Dampak Hari Kerja vs Hari Libur terhadap Penyewaan Sepeda')
filtered_data['workingday_label'] = filtered_data['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})
agg_data = filtered_data.groupby('workingday_label')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=agg_data, x='workingday_label', y='cnt', palette='coolwarm', ax=ax2)
ax2.set_title('Perbandingan Rata-rata Penyewaan: Hari Kerja vs Hari Libur')
ax2.set_xlabel('')
ax2.set_ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(fig2)

# Tren Penyewaan per Bulan
st.subheader('Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur')

# Cek apakah ada data setelah difilter
if not filtered_data.empty:
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(
        data=filtered_data, 
        x='mnth', 
        y='cnt', 
        hue='workingday', 
        marker='o', 
        palette={0: 'red', 1: 'blue'}, 
        style='workingday',
        dashes={0: (2, 2), 1: ''}, 
        ci=None,  
        ax=ax3
    )

    ax3.set_title("Tren Penyewaan per Bulan: Hari Kerja vs Hari Libur")
    ax3.set_xlabel("Bulan")
    ax3.set_ylabel("Jumlah Penyewaan")
    ax3.set_xticks(range(12))
    ax3.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    legend_labels = {0: "Hari Libur", 1: "Hari Kerja"}
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles, [legend_labels[int(label)] for label in labels], title="Jenis Hari")
    st.pyplot(fig3)
else:
    st.warning("Tidak ada data yang tersedia untuk rentang tanggal dan kondisi cuaca yang dipilih.")


# Manual Grouping (Pengelompokan Penyewaan)
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Kelompok Jumlah Penyewaan')

# Buat kategori pengelompokan berdasarkan jumlah penyewaan
bins = [0, filtered_data['cnt'].quantile(0.33), filtered_data['cnt'].quantile(0.66), filtered_data['cnt'].max()]
labels = ['Rendah', 'Sedang', 'Tinggi']
filtered_data['pengelompokan'] = pd.cut(filtered_data['cnt'], bins=bins, labels=labels, include_lowest=True)

# Visualisasi data setelah diproses
fig4, ax4 = plt.subplots(figsize=(8, 6))
filtered_data['pengelompokan'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('coolwarm', 3), ax=ax4)
ax4.set_ylabel('')  
ax4.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kelompok')
st.pyplot(fig4)


# Penjelasan
with st.expander("Penjelasan Grafik Distribusi Penyewaan Berdasarkan Kelompok Jumlah Penyewaan"):
    st.write("""
    Grafik ini menunjukkan distribusi penyewaan sepeda berdasarkan **kelompok jumlah penyewaan** yang telah dibagi menjadi tiga kategori:
    - **Rendah**: Penyewaan dengan jumlah rendah, menunjukkan periode dengan sedikit permintaan.
    - **Sedang**: Penyewaan dengan jumlah moderat, mencerminkan periode dengan permintaan normal.
    - **Tinggi**: Penyewaan dengan jumlah tinggi, mungkin terjadi pada waktu-waktu tertentu seperti liburan atau cuaca cerah.
    """)



