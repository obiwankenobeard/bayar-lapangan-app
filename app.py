# app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date
from datetime import datetime

# Display Title & Description
st.title("Pembayaran Iuran Lapangan :badminton_racquet_and_shuttlecock:")
st.markdown("Silakan input nama Anda dan masukkan tanggal yang akan dibayar")
st.markdown('Pembayaran bisa dilakukan pada rekening :blue[BCA Diyandaru Adhitya: 7475023765]')

# Create a connection
conn = st.connection("gsheets", type=GSheetsConnection)

# fetching data iuran
df = conn.read(worksheet="Iuran per Nama", usecols=list((1,2,4,5)),ttl=5)
df_uang_masuk = conn.read(worksheet="Uang Masuk", usecols=list((0,1,2,3,4,5)),ttl=5)

tanggal_main_spesifik = []
tanggal_main_only = []
nama_pengisi = []
tanggal_main = []
harus_dibayar = ()
data_pembayaran_baru_tumpuk = []
data_pembayaran_baru_tumpuk = pd.DataFrame(data_pembayaran_baru_tumpuk)
tanggal_input = date.today()
tanggal_input = datetime.strptime(str(tanggal_input), "%Y-%m-%d")
tanggal_input = tanggal_input.strftime("%d/%m/%Y")

#merubah format tanggal menjadi seperti excel
def date_to_excel_serial(date_str):
    date_str = str(date_str)
    base_date = datetime(1900, 1, 1)
    target_date = datetime.strptime(date_str, "%d/%m/%Y")
    delta = (target_date - base_date).days + 2
    return delta
        

#form pengisian pembayaran iuran
nama_pengisi = st.selectbox ("Nama Atlet", options=sorted(df['Nama'].unique()), index=None)
if nama_pengisi:
    condition = (df['Nama'] == nama_pengisi) & (df['Jumlah uang masuk'] == 0)
    tanggal_main_spesifik = df[condition]
    st.markdown("List tanggal main yang perlu dibayar:")
    st.dataframe(tanggal_main_spesifik)
    tanggal_main_only = tanggal_main_spesifik["Tanggal Main"].tolist()
    tanggal_main = st.multiselect("Tanggal main yang akan dibayar:", options=tanggal_main_only)

    if not tanggal_main:
        pass
    else:
        harus_dibayar = len(tanggal_main)*10000
        ganti_format = ('{:,}'.format(harus_dibayar)) 
        st.markdown(f"Anda akan membayar Rp."+ganti_format)
    if st.button("Bayar", type="primary",use_container_width=True):
        if not tanggal_main:
            st.warning("Pastikan Anda mengisi tanggal main dahulu")
        else:
           for x in tanggal_main:
                tanggal_serial = date_to_excel_serial(x)
                data_pembayaran_baru = pd.DataFrame([{
                         "Jenis" : "by Streamlit",
                         "Code": f"{tanggal_serial} | {nama_pengisi}",
                         "Tanggal": tanggal_input,
                         "Nama": nama_pengisi,
                         "Keterangan": x,
                         "Jumlah": "10000"   
                        }])         
                data_pembayaran_baru_tumpuk=pd.concat([data_pembayaran_baru_tumpuk, data_pembayaran_baru])
                updated_data=pd.concat([df_uang_masuk, data_pembayaran_baru_tumpuk])
                conn.update(worksheet="Uang Masuk",data=updated_data)
                st.success(f"Input Pembayaran Tanggal {x} Sukses")
           
