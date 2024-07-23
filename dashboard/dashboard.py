
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io

# Menampilkan judul aplikasi di Streamlit
st.title('Proyek Analisis Penyewaan Sepeda')

# Menampilkan subjudul untuk pertanyaan analisis
st.subheader('Pertanyaan 1: Bagaimana pengaruh hari libur dan hari kerja terhadap jumlah penyewaan sepeda?')
st.subheader('Pertanyaan 2: Apakah terdapat pola musiman dalam jumlah penyewaan sepeda?')

# Memuat dataset dari file CSV
data = pd.read_csv('day.csv')

# Mengonversi kolom 'dteday' menjadi tipe datetime dan menambahkan kolom bulan
data['dteday'] = pd.to_datetime(data['dteday'])
data['month'] = data['dteday'].dt.month

# Menampilkan informasi dataset
st.write("Informasi Dataset:")

# Menggunakan io.StringIO untuk menangkap output dari data.info()
buffer = io.StringIO()
data.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# Menampilkan statistik deskriptif dari dataset
st.write("\nStatistik Deskriptif:")
st.write(data.describe())

# Menampilkan beberapa baris awal dari dataset
st.write("\nBeberapa Baris Awal:")
st.write(data.head())

# Menampilkan subjudul untuk analisis pengaruh hari libur
st.subheader('Pengaruh Hari Libur terhadap Jumlah Penyewaan Sepeda')

# Mengelompokkan data berdasarkan bulan, hari libur, dan tipe pengguna
monthly_rentals = data.groupby(['month', 'holiday']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

# Menentukan jumlah penyewaan tertinggi dan terendah berdasarkan hari libur dan non-libur
max_rentals_holiday = monthly_rentals[monthly_rentals['holiday'] == 1]['cnt'].max()
min_rentals_holiday = monthly_rentals[monthly_rentals['holiday'] == 1]['cnt'].min()
max_rentals_non_holiday = monthly_rentals[monthly_rentals['holiday'] == 0]['cnt'].max()
min_rentals_non_holiday = monthly_rentals[monthly_rentals['holiday'] == 0]['cnt'].min()

# Menampilkan informasi jumlah tertinggi dan terendah
st.write(f"Jumlah penyewaan sepeda tertinggi pada hari libur: {max_rentals_holiday}")
st.write(f"Jumlah penyewaan sepeda terendah pada hari libur: {min_rentals_holiday}")
st.write(f"Jumlah penyewaan sepeda tertinggi pada hari non-libur: {max_rentals_non_holiday}")
st.write(f"Jumlah penyewaan sepeda terendah pada hari non-libur: {min_rentals_non_holiday}")

# Plot total penyewaan per bulan untuk casual dan registered berdasarkan hari libur
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(data=monthly_rentals, x='month', y='cnt', hue='holiday', palette='coolwarm', alpha=0.7, dodge=True, errorbar=None, ax=ax)

# Menambahkan judul dan label
ax.set_title('Jumlah Penyewaan Sepeda Tiap Bulan Berdasarkan Hari Libur')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_xticks(range(12))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ['Non-Libur', 'Libur'], title='Hari Libur')
st.pyplot(fig)

# Menampilkan subjudul untuk analisis pengaruh musim
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Musim Sepanjang Tahun')

# Mengelompokkan data berdasarkan tahun dan musim
yearly_rentals_season = data.groupby(['yr', 'season']).agg({
    'cnt': 'sum'
}).reset_index()

# Menentukan jumlah penyewaan tertinggi dan terendah berdasarkan musim
max_rentals_season = yearly_rentals_season['cnt'].max()
min_rentals_season = yearly_rentals_season['cnt'].min()

# Menemukan musim dengan jumlah penyewaan tertinggi dan terendah
season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
max_season = yearly_rentals_season.loc[yearly_rentals_season['cnt'].idxmax()]['season']
min_season = yearly_rentals_season.loc[yearly_rentals_season['cnt'].idxmin()]['season']

max_season_name = season_names[max_season]
min_season_name = season_names[min_season]

# Menampilkan informasi jumlah tertinggi dan terendah
st.write(f"Jumlah penyewaan sepeda tertinggi berdasarkan musim: {max_rentals_season} (Musim: {max_season_name})")
st.write(f"Jumlah penyewaan sepeda terendah berdasarkan musim: {min_rentals_season} (Musim: {min_season_name})")

# Plot jumlah penyewaan sepeda berdasarkan musim sepanjang tahun
fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(data=yearly_rentals_season, x='season', y='cnt', hue='season', palette='coolwarm', estimator='sum')
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim Sepanjang Tahun')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ['Spring', 'Summer', 'Fall', 'Winter'], title='Musim')
st.pyplot(fig)

# Menampilkan kesimpulan
st.subheader('Conclusion')
st.write("Conclusion pertanyaan 1: Berdasarkan hasil analisis, jumlah penyewaan sepeda lebih tinggi pada hari non-libur dibandingkan dengan hari libur. Ini menunjukkan bahwa lebih banyak orang menyewa sepeda pada hari-hari kerja atau hari-hari biasa, sementara pada hari libur, jumlah penyewa cenderung menurun.")
st.write("Conclusion pertanyaan 2: Dari hasil analisis musiman, terlihat bahwa jumlah penyewaan sepeda paling tinggi selama musim 'Fall'. Musim ini menunjukkan aktivitas penyewaan sepeda yang lebih banyak dibandingkan dengan musim lainnya, seperti 'Spring', 'Summer', dan 'Winter'.")
