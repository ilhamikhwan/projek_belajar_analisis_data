import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menyiapkan data day_df
df = pd.read_csv("day.csv")
df.head()

# Menghapus kolom yang tidak diperlukan
drop_column = ['instant']

for i in df.columns:
  if i in drop_column:
    df.drop(labels=i, axis=1, inplace=True)


# Mengubah angka menjadi keterangan
df['mnth'] = df['mnth'].map({
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
})
df['season'] = df['season'].map({
    1: 'Dingin', 2: 'Gugur', 3: 'Panas', 4: 'Semi'
})
df['weekday'] = df['weekday'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})



def sewa_harian_df(df):
    harian_sewa_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return harian_sewa_df


def harian_casual_df(df):
    casual_sewa_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_sewa_df

def registered_df(df):
    registered_sewa_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_sewa_df
    

def sewa_musim_df(df):
    musim_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return musim_df

def sewa_bulanan_df(df):
    sewa_bulan_df = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
    urutan_bulan = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    sewa_bulan_df = sewa_bulan_df.reindex(urutan_bulan, fill_value=0)
    return sewa_bulan_df


def sewa_mingguan_df(df):
    sewa_perminggu_df = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    })
    urutan_Minggu= [
        'Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'
        ]
    sewa_perminggu_df = sewa_perminggu_df.reindex(urutan_Minggu, fill_value=0)
    return sewa_perminggu_df


def sewa_workingday_df(df):
    workingday_df = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_df

def sewa_holiday_df(df):
    holiday_df = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_df

def sewa_weather_df(df):
    weather_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return weather_df



date_min = pd.to_datetime(df['dteday']).dt.date.min()
date_max = pd.to_datetime(df['dteday']).dt.date.max()
 
with st.sidebar:
    st.header('Muhammad Ilham Ikhwanul Akram')
    st.image('https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT7Y40iFLF0hwJtyafq_b1Gs4AOHDxcxDgLd5RBMqa4qdNRxpow')
    
    
    date_start, date_end = st.date_input(
        label='Time',
        min_value= date_min,
        max_value= date_max,
        value=[date_min, date_max]
    )

main_df = df[(df['dteday'] >= str(date_start)) & 
                (df['dteday'] <= str(date_end))]


sewa_harian = sewa_harian_df(main_df)
harian_casual = harian_casual_df(main_df)
registered_harian= registered_df(main_df)
sewa_musim = sewa_musim_df(main_df)
sewa_bulan = sewa_bulanan_df(main_df)
sewa_mingguan = sewa_mingguan_df(main_df)
sewa_workingday = sewa_workingday_df(main_df)
sewa_weather =sewa_weather_df(main_df)



st.header('Bike Sharing Dashboard')


st.subheader('Jumlah Seluruh Sepeda Yang Disewa')
col1, col2, col3 = st.columns(3)

with col1:
    harian_casual = harian_casual['casual'].sum()
    st.metric('Penyewa Biasa', value= harian_casual)

with col2:
    harian_registered = registered_harian['registered'].sum()
    st.metric('Penyewa Teregistrasi', value= harian_registered)
 
with col3:
    harian_total = sewa_harian['cnt'].sum()
    st.metric('Penyewa Total', value= harian_total)



st.subheader('Jumlah Sewa Berdasarkan Mingguan')

fig, ax = plt.subplots(figsize=(15, 10))

colors=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

sns.barplot(
    x=sewa_mingguan.index,
    y=sewa_mingguan['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(sewa_mingguan['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Jumlah Sewa Berdasarkan Bulan')

fig, axes = plt.subplots(figsize=(15,15))

colors=["tab:blue", "tab:red", "tab:green"]

sns.barplot(
  x='mnth',
  y='cnt',
  data=sewa_bulan,
  palette=colors,
  ax=axes)

for index, row in enumerate(sewa_bulan['cnt']):
    axes.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10)

axes.set_title('Jumlah Sewa Bulanan', fontsize=25)
axes.set_ylabel(None)
axes.tick_params(axis='x', labelsize=13)
axes.tick_params(axis='y', labelsize=13)

plt.tight_layout()
st.pyplot(fig)


st.subheader('Jumlah Sewa Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(15, 15))

sns.barplot(
    x='season',
    y='registered',
    data=sewa_musim,
    label='Registered',
    color='tab:red',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=sewa_musim,
    label='Casual',
    color='tab:blue',
    ax=ax
)

for index, row in sewa_musim.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

st.caption('Copyright (c) Muhammad Ilham Ikhwanul Akram 2024')
