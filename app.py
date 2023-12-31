# Dibuat Oleh :
# Nama      : Muhammad Hanif Annafi'
# NIM       : 21537141009
# Matkul    : Aplikasi Web

# Import Library Python
import streamlit as st
from datetime import datetime as dt
from PIL import Image

# Konfigurasi Icon dan Judul Halaman
st.set_page_config(page_icon=':mending_heart:', page_title='TATA')

# Library Visualisasi Data
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

# Library Database Spreadsheet
import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
service_account_file = 'mental-health-406315-152f944215eb.json'

# Library Notifikasi
import time
import threading
from plyer import notification

# Fungsi untuk menambah dan mengambil data ke Google Sheets
def add_data(date_string, answers, average):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(service_account_file)
    creds = creds.with_scopes(scope)
    client = gspread.authorize(creds)

    url = "https://docs.google.com/spreadsheets/d/16U04JNWR9Qaib0zoxmzwUtxfYusexja7VYQdatsbmNQ/edit?usp=sharing"
    nama_sheet = "Sheet1"

    sheet = client.open_by_url(url).worksheet(nama_sheet)
    row_to_append = [date_string] + answers + [average]
    sheet.append_row(row_to_append)
    print("Data Berhasil Ditambahkan!")

# Fungsi untuk mencari nilai Rata-Rata dari data Google Sheets
def nilai_rata_total(df):
    df['rata-rata'] = df[['perasaan', 'ketenangan', 'tidur', 'produktivitas', 'menikmati']].astype(float).mean(axis=1)
    return df[['date', 'rata-rata']]

# Fungsi untuk mengambil nilai Rata-Rata Total dari data Google Sheets
def get_total(df):
    kolom_angka = ['perasaan', 'ketenangan', 'tidur', 'produktivitas', 'menikmati', 'rata-rata']
    df[kolom_angka] = df[kolom_angka].apply(pd.to_numeric)

    nilai_harian = df.groupby('date')[kolom_angka].mean().reset_index()
    nilai_total = nilai_harian[kolom_angka].sum() / len(nilai_harian)

    nilai_total_df = pd.DataFrame(nilai_total).transpose()
    nilai_total_df['date'] = 'Total'
    nilai_harian = nilai_harian.append(nilai_total_df, ignore_index=True)

    return nilai_harian

# Fungsi untuk menampilkan Pesan Peringatan (Skala 1 - 10)
def show_alert(total_score):
    if total_score <= 1:
        result = "Kamu Sangat Membutuhkan Bantuan :sob:"
        st.error(f"{result}")
        st.link_button("Hubungi 119", "https://wa.me/6281110500567")
    elif total_score <= 2:
        result = "Kamu Sangat Kehilangan Arah dan Sangat Rapuh :persevere:"
        st.error(f"{result}")
        st.link_button("Hubungi 119", "https://wa.me/6281110500567")
    elif total_score <= 3:
        result = "Kamu Mulai Kehilangan Arah dan Mulai Rapuh :confounded:"
        st.error(f"{result}")
        st.link_button("Hubungi 119", "https://wa.me/6281110500567")
    elif total_score <= 4:
        result = "Kamu Mengalami Keadaan yang Cukup Sulit :sweat:"
        st.warning(f"{result}")
    elif total_score <= 5:
        result = "Kamu Mulai Mengalami Kesulitan :neutral_face:"
        st.warning(f"{result}")
    elif total_score <= 6:
        result = "Kamu Berada di Kondisi yang Cukup Stabil :blush:"
        st.success(f"{result}")
    elif total_score <= 7:
        result = "Kamu Dapat Menjadi Lebih Baik Lagi :grin:"
        st.success(f"{result}")
    elif total_score <= 8:
        result = "Kamu Baik-Baik Saja :smile:"
        st.success(f"{result}")
    elif total_score <= 9:
        result = "Kamu Sangat Merasa Baik :laughing:"
        st.success(f"{result}")
    else:
        result = "Perasaan Kamu Sangat Luar Biasa Baik :satisfied:"
        st.success(f"{result}")

# Fungsi untuk menampilkan notifikasi pada Halaman / Desktop
def show_notification():
    while True:
        notification.notify(
            title='Pengingat Kesehatan Mental',
            message='Jangan lupa untuk mengisi kuisioner kesehatan mental hari ini!',
            timeout=5
        )
        time.sleep(86400)

# Fungsi untuk memulai notifikasi dalam thread terpisah
def start_notification():
    thread = threading.Thread(target=show_notification)
    thread.start()

# Halaman Intro / Beranda
def intro():
    st.title('Selamat Datang di TATA!')
    st.sidebar.success('Silakan Pilih Menu')

    st.markdown(
        '''
        ## Final Aplikasi Web
        - Nama : [Muhammad Hanif Annafi](https://annafikk.my.id)
        - NIM : 21537141009
        - Kelas : I.1 - S1 Teknologi Informasi

        ## Fitur
        - Informasi umum tentang kesehatan mental
        - Kuesioner interaktif yang membantu pengguna dalam melacak kesehatan mental mereka
        - Visualisasi data kesehatan mental pengguna dari waktu ke waktu
        - Panduan yang dipersonalisasi berdasarkan data pengguna
        - Forum diskusi antar pengguna
        - Call center untuk pengguna yang mengalami krisis kesehatan mental
        '''
    )

# Halaman Informasi
def informasi():
    st.header('Informasi Tentang Kesehatan Mental')
    st.subheader('Pengertian Kesehatan Mental')
    st.write(
        '''
        Kesehatan mental adalah kesehatan yang berkaitan dengan kondisi emosi, kejiwaan, dan psikis seseorang. Perlu kamu ketahui 
        bahwa peristiwa yang memiliki dampak besar pada kepribadian dan perilaku seseorang dapat berpengaruh pada kesehatan 
        mentalnya. Misalnya, pelecehan saat usia dini, stres berat dalam jangka waktu lama tanpa adanya penanganan, dan mengalami 
        kekerasan dalam rumah tangga (KDRT). 
        
        Berbagai kondisi tersebut dapat membuat kondisi kejiwaan seseorang menjadi terganggu, sehingga muncul gejala gangguan kesehatan jiwa. 
        Akan tetapi, masalah kesehatan mental dapat dengan mudah mengubah cara seseorang dalam mengatasi stres, komunikasi dengan 
        orang lain, membuat pilihan, dan memicu hasrat untuk menyakiti diri sendiri. Beberapa jenis gangguan mental yang umum terjadi 
        antara lain depresi, gangguan bipolar, kecemasan, gangguan stres pasca trauma (PTSD), gangguan obsesif kompulsif (OCD), 
        dan psikosis. Selain itu, ada beberapa penyakit mental hanya terjadi pada jenis pengidap tertentu seperti postpartum depression yang 
        hanya menyerang wanita setelah melahirkan.
        '''
    )

    st.subheader('Skala Kesehatan Mental')
    image = Image.open('./img/mental_health_score.png')
    st.image(image, caption='Skala Kesehatan Mental')
    st.write(
        '''
        Dapat dilihat pada gambar tersebut bahwa skala kesehatan mental dapat diukur dalam 10 skala. Mulai dari skala 1 yang menandakan
        bahwa seseorang sedang mengalami gangguan kesehatan mental yang sangat parah sehingga sangat memerlukan bantuan orang yang ahli agar
        tidak terjadi hal yang tidak diinginkan. Kemudian terdapat skala 10 yang menandakan bahwa seseorang tidak sedang mengalami gangguan
        kesehatan mental sehingga hidupnya aman, damai, dan tenteram.
        '''
    )

    st.subheader('Peran Vital Psikologi dalam Menangani Gangguan Kesehatan Mental pada Generasi Milenial')
    st.write(
        '''
        Gangguan kesehatan mental menjadi salah satu tantangan serius yang dihadapi oleh generasi milenial saat ini. Psikologi telah menjadi fokus 
        utama dalam membantu mereka mengatasi dan mengelola tantangan ini. Dalam penelitian yang dilakukan oleh Nurwulan Sari dan Sanusi (2023), 
        berbagai pandangan memberikan wawasan yang mendalam tentang bagaimana psikologi dapat berperan dalam mendukung penyintas gangguan kesehatan mental.
        Pandangan tersebut menggambarkan sudut pandang yang berbeda dalam memahami peran psikologi. Menurut pandangan tersebut, psikologi bukan hanya 
        sebatas alat untuk menyampaikan pesan, tetapi juga sebagai kunci penting dalam membina hubungan yang efektif dan membangun pemahaman yang mendalam 
        antara komunikator dan komunikan. Salah satu aspek penting yang ditekankan adalah pentingnya menggunakan bahasa yang baik dan mampu dipahami oleh 
        penyintas gangguan kesehatan mental. Dapat disimpulkan bahwa pesan yang jelas dan bahasa yang tepat menjadi kunci dalam membantu mereka berinteraksi secara efektif dalam masyarakat. 

        _[ Nurwulan Sari, R., & Sanusi, N. (2023). Penerapan Psikologi Komunikasi dalam Mengatasi Gangguan Kesehatan Mental pada Generasi Milenial. Jurnal Penelitian Dan Studi Ilmu Komunikasi, 4(1). http://jurnal.usbypkp.ac.id/index.php/buanakomunikasi ]_     
        '''
    )

# Halaman Dataset
def dataset():
    @st.cache_data
    def load_data():
        url = './dataset/survey.csv'
        df = pd.read_csv(url)
        return df

    # Memuat dan Menampilkan Dataset
    data = load_data()
    st.subheader('Data Survei Kesehatan Mental')
    st.write(data)

    # Mengubah kolom Timestamp menjadi tipe data datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # =========================================> Filter
    selected_columns = ['Age', 'Gender', 'Country', 'treatment', 'seek_help', 'mental_health_consequence']
    new_table = data[selected_columns]
    st.subheader('Data Survei yang Telah Difilter')
    st.write(new_table)

    # =========================================> Usia
    with st.expander('Responden Berdasarkan Usia'):
        # Memecah menjadi beberapa kategori usia
        bins = [0, 20, 30, 40, 50, 60, 70, 100]
        labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
        data['Age_Group'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

        age_group_counts = data['Age_Group'].value_counts()
        age_group_counts = age_group_counts.reindex(labels)

        data_dict = {'Usia': age_group_counts.index, 'Jumlah Responden': age_group_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Usia')
        st.table(df)

        st.subheader('Grafik Responden Berdasarkan Usia')
        fig, ax = plt.subplots()
        age_group_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Age Groups')
        ax.set_ylabel('Counts')
        st.pyplot(fig)

    # =========================================> Gender
    with st.expander('Responden Berdasarkan Jenis Kelamin'):
        # Grafik Berdasarkan Jenis Kelamin Keseluruhan
        gender_counts = data['Gender'].value_counts()

        st.subheader('Grafik Responden Berdasarkan Jenis Kelamin')
        st.bar_chart(gender_counts)


        # Filter Grafik Hanya Untuk Male dan Female
        filtered_data = data[data['Gender'].isin(['Male', 'Female'])]
        gender_counts = filtered_data['Gender'].value_counts()

        data_dict = {'Jenis Kelamin': gender_counts.index, 'Jumlah Responden': gender_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Jenis Kelamin')
        st.table(df)

        st.subheader('Grafik Responden Berdasarkan Jenis Kelamin (M/F)')
        fig, ax = plt.subplots()
        ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # =========================================> Self Employed
    with st.expander('Responden Berdasarkan Jenis Pekerjaan (Wiraswasta)'):
        self_employed_counts = data['self_employed'].value_counts()
        data_dict = {'Wiraswasta': self_employed_counts.index, 'Jumlah Responden': self_employed_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Pekerjaan Wiraswasta')
        st.table(df)

        st.subheader('Apakah Pekerjaan Responden Wiraswasta?')
        fig, ax = plt.subplots()
        ax.pie(self_employed_counts, labels=self_employed_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # =========================================> Negara
    with st.expander('Responden Berdasarkan Negara'):
        st.subheader('Tabel Asal Negara dan Jumlah Responden')
        country_counts = data['Country'].value_counts()
        country_data = pd.DataFrame({'Negara': country_counts.index, 'Jumlah Responden': country_counts.values})
        st.write(country_data)

        # Persentase Responden dari Masing-Masing Negara
        st.subheader('Grafik untuk Persentase Responden dari Masing-Masing Negara')
        fig, ax = plt.subplots()
        ax.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # =========================================> Treatment
    with st.expander('Responden Berdasarkan Treatment'):
        treatment_counts = data['treatment'].value_counts()
        data_dict = {'Treatment': treatment_counts.index, 'Jumlah Responden': treatment_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Perlakuan (Treatment)')
        st.table(df)

        treatment_counts = data['treatment'].value_counts(normalize=True) * 100
        st.subheader('Grafik untuk Persentase Perlakuan (Treatment)')
        fig, ax = plt.subplots()
        ax.pie(treatment_counts, labels=treatment_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # =========================================> Seek Help
    with st.expander('Responden yang Mencari Bantuan'):
        seek_help_counts = data['seek_help'].value_counts()
        data_dict = {'Mencari Bantuan': seek_help_counts.index, 'Jumlah Responden': seek_help_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden yang Mencari Bantuan dalam Kesehatan Mental Mereka')
        st.table(df)

        st.subheader('Grafik untuk Responden yang Mencari Bantuan dalam Kesehatan Mental Mereka')
        seek_help_counts = data['seek_help'].value_counts(normalize=True) * 100
        fig, ax = plt.subplots()
        ax.pie(seek_help_counts, labels=seek_help_counts.index, autopct='%1.1f%%')
        ax.set_title('Seek Help')
        st.pyplot(fig)

    # =========================================> Mental Health Consequence
    with st.expander('Responden yang Memiliki Konsekuensi Kesehatan Mental'):
        mental_health_consequence_counts = data['mental_health_consequence'].value_counts()
        data_dict = {'Konsekuensi': mental_health_consequence_counts.index, 'Jumlah Responden': mental_health_consequence_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Konsekuensi')
        st.table(df)

        st.subheader('Grafik untuk Responden yang Memiliki Konsekuensi Kesehatan Mental')
        mental_health_consequence_counts = data['mental_health_consequence'].value_counts(normalize=True) * 100
        fig, ax = plt.subplots()
        ax.pie(mental_health_consequence_counts, labels=mental_health_consequence_counts.index, autopct='%1.1f%%')
        ax.set_title('Mental Health Consequence')
        st.pyplot(fig)

def dataset2():
    @st.cache_data
    def load_data():
        url = './dataset/student-mental-health.csv'
        df = pd.read_csv(url)
        return df

    # Memuat dan Menampilkan Dataset
    data = load_data()
    st.subheader('Data Mentah Kesehatan Mental pada Mahasiswa')
    st.write(data)

    # =========================================> Filter
    selected_columns = ['Gender', 'Age', 'Course', 'Current_Year', 'Depression', 'Anxiety', 'Panic_Attack', 'Seek_Specialist']
    new_table = data[selected_columns]
    st.subheader('Data yang Telah Difilter')
    st.write(new_table)

    # =========================================> Usia
    with st.expander('Responden Berdasarkan Usia'):
        bins = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        labels = ['17', '18', '19', '20', '21', '22', '23', '24', '25']
        data['Age'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

        age_group_counts = data['Age'].value_counts()
        age_group_counts = age_group_counts.reindex(labels)

        st.subheader('Tabel Responden Berdasarkan Usia')
        data_dict = {'Usia': age_group_counts.index, 'Jumlah Responden': age_group_counts.values}
        df = pd.DataFrame(data_dict)
        st.table(df)

        st.subheader('Grafik Responden Berdasarkan Usia')
        fig, ax = plt.subplots()
        age_group_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Kelompok Usia')
        ax.set_ylabel('Jumlah Responden')
        st.pyplot(fig)

    # =========================================> Gender
    with st.expander('Responden Berdasarkan Jenis Kelamin'):
        Gender_counts = data['Gender'].value_counts()
        data_dict = {'Jenis Kelamin': Gender_counts.index, 'Jumlah Responden': Gender_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Jumlah Responden Berdasarkan Jenis Kelamin')
        st.table(df)

        st.subheader('Grafik Responden Berdasarkan Jenis Kelamin')
        st.bar_chart(Gender_counts)

    # =========================================> Jurusan
    with st.expander('Responden Berdasarkan Jurusan'):
        Course_counts = data['Course'].value_counts()
        data_dict = {'Jurusan': Course_counts.index, 'Jumlah Responden': Course_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Jumlah Responden Berdasarkan Jurusan')
        st.table(df)

    # =========================================> Tahun Kuliah
    with st.expander('Responden Berdasarkan Tahun Kuliah'):
        st.subheader('Tabel Jumlah Responden Berdasarkan Tahun Kuliah')
        Current_Year_counts = data['Current_Year'].value_counts()
        Current_Year_data = pd.DataFrame({'Tahun Kuliah': Current_Year_counts.index, 'Jumlah Responden': Current_Year_counts.values})
        st.write(Current_Year_data)

        # Persentase Responden dari Tahun Kuliah
        st.subheader('Grafik untuk Persentase Tahun Kuliah dari Responden')
        fig, ax = plt.subplots()
        ax.pie(Current_Year_counts, labels=Current_Year_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # =========================================> Depresi
    with st.expander('Responden yang Memiliki Depresi'):
        Depression_counts = data['Depression'].value_counts(normalize=True) * 100
        data_dict = {'Depresi': Depression_counts.index, 'Jumlah Responden': Depression_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Depresi')
        st.table(df)

        fig, ax = plt.subplots()
        ax.pie(Depression_counts, labels=Depression_counts.index, autopct='%1.1f%%')
        st.subheader('Apakah Responden Mengalami Depresi?')
        st.pyplot(fig)

    # =========================================> Anxiety
    with st.expander('Responden yang Memiliki Anxiety'):
        Anxiety_counts = data['Anxiety'].value_counts(normalize=True) * 100
        data_dict = {'Depresi': Anxiety_counts.index, 'Jumlah Responden': Anxiety_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Anxiety')
        st.table(df)

        fig, ax = plt.subplots()
        ax.pie(Anxiety_counts, labels=Anxiety_counts.index, autopct='%1.1f%%')
        st.subheader('Apakah Responden Mengalami Anxiety?')
        ax.set_title('Anxiety')
        st.pyplot(fig)

    # =========================================> Panic_Attack
    with st.expander('Responden yang Memiliki Serangan Kecemasan'):
        Panic_Attack_counts = data['Panic_Attack'].value_counts(normalize=True) * 100
        data_dict = {'Serangan Kecemasan': Panic_Attack_counts.index, 'Jumlah Responden': Panic_Attack_counts.values}
        df = pd.DataFrame(data_dict)
        st.subheader('Tabel Responden Berdasarkan Serangan Kecemasan')
        st.table(df)
        
        fig, ax = plt.subplots()
        ax.pie(Panic_Attack_counts, labels=Panic_Attack_counts.index, autopct='%1.1f%%')
        st.subheader('Apakah Responden Mengalami Serangan Kecemasan?')
        ax.set_title('Panic Attack')
        st.pyplot(fig)

# Halaman Kuisioner
def pertanyaan():
    st.write("")
    st.write("Apakah Anda ingin mengaktifkan notifikasi pengingat?")
    if st.button('Aktifkan Notifikasi'):
        start_notification()
        st.toast('Notifikasi telah diaktifkan!')

    st.title("Kuisioner Kesehatan Mental")
    questions = [
        "Bagaimana perasaanmu hari ini? (0 = Sangat Buruk, 10 = Sangat Baik)",
        "Bagaimana kamu menilai tingkat ketenanganmu hari ini? (0 = Sangat Buruk, 10 = Sangat Baik)",
        "Bagaimana tidurmu tadi malam? (0 = Sangat Tidak Nyenyak, 10 = Sangat Nyenyak)",
        "Bagaimana tingkat produktivitasmu hari ini? (0 = Sangat Tidak Produktif, 10 = Sangat Produktif)",
        "Bagaimana kamu menikmati harimu hari ini? (0 = Tidak Sama Sekali, 10 = Sangat Menikmati)"
    ]

    answers = []

    for question in questions:
        answer = st.slider(question, 0, 10)
        answers.append(answer)

    average = sum(answers) / len(answers)

    st.markdown('##')
    st.write(f"Skor Rata-Rata Kesehatan Mental Kamu Hari Ini : {average:.1f}")

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=average,
        mode="gauge+number",
        title={'text': "Skor Kesehatan Mental"},
        gauge={
            'axis': {'range': [0, 10]},
            'steps': [
                {'range': [0, 2], 'color': "red"},
                {'range': [2, 4], 'color': "orange"},
                {'range': [4, 6], 'color': "yellow"},
                {'range': [6, 8], 'color': "lightgreen"},
                {'range': [8, 10], 'color': "green"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': average}
        }
    ))

    st.plotly_chart(fig, use_container_width=True, height=50)

    if st.button('Kirim Hasil Skor Kamu'):
        now = dt.now()
        date_string = now.strftime('%d/%m/%Y')
        st.write(f"Date: {date_string}")
        add_data(date_string, answers, average)
        st.success("Skor Kesehatan Mental Kamu Telah Berhasil Di Kirim!")
        st.toast("Terkirim!")

    return answers

# Halaman Visualisasi Data
def visualisasi():
    st.cache_data
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(service_account_file)
    creds = creds.with_scopes(scope)
    client = gspread.authorize(creds)

    url = "https://docs.google.com/spreadsheets/d/16U04JNWR9Qaib0zoxmzwUtxfYusexja7VYQdatsbmNQ/edit?usp=sharing"
    nama_sheet = "Sheet1"

    sheet = client.open_by_url(url).worksheet(nama_sheet)
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    st.subheader('Visualisasi Data Kesehatan Mental')
    st.info('Scroll Ke Bawah Untuk Melihat Hasil Selengkapnya')
    st.dataframe(df)

    with st.expander('Rata-Rata Skor Kesehatan Mental per Hari'):
        fig1 = px.line(df, x="date", y="rata-rata", line_shape="spline", color_discrete_sequence=["red"])
        fig1.update_layout(xaxis_tickformat='%Y-%m-%d', title="Rata-Rata Skor Kesehatan Mental per Hari")
        
        if fig1:
            st.plotly_chart(fig1)
        else:
            st.error("Gagal membuat grafik. Pastikan data yang digunakan sesuai.")


    with st.expander('Skor Kesehatan Mental per Hari'):
        fig2 = px.line(df, x="date", y=["perasaan", "ketenangan", "tidur", "produktivitas", "menikmati"], line_shape="spline")
        fig2.update_layout(xaxis_tickformat='%Y-%m-%d', title="Skor Kesehatan Mental per Hari")

        if fig2:
            st.plotly_chart(fig2)
        else:
            st.error("Gagal membuat grafik. Pastikan data yang digunakan sesuai.")

    with st.expander('Rata-Rata Kesehatan Mental per Kategori'):
        average_scores = nilai_rata_total(df)
        fig3 = px.bar_polar(average_scores, r="rata-rata", theta="date", template="plotly_dark")
        fig3.update_traces(opacity=0.7)
        fig3.update_layout(title="Rata-Rata Kesehatan Mental per Kategori")

        if fig3:
            st.plotly_chart(fig3)
        else:
            st.error("Gagal membuat grafik. Pastikan data yang digunakan sesuai.")
    
    df['rata-rata'] = df.mean(axis=1)
    total_average = df['rata-rata'].mean()
    show_alert(total_average)
    return total_average


from transformers import pipeline
sentiment_analysis = pipeline("sentiment-analysis")
def analyze_sentiment(text):
    result = sentiment_analysis(text)
    return result[0]['label']

# Halaman Forum Diskusi
def diskusi():
    st.cache_data
    from datetime import datetime
    st.title('Forum Diskusi Kesehatan Mental')
    st.write('Selamat datang di forum diskusi! Silakan berbagi pengalaman Anda atau tanyakan sesuatu kepada komunitas.')

    username = st.text_input("Nama Pengguna", value="")
    userinput = st.text_area('Tulis komentar atau pertanyaan Anda di sini')

    if st.button('Kirim'):
        if not username or not userinput:
            st.warning("Harap isi kedua kotak teks sebelum mengirim!")
        else:
            sent_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sentiment = analyze_sentiment(userinput)

            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = service_account.Credentials.from_service_account_file(service_account_file)
            creds = creds.with_scopes(scope)
            client = gspread.authorize(creds)

            url = "https://docs.google.com/spreadsheets/d/16U04JNWR9Qaib0zoxmzwUtxfYusexja7VYQdatsbmNQ/edit?usp=sharing"
            sheet_name = "Sheet2"

            sheet = client.open_by_url(url).worksheet(sheet_name)
            row_to_append = [sent_time, username, userinput, sentiment]
            sheet.append_row(row_to_append)
            st.write("Pesan Anda telah terkirim!")
    
    # Menampilkan pesan yang telah dikirim oleh pengguna sebelumnya
    st.subheader('Pesan yang Telah Dikirim')
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(service_account_file)
    creds = creds.with_scopes(scope)
    client = gspread.authorize(creds)

    url = "https://docs.google.com/spreadsheets/d/16U04JNWR9Qaib0zoxmzwUtxfYusexja7VYQdatsbmNQ/edit?usp=sharing"
    sheet_name = "Sheet2"

    sheet = client.open_by_url(url).worksheet(sheet_name)
    data = sheet.get_all_values()

    # Menampilkan pesan yang dikirim dalam bentuk dataframe
    df_messages = pd.DataFrame(data[1:], columns=data[0])

    # Menampilkan pesan dalam bentuk chat message
    for index, row in df_messages.iterrows():
        with st.expander(f"Diposting Pada {row[0]} oleh : {row[1]}", expanded=True):
            st.write(f"Pesan: {row[2]}")
            st.write(f"Sentimen: {row[3]}")

# Halaman Help Center
def bundir():
    st.title('Kamu Tidak Sendiri')
    st.write(
        'Jika kamu ataupun orang lain sedang mengalami hari yang buruk, ingat bantuan akan selalu tersedia.')

    with st.expander('Lihat Sumber Daya'):
        st.write(
            '''
            ## Berbicara dengan seorang profesional
            Jika kamu ataupun orang lain sedang mengalami fase terburuk, berikut adalah beberapa sumber daya yang mungkin dapat membantu.
            ''')
        image2 = Image.open('./img/logo_kemenkes.jpg')
        st.image(image2, caption='Kementerian Kesehatan Republik Indonesia')
        st.write('Layanan 24/7 Kementerian Kesehatan Republik Indonesia')
        st.link_button("119", "https://wa.me/6281110500567")
        st.link_button(
            "Kontak", "https://www.kemkes.go.id/id/layanan/kontak-kami")

    st.title('Tips dan Dukungan')
    with st.expander('Bicaralah dengan seseorang yang kamu percayai'):
        st.write(
            '''
            - Tidak jarang kamu merasa sulit untuk meminta bantuan atau membuka diri tentang perasaan yang kamu alami. Namun, hanya dengan berbicara kepada satu orang yang kamu percayai dapat membuat kamu merasa jauh lebih baik.
            - Beritahukanlah kepada seorang teman atau anggota keluarga yang kamu percayai tentang apa yang kamu alami. Gambarkan bagaimana perasaan kamu, apa yang telah terjadi, dan dukungan apa yang menurut kamu akan membantu. Jangan ragu untuk meminta pertolongan.
            ''')
    with st.expander('Luangkan Waktu'):
        st.write(
            '''
            - Mengambil napas secara perlahan dapat membantu kamu merasa lebih rileks secara fisik dan pikiran. Cobalah menghitung perlahan hingga angka 4 saat kamu menghirup udara melalui hidungmu, kemudian tahan napas tersebut dan hitung hingga angka 7. Lalu hitung hingga angka 8 saat kamu mengeluarkan napas melalui mulut.
            - Berlatih untuk dapat fokus. Cara yang paling mudah untuk melakukannya adalah menyebutkan 5 hal yang bisa kamu lihat, 4 hal yang bisa kamu sentuh, 3 hal yang bisa kamu dengar, 2 hal yang bisa kamu cium, dan 1 hal yang bisa kamu rasakan.
            - Cobalah semprotkan sedikit air es ke wajahmu atau buka jendela ruanganmu untuk menghirup udara segar yang sejuk. Hal ini dapat membantu menenangkan sistem sarafmu.
            - Catatlah apa yang ada di dalam pikiranmu. Jika kamu tidak tahu harus mulai dari mana, coba tuliskan seolah-olah kamu sedang bercerita kepada seseorang yang kamu percayai.
            ''')
    with st.expander('Jelajahi kegiatan yang membuatmu bahagia'):
        st.write(
            '''
            - Berjalan di luar, menjelajahi alam, dan menikmati udara segar. Kamu juga bisa hanya tinggal di dalam ruangan dan menari mengikuti lagu yang kamu sukai.
            - Menonton film favoritmu, menghabiskan waktu bersama teman, membaca buku, memanjakan diri dengan camilan, atau membuat daftar putar musik.
            - Pastikan kamu mendapatkan cukup tidur, berolahraga secara teratur, dan makan dengan baik.
            ''')
    with st.expander('Terhubunglah dengan dunia di sekitarmu'):
        st.write(
            '''
            - Telepon seseorang yang sudah lama tidak kamu temui.
            - Temukan lebih banyak tentang kelompok minat atau relawan lokal yang bisa kamu ikuti untuk bertemu dengan orang baru.
            - Ikuti kelas atau mulai hobi yang selama ini ingin kamu coba, seperti olahraga baru atau kegiatan kreatif.
            ''')
    with st.expander('Renungkan tentang hal-hal penting bagimu'):
        st.write(
            '''
            - Tulis 5 orang atau hal yang membuatmu merasa bahagia, bersyukur, atau aman.
            - Sampaikan rasa terima kasihmu kepada seseorang yang kamu hargai dan beritahu mereka seberapa besar kamu menghargai mereka.
            ''')

# Konfigurasi Halaman
nama_halaman = {
    'Beranda': intro,
    'Informasi Umum': informasi,
    'Data Hasil Survei': dataset,
    'Data Hasil Mahasiswa': dataset2,
    'Pengisian Kuisioner': pertanyaan,
    'Visualisasi Data Kuisioner': visualisasi,
    'Forum Diskusi': diskusi,
    'Help Center': bundir
}

# Konfigurasi Sidebar Halaman
demo = st.sidebar.selectbox('Silakan Pilih Menu', nama_halaman)
nama_halaman[demo]()