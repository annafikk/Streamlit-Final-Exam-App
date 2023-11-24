# Import Library Python
import streamlit as st
import datetime as dt
import plotly.graph_objects as go

# Halaman Intro
def intro():
    st.title('Selamat Datang di Streamlit!')
    st.sidebar.success('Silakan Pilih Menu')

    st.subheader('Final Aplikasi Web')
    st.markdown(
        '''
        - Nama : [Muhammad Hanif Annafi](https://annafikk.my.id)
        - NIM : 21537141009
        - Kelas : I.1 - S1 Teknologi Informasi
        '''
    )

# Halaman Informasi
def informasi():
    import pandas as pd
    import plotly.express as px

    st.title('Informasi Tentang Mental Health')
    st.subheader('Pengertian Mental Health')
    st.write(
        '''
        Kesehatan jiwa atau sebutan lainnya kesehatan mental adalah kesehatan yang berkaitan dengan kondisi emosi, kejiwaan, dan psikis seseorang. 
        Perlu kamu ketahui bahwa peristiwa dalam hidup yang berdampak besar pada kepribadian dan perilaku seseorang bisa berpengaruh pada kesehatan 
        mentalnya.Misalnya, pelecehan saat usia dini, stres berat dalam jangka waktu lama tanpa adanya penanganan, dan mengalami kekerasan dalam 
        rumah tangga. Berbagai kondisi tersebut bisa membuat kondisi kejiwaan seseorang terganggu, sehingga muncul gejala gangguan kesehatan jiwa. 
        Akan tetapi, masalah kesehatan mental bisa mengubah cara seseorang dalam mengatasi stres, berhubungan dengan orang lain, membuat pilihan, 
        dan memicu hasrat untuk menyakiti diri sendiri. Beberapa jenis gangguan mental yang umum terjadi antara lain depresi, gangguan bipolar, 
        kecemasan, gangguan stres pasca trauma (PTSD), gangguan obsesif kompulsif (OCD), dan psikosis. Selain itu, ada beberapa penyakit mental 
        hanya terjadi pada jenis pengidap tertentu, seperti postpartum depression hanya menyerang ibu setelah melahirkan.
        '''
    )

    data = pd.read_csv('dataset\survey.csv')
    data.dropna(subset=['seek_help'], inplace=True)

    st.write(data)

    st.write(data.describe())

# Halaman Kuisioner
def pertanyaan():
    from datetime import datetime as dt
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
    st.write(f"Your average mental health score today is {average:.1f}")

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=average,
        mode="gauge+number",
        title={'text': "Mental Health Score"},
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

    now = dt.now()
    date_string = now.strftime('%Y-%m-%d')
    st.write(f"Date: {date_string}")

    return answers

# Konfigurasi Halaman
nama_halaman = {
    'Beranda': intro,
    'Informasi Umum': informasi,
    'Kuisioner': pertanyaan
}

# Konfigurasi Sidebar Halaman
demo = st.sidebar.selectbox('Silakan Pilih Menu', nama_halaman)
nama_halaman[demo]()
