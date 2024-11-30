import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

# Fungsi untuk halaman deskripsi dataset
def dataset_description():
    st.title("📊 Deskripsi Dataset")
    st.markdown(
        """
        Dataset ini berisi statistik video YouTube yang sedang trending di Indonesia. Data diambil dari 
        [Kaggle](https://www.kaggle.com/datasets/syahrulhamdani/indonesias-trending-youtube-video-statistics) 
        dan mencakup informasi seperti:
        
        - **Trending Date**: Tanggal ketika video menjadi trending.
        - **Title**: Judul video.
        - **Channel Name**: Nama channel yang mengunggah video.
        - **Category**: Kategori konten video (misalnya Music, Entertainment, dll.).
        - **Views**: Jumlah total penayangan.
        - **Likes**: Jumlah total likes.
        - **Dislikes**: Jumlah total dislikes.
        - **Comments**: Jumlah total komentar.
        - **Tags**: Tag yang digunakan dalam video.
        - **Description**: Deskripsi video.

        Dataset ini cocok untuk menganalisis tren, popularitas, dan keterlibatan video di platform YouTube.
        DIbuat oleh Muhammad DImas M
        """
    )

# Fungsi untuk membuka dataset dari pickle dan menjelaskan kolom
def open_dataset():
    st.title("📂 Buka Dataset dan Penjelasan Kolom")
    
    # Membaca dataset dari file pickle
    try:
        with open("data_input/used_data.pickle", "rb") as file:  # Sesuaikan path file Anda
            df = pickle.load(file)
    except Exception as e:
        st.error(f"Error saat memuat file: {e}")
        return

    # Menampilkan dataset
    st.subheader("📑 Dataset")
    st.dataframe(df.head(10))  # Menampilkan 10 baris pertama
    
    # Penjelasan kolom
    st.subheader("📝 Penjelasan")
    st.markdown(
        """
        - **title**: Judul video.
        - **channel_name**: Nama channel yang mengunggah video.
        - **views**: Jumlah total penayangan video.
        - **likes**: Jumlah total likes pada video.
        - **dislikes**: Jumlah total dislikes pada video.
        - **comments**: Jumlah total komentar pada video.
        - **category**: Kategori konten video (misalnya Music, Entertainment, dll.).
        - **trending_date**: Tanggal saat video mulai trending.
        """
    )

# Fungsi untuk halaman prediksi
def prediction_page():
    st.title("🎥 Prediksi Trending YouTube")
    px.defaults.template = 'plotly_dark'
    px.defaults.color_continuous_scale = 'reds'

    # Membuka file pickle
    with open("data_input/used_data.pickle", 'rb') as f:
        data = pickle.load(f)

    # Input tanggal
    min_date = data['trending_date'].min()
    max_date = data['trending_date'].max()
    dates = st.sidebar.date_input(label='Rentang Waktu',
                                   min_value=min_date,
                                   max_value=max_date,
                                   value=[min_date, max_date])

    # Validasi input tanggal
    if len(dates) == 1:
        st.sidebar.error("Harap pilih dua tanggal untuk rentang waktu!")
        st.stop()
    elif len(dates) == 2:
        start_date, end_date = dates

    # Input kategori
    categories = ["All Categories"] + list(data['category'].value_counts().keys().sort_values())
    category = st.sidebar.selectbox(label='Kategori', options=categories)

    # Filter
    outputs = data[(data['trending_date'] >= start_date) & 
                   (data['trending_date'] <= end_date)]
    if category != "All Categories":
        outputs = outputs[outputs['category'] == category]

    # Visualisasi dengan bar chart
    st.header(':video_camera: Channel')
    bar_data = outputs['channel_name'].value_counts().nlargest(10).sort_values()
    fig = px.bar(bar_data, color=bar_data, orientation='h', title=f'Channel Terpopuler dari kategori {category}')
    st.plotly_chart(fig)

    # Visualisasi dengan scatter plot
    st.header(':bulb: Engagement')
    col1, col2 = st.columns(2)
    metrics_choice = ['like', 'dislike', 'comment']
    choice_1 = col1.selectbox('Horizontal', options=metrics_choice)
    choice_2 = col2.selectbox('Vertical', options=metrics_choice)
    fig = px.scatter(outputs, 
                     x=choice_1, 
                     y=choice_2, 
                     size='view', 
                     hover_name='channel_name', 
                     hover_data=['title'],
                     title=f'Perhitungan Like dan Dislike')
    st.plotly_chart(fig)

# Sidebar untuk navigasi antar halaman
page = st.sidebar.selectbox("Pilih Menu", ["Deskripsi Dataset", "Dataset", "Prediksi dan Grafik"])

# Menampilkan halaman berdasarkan pilihan
if page == "Deskripsi Dataset":
    dataset_description()
elif page == "Dataset":
    open_dataset()
elif page == "Prediksi dan Grafik":
    prediction_page()
