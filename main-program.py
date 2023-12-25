import mysql.connector
import re
import datetime
import calendar
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

#konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rental_motor'
}

def registrasiPemilik(con, username, password, nik, nama, no_hp):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO pemilik (username, nik, nama, no_hp, password) VALUES (%s, %s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (username, nik, nama, no_hp, password)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def registrasiPenyewa(con, username, password, nik, nama, no_hp):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO penyewa (username, nik, nama, no_hp, password) VALUES (%s, %s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (username, nik, nama, no_hp, password)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def cariUsername(con, role, inputan_username):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca username dari database
    select_query = f'SELECT username FROM {role}'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua username ke dalam variabel rows
    usernames = cursor.fetchall()

    #print semua row
    for username in usernames:
        #jika username ditemukan di database
        if username == (inputan_username,):
            return True

    #jika username tidak ditemukan di database    
    return False

def cekPassword(con, role, inputan_username, inputan_password):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca password dari database
    select_query = f'SELECT password FROM {role} where username="{inputan_username}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan password ke dalam variabel rows
    passwords = cursor.fetchall()

    #print semua row
    for password in passwords:
        #jika password yang diinputkan user benar
        if password == (inputan_password,):
            return True

    #jika password yang diinputkan user salah    
    return False

#fungsi untuk membaca semua data di database
def readMotor(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca data dari database
        select_query = f'SELECT plat_nomor, merek, tipe, sewa_perhari FROM motor where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca data dari database
        select_query = f'SELECT plat_nomor, merek, tipe, sewa_perhari FROM motor'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    motor_dict = {
        'Plat Nomor': [],
        'Merek': [],
        'Tipe': [],
        'Sewa Perhari': []
    }

    #masukkan semua data motor ke dictionary motor_dict
    for i in range(len(rows)):
        motor_dict['Plat Nomor'].append(rows[i][0])
        motor_dict['Merek'].append(rows[i][1])
        motor_dict['Tipe'].append(rows[i][2])
        motor_dict['Sewa Perhari'].append(rows[i][3])

    print(pd.DataFrame(motor_dict))

def cariPlatnomor(con, inputan_platnomor, id_pemilik=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    if id_pemilik=='':
        #query sql untuk membaca plat nomor dari database
        select_query = f'SELECT plat_nomor FROM motor'
    else:
        #query sql untuk membaca plat nomor dari database
        select_query = f'SELECT plat_nomor FROM motor WHERE id_pemilik="{id_pemilik}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel rows
    plats = cursor.fetchall()

    #print semua row
    for plat_nomor in plats:
        #jika plat nomor ditemukan di database
        if plat_nomor == (inputan_platnomor.upper(),):
            return inputan_platnomor.upper()

    #jika plat nomor tidak ditemukan di database    
    return False

def tambahMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO motor (plat_nomor, merek, tipe, sewa_perhari, id_pemilik) VALUES (%s, %s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (plat_nomor.upper(), merek, tipe, sewa_perhari, id_pemilik)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def updateMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk update data di database
    update_query = 'UPDATE motor SET plat_nomor=%s, merek=%s, tipe=%s, sewa_perhari=%s WHERE plat_nomor=%s AND id_pemilik=%s'

    #data yang digunakan pada query
    value = (plat_nomor.upper(), merek, tipe, sewa_perhari, plat_nomor.upper(), id_pemilik)

    #masukkan data ke database
    cursor.execute(update_query, value)

    #simpan perubahan
    con.commit()

#fungsi untuk hapus data di database
def hapusMotor(con, plat_nomor, id_pemilik):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk hapus data
    delete_query = 'DELETE FROM motor WHERE plat_nomor=%s and id_pemilik=%s'

    #id dari data yang akan dihapus
    value = (plat_nomor, id_pemilik)

    #hapus data
    cursor.execute(delete_query, value)

    #simpan perubahan
    con.commit()

    #jeda 2 detik
    sleep(2)

#fungsi untuk membaca semua data di database
def readPenyewaan(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca data dari database
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca data dari database
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan WHERE id_penyewa="{username}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    penyewaan_dict = {
        'Id Penyewaan': [],
        'Tgl Penyewaan': [],
        'Tgl Pengembalian': [],
        'Plat Nomor': [],
        'Merek Motor': [],
        'Tipe Motor': [],
        'Sewa Perhari': [],
        'Biaya': []
    }

    #masukkan semua data penyewaan ke dictionary penyewaan_dict
    for i in range(len(rows)):
        penyewaan_dict['Id Penyewaan'].append(rows[i][0])
        penyewaan_dict['Tgl Penyewaan'].append(rows[i][1])
        penyewaan_dict['Tgl Pengembalian'].append(rows[i][2])
        penyewaan_dict['Plat Nomor'].append(rows[i][3])
        penyewaan_dict['Merek Motor'].append(rows[i][4])
        penyewaan_dict['Tipe Motor'].append(rows[i][5])
        penyewaan_dict['Sewa Perhari'].append(rows[i][6])
        penyewaan_dict['Biaya'].append('-')

    for i in range(len(rows)):
        if penyewaan_dict['Tgl Pengembalian'][i]:
            tgl_penyewaan = penyewaan_dict['Tgl Penyewaan'][i]
            tgl_pengembalian = penyewaan_dict['Tgl Pengembalian'][i]
            total_hari = int((np.datetime64(tgl_pengembalian) - np.datetime64(tgl_penyewaan))/np.timedelta64(1,'D'))
            if total_hari<1:
                biaya = penyewaan_dict['Sewa Perhari'][i]
            else:
                biaya = total_hari * penyewaan_dict['Sewa Perhari'][i]
            penyewaan_dict['Biaya'][i] = biaya

    print(pd.DataFrame(penyewaan_dict))

#fungsi untuk membaca semua data di database
def showTop3Rented(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca data dari database
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca data dari database
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    penyewaan_dict = {
        'Plat Nomor': [],
    }

    #masukkan semua data penyewaan ke dictionary penyewaan_dict
    for i in range(len(rows)):
        penyewaan_dict['Plat Nomor'].append(rows[i][3])

    df = pd.DataFrame(penyewaan_dict)
    # Menghitung frekuensi plat nomor
    frequencies = df['Plat Nomor'].value_counts()

    # Mengambil dua plat nomor paling sering digunakan
    top_two_plates = frequencies.head(3)

    # Membuat grafik batang
    plt.bar(top_two_plates.index, top_two_plates.values)
    plt.xlabel('Motor')
    plt.ylabel('Frekuensi')
    plt.title('Top 3 Motor Paling Sering Disewa')
    plt.show()

def cariIdPenyewaanDiPenyewaan(con, inputan_idpenyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca data dari database
    select_query = f'SELECT id_penyewaan FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel rows
    penyewaan_ids = cursor.fetchall()

    #print semua row
    for id_penyewaan in penyewaan_ids:
        #jika plat nomor ditemukan di database
        if f'{id_penyewaan}' == f'({inputan_idpenyewaan},)':
            return inputan_idpenyewaan

    #jika plat nomor tidak ditemukan di database    
    return False

def cariIdPenyewaanDiPengembalian(con, inputan_idpenyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca data dari database
    select_query = f'SELECT id_penyewaan FROM pengembalian'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel rows
    penyewaan_ids = cursor.fetchall()

    #print semua row
    for id_penyewaan in penyewaan_ids:
        #jika plat nomor ditemukan di database
        if f'{id_penyewaan}' == f'({inputan_idpenyewaan},)':
            return inputan_idpenyewaan

    #jika plat nomor tidak ditemukan di database    
    return False

def getMotorElements(con, inputan_platnomor):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca plat nomor dari database
    select_query = f'SELECT plat_nomor,merek,tipe,sewa_perhari,id_pemilik FROM motor'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel rows
    motors = cursor.fetchall()

    motor_items = []
    #print semua row
    for motor in motors:
        #jika plat nomor ditemukan di database
        if motor[0] == inputan_platnomor.upper():
            for item in motor:
                motor_items.append(item)
            return motor_items

    #jika plat nomor tidak ditemukan di database    
    return False

def sewaMotor(con, tgl_penyewaan, plat_nomor, merek_motor, tipe_motor,  sewa_perhari, id_pemilik, id_penyewa):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO penyewaan (tgl_penyewaan, plat_nomor, merek_motor, tipe_motor, sewa_perhari, id_pemilik, id_penyewa) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (tgl_penyewaan, plat_nomor.upper(), merek_motor, tipe_motor, sewa_perhari, id_pemilik, id_penyewa)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def setTglPengembalian(con, id_penyewaan, tgl_pengembalian):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk update data di database
    update_query = 'UPDATE penyewaan SET tgl_pengembalian=%s WHERE id_penyewaan=%s'

    #data yang digunakan pada query
    value = (tgl_pengembalian, id_penyewaan)

    #masukkan data ke database
    cursor.execute(update_query, value)

    #simpan perubahan
    con.commit()

def getPenyewaanElements(con, id_penyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca id_penyewaan dari database
    select_query = f'SELECT id_penyewaan,plat_nomor,tgl_penyewaan FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua id_penyewaan ke dalam variabel rows
    penyewaans = cursor.fetchall()

    penyewaan_items = []
    #print semua row
    for penyewaan in penyewaans:
        #jika id_penyewaan ditemukan di database
        if f'{penyewaan[0]}' == f'{id_penyewaan}':
            for item in penyewaan:
                penyewaan_items.append(item)
            return penyewaan_items

    #jika plat nomor tidak ditemukan di database    
    return False

def kembalikanMotor(con, id_penyewaan, plat_nomor, tgl_penyewaan, tgl_pengembalian):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO pengembalian (tgl_penyewaan, tgl_pengembalian, plat_nomor, id_penyewaan) VALUES (%s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (tgl_penyewaan, tgl_pengembalian, plat_nomor.upper(), id_penyewaan)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def dashboard(con, loggedin_user, loggedin_role):
    while loggedin_user != '':
        #jika yang login adalah pemilik
        if loggedin_role == 'pemilik':
            print('Daftar Motor')
            readMotor(con, loggedin_role, loggedin_user)
            print()
            print('Transaksi Penyewaan')
            readPenyewaan(con, loggedin_role, loggedin_user)
            print()

            print('Aksi:')
            print('1. Tambah Motor')
            print('2. Update Motor')
            print('3. Delete Motor')
            print('4. Kembalikan Motor')
            print('5. Tampilkan motor yang paling sering disewa')
            print('6. Logout')
            aksi_dipilih = input('Pilih aksi [1-5]: ')

            if aksi_dipilih == '1':
                inputan_kosong = True

                while inputan_kosong:
                    inputan_sesuai = False

                    while not inputan_sesuai:
                        print()
                        plat_nomor = input('Plat Nomor: ')
                        merek = input('Merek Motor: ')
                        tipe = input('Tipe Motor: ')
                        sewa_perhari = input('Sewa Perhari: Rp')
                        id_pemilik = loggedin_user

                        if plat_nomor!='' or merek!='' or tipe!='' or sewa_perhari!='':
                            inputan_kosong = False
                            platnomor_sudah_ada = cariPlatnomor(con, plat_nomor)
                                
                            if platnomor_sudah_ada:
                                print('Plat nomor sudah terdaftar!')
                                sleep(2)
                            else:
                                pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z]$')

                                if not pattern.match(plat_nomor):
                                        print('Plat motor hanya diawali dan diakhiri oleh huruf dan hanya boleh mengandung huruf, angka, dan spasi!')
                                        sleep(2)
                                else:
                                    if not sewa_perhari.isdigit():
                                        print('Sewa perhari hanya boleh bilangan integer!')
                                    else:
                                        inputan_sesuai = True
                                        try:
                                            tambahMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik)
                                            print('Tambah motor berhasil.')
                                            print()
                                        except:
                                            print('Tambah motor gagal!')
                                            print()
                                    sleep(2)
                        else:
                            print('Inputan tidak boleh kosong!')
                            sleep(2)
            elif aksi_dipilih == '2':
                platnomor_ketemu = False

                while not platnomor_ketemu:
                    print()
                    plat_nomor = input('Masukkan plat nomor: ')
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor, loggedin_user)

                    if platnomor_ketemu:
                        inputan_kosong = True

                        while inputan_kosong:
                            inputan_sesuai = False

                            while not inputan_sesuai:
                                print()
                                plat_nomor = input('Plat Nomor: ')
                                merek = input('Merek Motor: ')
                                tipe = input('Tipe Motor: ')
                                sewa_perhari = input('Sewa Perhari: Rp')
                                id_pemilik = loggedin_user

                                if plat_nomor!='' or merek!='' or tipe!='' or sewa_perhari!='':
                                    inputan_kosong = False
                                    platnomor_sudah_ada = cariPlatnomor(con, plat_nomor)

                                    if platnomor_sudah_ada and (plat_nomor.upper()!=platnomor_ketemu):
                                        print('Plat nomor sudah terdaftar!')
                                        sleep(2)
                                    else:
                                        pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z]$')

                                        if not pattern.match(plat_nomor):
                                            print('Plat motor hanya diawali dan diakhiri oleh huruf dan hanya boleh mengandung huruf, angka, dan spasi!')
                                            sleep(2)
                                        else:
                                            if not sewa_perhari.isdigit():
                                                print('Sewa perhari hanya boleh bilangan integer!')
                                            else:
                                                inputan_sesuai = True
                                                try:
                                                    updateMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik)
                                                    print('Update motor berhasil.')
                                                    print()
                                                except:
                                                    print('Update motor gagal!')
                                                    print()
                                            sleep(2)
                                else:
                                    print('Inputan tidak boleh kosong!')
                                    sleep(2)
                    else:
                        print(f'Plat nomor {plat_nomor} tidak terdaftar!')
                        sleep(2)
            elif aksi_dipilih == '3':
                platnomor_ketemu = False

                while not platnomor_ketemu:
                    plat_nomor = input('Masukkan plat nomor: ')
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor, loggedin_user)

                    if platnomor_ketemu:
                        try:
                            hapusMotor(con, plat_nomor, loggedin_user)
                            print('Hapus motor berhasil.')
                            print()
                        except:
                            print('Hapus motor gagal!')
                            print()
                        sleep(2)
                    else:
                        print(f'Plat nomor {plat_nomor} tidak terdaftar!')
                        sleep(2)
            elif aksi_dipilih == '4':
                print()
                id_penyewaan = input('Masukkan id penyewaan: ')

                if cariIdPenyewaanDiPenyewaan(con, id_penyewaan) and (not cariIdPenyewaanDiPengembalian(con, id_penyewaan)):
                    penyewaan_elements = getPenyewaanElements(con, id_penyewaan)
                    plat_nomor = penyewaan_elements[1]
                    tgl_penyewaan = penyewaan_elements[2]

                    try:
                        current_GMT = time.gmtime()
                        ts = calendar.timegm(current_GMT)
                        date_time = datetime.datetime.fromtimestamp(ts)
                        str_date_time = date_time.strftime("%Y-%m-%d")

                        setTglPengembalian(con, id_penyewaan, str_date_time)
                        kembalikanMotor(con, id_penyewaan, plat_nomor, tgl_penyewaan, str_date_time)
                        print('Motor berhasil dikembalikan!')
                        print()
                        sleep(2)
                    except:
                        print('Motor gagal dikembalikan!')
                        print()
                        sleep(2)
                else:
                    print('Id penyewaan tidak ketemu atau motor sudah dikembalikan!')
                    print()
                    sleep(2)
            elif aksi_dipilih == '5':
                showTop3Rented(con, loggedin_role, loggedin_user)
            elif aksi_dipilih == '6':
                loggedin_user = ''
                print('Logout berhasil.')
                print()
                sleep(2)
                return True
            else:
                print('Inputan salah! Masukkan angka 1-5!')
                print()
                sleep(2)
        #jika yang login adalah penyewa
        else:
            while loggedin_user !='':
                print('Daftar Motor')
                readMotor(con, loggedin_role, loggedin_user)
                print()
                print('Transaksi Penyewaan')
                readPenyewaan(con, loggedin_role, loggedin_user)
                print()

                print('Aksi:')
                print('1. Sewa Motor')
                print('2. Tampilkan motor yang paling sering disewa')
                print('3. Logout')
                aksi_dipilih = input('Pilih aksi [1/2]: ')

                if aksi_dipilih == '1':
                    print()
                    plat_nomor = input('Plat Nomor: ')
                    
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor)

                    if platnomor_ketemu:
                        motor_elements = getMotorElements(con, plat_nomor)
                        merek = motor_elements[1]
                        tipe = motor_elements[2]
                        sewa_perhari = motor_elements[3]
                        id_pemilik = motor_elements[4]

                        try:
                            current_GMT = time.gmtime()
                            ts = calendar.timegm(current_GMT)
                            date_time = datetime.datetime.fromtimestamp(ts)
                            str_date_time = date_time.strftime("%Y-%m-%d")

                            sewaMotor(con, str_date_time, plat_nomor, merek, tipe, sewa_perhari, id_pemilik, loggedin_user)
                            print('Sewa motor berhasil!')
                            print()
                            sleep(2)
                        except:
                            print('Sewa motor gagal!')
                            print()
                            sleep(2)
                elif aksi_dipilih == '2':
                    showTop3Rented(con, loggedin_role)
                elif aksi_dipilih == '3':
                    loggedin_user = ''
                    print('Logout berhasil.')
                    print()
                    sleep(2)
                    return True
                else:
                    print('Inputan salah! Masukkan angka 1 atau 2!')
                    print()
                    sleep(2)


def main(con):
    belum_login = True
    loggedin_user = ''
    loggedin_role = ''

    while belum_login:
        print('Menu')
        print('1. Register')
        print('2. Login')
        print('3. Hentikan Program')
        menu_dipilih = input('Pilih menu [1/2]: ')

        if menu_dipilih == '1':
            role_dipilih = False

            print('Registrasi User')

            while not role_dipilih:
                print()
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
                print('0. Kembali')
                role = input('Pilih role [1/2]: ')

                if role == '1':
                    role_dipilih = True
                    inputan_kosong = True

                    while inputan_kosong:
                        username_sesuai = False

                        while not username_sesuai:
                            print()
                            nik = input('NIK: ')
                            nama = input('Nama: ')
                            no_hp = input('Nomor HP: ')
                            username = input('Username: ')
                            password = input('Password: ')

                            if nik!='' or nama!='' or no_hp!='' or username!='' or password!='':
                                inputan_kosong = False
                                pattern = re.compile("^[a-z0-9_.]+$")

                                if not pattern.match(username):
                                    print('Username hanya boleh berupa huruf kecil, angka, underscore, dan titik!')
                                    sleep(2)
                                else:
                                    chosen_role = 'pemilik'
                                    username_sudah_ada = cariUsername(con, chosen_role, username)

                                    if username_sudah_ada:
                                        print('Username sudah terdaftar!')
                                        sleep(2)
                                    else:
                                        username_sesuai = True
                                        try:
                                            registrasiPemilik(con, username, password, nik, nama, no_hp)
                                            print('Registrasi pemilik berhasil.')
                                            print()
                                        except:
                                            print('Registrasi gagal!')
                                            print()
                                        sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)

                elif role == '2':
                    role_dipilih = True
                    inputan_kosong = True

                    while inputan_kosong:
                        username_sesuai = False

                        while not username_sesuai:
                            print()
                            nik = input('NIK: ')
                            nama = input('Nama: ')
                            no_hp = input('Nomor HP: ')
                            username = input('Username: ')
                            password = input('Password: ')

                            if nik!='' or nama!='' or no_hp!='' or username!='' or password!='':
                                inputan_kosong = False
                                pattern = re.compile("^[a-z0-9_.]+$")

                                if not pattern.match(username):
                                    print('Username hanya boleh berupa huruf kecil, angka, underscore, dan titik!')
                                    sleep(2)
                                else:
                                    chosen_role = 'penyewa'
                                    username_sudah_ada = cariUsername(con, chosen_role, username)

                                    if username_sudah_ada:
                                        print('Username sudah terdaftar!')
                                        sleep(2)
                                    else:
                                        username_sesuai = True
                                        try:
                                            registrasiPenyewa(con, username, password, nik, nama, no_hp)
                                            print('Registrasi penyewa berhasil.')
                                            print()
                                        except:
                                            print('Registrasi gagal!')
                                            print()
                                        sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)
                elif role == '0':
                    role_dipilih = True
                elif role == '':
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    sleep(2)
                else:
                    print('Inputan salah! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    sleep(2)
        elif menu_dipilih == '2':
            role_dipilih = False

            print('Login User')

            while not role_dipilih:
                print()
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
                print('0. Kembali')
                role = input('Pilih role [1/2]: ')

                if role == '1':
                    role_dipilih = True
                    inputan_kosong = True

                    while inputan_kosong:
                        login_berhasil = False

                        while not login_berhasil:
                            print()
                            username = input('Username: ')
                            password = input('Password: ')

                            if username!='' or password!='':
                                inputan_kosong = False
                                chosen_role = 'pemilik'
                                username_ditemukan = cariUsername(con, chosen_role, username)

                                if not username_ditemukan:
                                    print(f'Username {username} belum terdaftar!')
                                    sleep(2)
                                else:
                                    password_benar = cekPassword(con, chosen_role, username, password)
                                    
                                    if password_benar:
                                        login_berhasil = True
                                        loggedin_role = chosen_role
                                        loggedin_user = username
                                        print('Berhasil Login.')
                                        print()
                                        sleep(2)
                                        belum_login = dashboard(con, loggedin_user, loggedin_role)
                                    else:
                                        print('Password salah!')
                                        sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)

                elif role == '2':
                    role_dipilih = True
                    inputan_kosong = True

                    while inputan_kosong:
                        login_berhasil = False

                        while not login_berhasil:
                            print()
                            username = input('Username: ')
                            password = input('Password: ')

                            if username!='' or password!='':
                                inputan_kosong = False
                                chosen_role = 'penyewa'
                                username_ditemukan = cariUsername(con, chosen_role, username)

                                if not username_ditemukan:
                                    print(f'Username {username} belum terdaftar!')
                                    sleep(2)
                                else:
                                    password_benar = cekPassword(con, chosen_role, username, password)
                                    
                                    if password_benar:
                                        login_berhasil = True
                                        loggedin_role = chosen_role
                                        loggedin_user = username
                                        print('Berhasil Login.')
                                        print()
                                        sleep(2)
                                        belum_login = dashboard(con, loggedin_user, loggedin_role)
                                    else:
                                        print('Password salah!')
                                        sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)
                elif role == '0':
                    role_dipilih = True
                elif role == '':
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    sleep(2)
                else:
                    print('Inputan salah! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    sleep(2)
        elif menu_dipilih == '3':
            belum_login = False
            print('Program dihentikan...')
            sleep(2)
        else:
            print('Inputan salah! Masukkan angka 1/2/3')
            print()
            sleep(2)
try:
    #membuat koneksi dengan database
    connection = mysql.connector.connect(**db_config)

    #jika berhasil terhubung dengan database
    if connection.is_connected():
        #jalankan program utama
        main(connection)
#jika gagal terhubung dengan database
except mysql.connector.Error as e:
    #print error message
    print(f'Error connecting to mysql: {e}')
#jika semua kodingan try sudah dijalankan dan tidak ada error
finally:
    #jika sudah terhubung dengan database
    if 'connection' in locals() and connection.is_connected():
        #tutup koneksi
        connection.close()
        #print ini
        print('Connection closed')