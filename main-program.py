#libraries yang digunakan
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

#fungsi untuk registrasi pemilik
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

#fungsi untuk registrasi penyewa
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

#fungsi untuk mengecek apakah username sudah terdaftar atau belum
def cariUsername(con, role, inputan_username):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca username dari database
    select_query = f'SELECT username FROM {role}'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua username ke dalam variabel usernames
    usernames = cursor.fetchall()

    #baca setiap username
    for username in usernames:
        #jika username ditemukan di database
        if username == (inputan_username,):
            #kembalikan nilai True
            return True

    #jika username tidak ditemukan di database    
    #kembalikan nilai False
    return False

#fungsi untuk mengecek apakah inputan password sudah sesuai dengan username
def cekPassword(con, role, inputan_username, inputan_password):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca password dari database
    select_query = f'SELECT password FROM {role} where username="{inputan_username}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan password ke dalam variabel passwords
    passwords = cursor.fetchall()

    #baca setiap password
    for password in passwords:
        #jika password yang diinputkan user benar
        if password == (inputan_password,):
            #kembalikan nilai True
            return True

    #jika password yang diinputkan user salah    
    #kembalikan nilai False
    return False

#fungsi untuk menampilkan data motor berbentuk dataframe
def readMotor(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca data motor milik pemilik
        select_query = f'SELECT plat_nomor, merek, tipe, sewa_perhari FROM motor where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca data semua motor
        select_query = f'SELECT plat_nomor, merek, tipe, sewa_perhari FROM motor'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    #dictionary untuk menyimpan data motor
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

    #print dataframe
    print(pd.DataFrame(motor_dict))

#fungsi untuk mengecek apakah plat nomor sudah terdaftar atau belum
def cariPlatnomor(con, inputan_platnomor, id_pemilik=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    if id_pemilik=='':
        #query sql untuk membaca semua plat nomor yang terdaftar
        select_query = f'SELECT plat_nomor FROM motor'
    else:
        #query sql untuk membaca semua plat nomor milik pemilik
        select_query = f'SELECT plat_nomor FROM motor WHERE id_pemilik="{id_pemilik}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel plats
    plats = cursor.fetchall()

    #baca setiap plat nomor
    for plat_nomor in plats:
        #jika plat nomor ditemukan di database
        if plat_nomor == (inputan_platnomor.upper(),):
            #kembalikan string plat nomor
            return inputan_platnomor.upper()

    #jika plat nomor tidak ditemukan di database
    #kembalikan nilai False
    return False

#fungsi untuk menambah motor
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

#fungsi untuk memperbarui data motor
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

#fungsi untuk hapus motor
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

#fungsi untuk membaca semua data penyewaan
def readPenyewaan(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca semua data penyewaan milik penyewa
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca semua data penyewaan milik pemilik
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan WHERE id_penyewa="{username}"'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    #dictionary untuk menyimpan data penyewaan
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

    #hitung total biaya sewa
    for i in range(len(rows)):
        #jika motor sudah dikembalikan
        if penyewaan_dict['Tgl Pengembalian'][i]:
            #inisialisasi tanggal penyewaan
            tgl_penyewaan = penyewaan_dict['Tgl Penyewaan'][i]
            #inisialisasi tanggal pengembalian
            tgl_pengembalian = penyewaan_dict['Tgl Pengembalian'][i]
            #hitung total hari dari mulai tanggal penyewaan hingga tanggal pengembalian
            total_hari = int((np.datetime64(tgl_pengembalian) - np.datetime64(tgl_penyewaan))/np.timedelta64(1,'D'))
            #jika motor sudah dikembalikan kurang dari sehari
            if total_hari<1:
                #maka total biaya = biaya sewa perhari
                biaya = penyewaan_dict['Sewa Perhari'][i]
            #jika motor dikembalikan minimal sehari
            else:
                #maka total biaya = total hari dikali biaya sewa perhari
                biaya = total_hari * penyewaan_dict['Sewa Perhari'][i]
            #masukkan biaya yang sudah dihitung ke penyewaan_dict
            penyewaan_dict['Biaya'][i] = biaya

    #print dataframe penyewaan
    print(pd.DataFrame(penyewaan_dict))

#fungsi untuk menampilkan 3 motor yang paling sering disewa
def showTop3Rented(con, role, username=''):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #jika yang login adalah pemilik
    if role == 'pemilik':
        #query sql untuk membaca semua data penyewaan milik pemilik
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan where id_pemilik="{username}"'
    #jika yang login adalah penyewa
    else:
        #query sql untuk membaca semua data penyewaan
        select_query = f'SELECT id_penyewaan, tgl_penyewaan, tgl_pengembalian, plat_nomor, merek_motor, tipe_motor, sewa_perhari FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    #dictionary untuk menyimpan semua plat nomor
    penyewaan_dict = {
        'Plat Nomor': [],
    }

    #masukkan semua plat nomor ke dictionary penyewaan_dict
    for i in range(len(rows)):
        penyewaan_dict['Plat Nomor'].append(rows[i][3])

    #buat dataframe dari dictionary penyewaan_dict
    df = pd.DataFrame(penyewaan_dict)
    #hitung frekuensi plat nomor
    frequencies = df['Plat Nomor'].value_counts()

    #ambil dua plat nomor yang paling sering digunakan
    top_two_plates = frequencies.head(3)

    #buat grafik batang
    plt.bar(top_two_plates.index, top_two_plates.values)
    plt.xlabel('Motor')
    plt.ylabel('Frekuensi')
    plt.title('Top 3 Motor Paling Sering Disewa')
    plt.show()

#fungsi untuk mencari apakah id penyewaan ada di tabel penyewaan
def cariIdPenyewaanDiPenyewaan(con, inputan_idpenyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca semua id penyewaan dari tabel penyewaan
    select_query = f'SELECT id_penyewaan FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua id penyewaan ke dalam variabel penyewaan_ids
    penyewaan_ids = cursor.fetchall()

    #baca setiap id penyewaan
    for id_penyewaan in penyewaan_ids:
        #jika id penyewaan ditemukan di tabel penyewaan
        if f'{id_penyewaan}' == f'({inputan_idpenyewaan},)':
            #kembalikan nilai id penyewaan
            return inputan_idpenyewaan

    #jika plat nomor tidak ditemukan di database
    #kembalikan nilai False
    return False

#fungsi untuk mencari id penyewaan di tabel pengembalian
def cariIdPenyewaanDiPengembalian(con, inputan_idpenyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca semua id penyewaan dari tabel pengembalian
    select_query = f'SELECT id_penyewaan FROM pengembalian'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua id penyewaan ke dalam variabel penyewaan_ids
    penyewaan_ids = cursor.fetchall()

    #baca setiap id penyewaan
    for id_penyewaan in penyewaan_ids:
        #jika id penyewaan ditemukan di tabel penyewaan
        if f'{id_penyewaan}' == f'({inputan_idpenyewaan},)':
            #kembalikan nilai id penyewaan
            return inputan_idpenyewaan

    #jika id penyewaan tidak ditemukan di tabel penyewaan
    #kembalikan nilai False    
    return False

#fungsi untuk mengambil elemen-elemen dari sebuah motor
def getMotorElements(con, inputan_platnomor):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca semua data motor
    select_query = f'SELECT plat_nomor,merek,tipe,sewa_perhari,id_pemilik FROM motor'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data motor ke dalam variabel motors
    motors = cursor.fetchall()

    #array untuk menampung elemen-elemen sebuah motor
    motor_items = []

    #baca setiap data motor
    for motor in motors:
        #jika plat nomor ditemukan di database
        if motor[0] == inputan_platnomor.upper():
            #baca setiap elemen dari sebuah data motor
            for item in motor:
                #masukkan masing-masing elemen ke motor_items
                motor_items.append(item)
            #kembalikan array yang sudah terisi dengan elemen-elemen dari sebuah motor
            return motor_items

    #jika plat nomor tidak ditemukan di database
    #kembalikan nilai False
    return False

#fungsi untul sewa motor
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

#fungsi untuk menginisialisasi tgl_pengembalian di tabel penyewaan ketika motor dikembalikan
def setTglPengembalian(con, id_penyewaan, tgl_pengembalian):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk update data di database
    update_query = 'UPDATE penyewaan SET tgl_pengembalian=%s WHERE id_penyewaan=%s'

    #data yang digunakan pada query
    value = (tgl_pengembalian, id_penyewaan)

    #replace data di database
    cursor.execute(update_query, value)

    #simpan perubahan
    con.commit()

#fungsi untuk mengambil elemen-elemen dari sebuah penyewaan
def getPenyewaanElements(con, id_penyewaan):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca semua data penyewaan dari tabel penyewaan
    select_query = f'SELECT id_penyewaan,plat_nomor,tgl_penyewaan FROM penyewaan'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data penyewaan ke dalam variabel penyewaans
    penyewaans = cursor.fetchall()

    #array untuk menampung elemen-elemen sebuah penyewaan
    penyewaan_items = []

    #baca setiap data penyewaan
    for penyewaan in penyewaans:
        #jika id penyewaan ditemukan di database
        if f'{penyewaan[0]}' == f'{id_penyewaan}':
            #baca setiap elemen dari sebuah data panyewaan
            for item in penyewaan:
                #masukkan masing-masing elemen penyewaan ke penyewaan_items
                penyewaan_items.append(item)
            #kembalikan array yang sudah terisi dengan elemen-elemen dari sebuah penyewaan
            return penyewaan_items

    #jika id penyewaan tidak ditemukan di database
    #kembalikan nilai False    
    return False

#fungsi untuk mengembalikan motor
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

#fungsi dashboard pemilik dan penyewa
def dashboard(con, loggedin_user, loggedin_role):
    #selagi user sudah login
    while loggedin_user != '':
        #jika yang login adalah pemilik
        if loggedin_role == 'pemilik':
            #print data-data motor milik pemilik
            print('Daftar Motor')
            readMotor(con, loggedin_role, loggedin_user)
            print()
            #print data-data penyewaan dari motor-motor si pemilik
            print('Transaksi Penyewaan')
            readPenyewaan(con, loggedin_role, loggedin_user)
            print()

            #aksi-aksi yang bisa dilakukan pemilik
            print('Aksi:')
            print('1. Tambah Motor')
            print('2. Update Motor')
            print('3. Delete Motor')
            print('4. Kembalikan Motor')
            print('5. Tampilkan motor yang paling sering disewa')
            print('6. Logout')
            #inputan aksi
            aksi_dipilih = input('Pilih aksi [1-5]: ')

            #jika aksi yang dipilih adalah tambah  motor
            if aksi_dipilih == '1':
                #status inputan masih kosong
                inputan_kosong = True

                #selagi inputan masih kosong
                while inputan_kosong:
                    #status inputan belum sesuai
                    inputan_sesuai = False

                    #selagi inputan belum selesai
                    while not inputan_sesuai:
                        print()
                        #inputan-inputan informasi motor
                        plat_nomor = input('Plat Nomor: ')
                        merek = input('Merek Motor: ')
                        tipe = input('Tipe Motor: ')
                        sewa_perhari = input('Sewa Perhari: Rp')
                        id_pemilik = loggedin_user

                        #jika semua inputan diisi
                        if plat_nomor!='' or merek!='' or tipe!='' or sewa_perhari!='':
                            #inputan sudah tidak kosong
                            inputan_kosong = False
                            #cari plat nomor di database
                            platnomor_sudah_ada = cariPlatnomor(con, plat_nomor)
                            
                            #jika plat nomor ada di database
                            if platnomor_sudah_ada:
                                #print ini
                                print('Plat nomor sudah terdaftar!')
                                #jeda 2 detik
                                sleep(2)
                            #jika plat nomor tidak ada di database
                            else:
                                #regex untuk validasi inputan plat nomor
                                pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z]$')

                                #jika inputan plat nomor tidak sesuai regex
                                if not pattern.match(plat_nomor):
                                        #print ini
                                        print('Plat motor hanya diawali dan diakhiri oleh huruf dan hanya boleh mengandung huruf, angka, dan spasi!')
                                        #jeda 2 detik
                                        sleep(2)
                                #jika inputan plat nomor sudah sesuai regex
                                else:
                                    #jika inputan sewa perhari bukan integer
                                    if not sewa_perhari.isdigit():
                                        #print ini
                                        print('Sewa perhari hanya boleh bilangan integer!')
                                    #jika inputan sewa perhari adalah integer
                                    else:
                                        #inputan sudah sesuai
                                        inputan_sesuai = True
                                        try:
                                            #jalankan fungsi tambahMotor() dengan inputan-inputan informasi motor sebagai argumen
                                            tambahMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik)
                                            #print ini
                                            print('Tambah motor berhasil.')
                                            #buat baris baru
                                            print()
                                        except:#jika ada error
                                            #print ini
                                            print('Tambah motor gagal!')
                                            #buat baris baru
                                            print()
                                    #jeda 2 detik
                                    sleep(2)
                        #jika inputan ada yang kosong
                        else:
                            #print ini
                            print('Inputan tidak boleh kosong!')
                            #jeda 2 detik
                            sleep(2)
            #jika aksi yang dipilih adalah update motor
            elif aksi_dipilih == '2':
                #status plat nomor belum ketemu
                platnomor_ketemu = False

                #selagi plat nomor belum ketemu
                while not platnomor_ketemu:
                    #buat baris baru
                    print()
                    #inputan plat nomor
                    plat_nomor = input('Masukkan plat nomor: ')
                    #cari plat nomor yang diinputkan apakah ada di database
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor, loggedin_user)

                    #jika plat nomor ada di database
                    if platnomor_ketemu:
                        #status inputan masih kosong
                        inputan_kosong = True

                        #selagi inputan masih kosong
                        while inputan_kosong:
                            #status inputan belum sesuai
                            inputan_sesuai = False

                            #selagi inputan belum sesuai
                            while not inputan_sesuai:
                                #buat baris baru
                                print()
                                #inputkan informasi motor yang ingin diperbarui
                                plat_nomor = input('Plat Nomor: ')
                                merek = input('Merek Motor: ')
                                tipe = input('Tipe Motor: ')
                                sewa_perhari = input('Sewa Perhari: Rp')
                                id_pemilik = loggedin_user

                                #jika semua inputan diisi
                                if plat_nomor!='' or merek!='' or tipe!='' or sewa_perhari!='':
                                    #inputan sudah tidak kosong
                                    inputan_kosong = False
                                    #cari apakah plat nomor yang diinputkan ada di database
                                    platnomor_sudah_ada = cariPlatnomor(con, plat_nomor)

                                    #jika plat nomor sudah ada di database dan bukan plat nomor sebelumnya
                                    if platnomor_sudah_ada and (plat_nomor.upper()!=platnomor_ketemu):
                                        #print ini
                                        print('Plat nomor sudah terdaftar!')
                                        #jeda 2 detik
                                        sleep(2)
                                    #jika plat nomor tidak ada di database
                                    else:
                                        #regex untuk validasi plat nomor
                                        pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z]$')

                                        #jika inputan plat nomor tidak sesuai regex
                                        if not pattern.match(plat_nomor):
                                            #print ini
                                            print('Plat motor hanya diawali dan diakhiri oleh huruf dan hanya boleh mengandung huruf, angka, dan spasi!')
                                            #jeda 2 detik
                                            sleep(2)
                                        #jika inputan plat nomor sudah sesuai regex
                                        else:
                                            #jika inputan sewa perhari bukan integer
                                            if not sewa_perhari.isdigit():
                                                print('Sewa perhari hanya boleh bilangan integer!')
                                            else:
                                                #status inputan sudah sesuai
                                                inputan_sesuai = True
                                                try:
                                                    #update informasi motor sesuai dengan yang diinputkan user
                                                    updateMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik)
                                                    #print ini
                                                    print('Update motor berhasil.')
                                                    #buat baris baru
                                                    print()
                                                except:#jika ada error
                                                    #print ini
                                                    print('Update motor gagal!')
                                                    #buat baris baru
                                                    print()
                                            #jeda 2 detik
                                            sleep(2)
                                #jika inputan ada yang kosong
                                else:
                                    #print ini
                                    print('Inputan tidak boleh kosong!')
                                    #jeda 2 detik
                                    sleep(2)
                    #jika plat nomor yang diinputkan belum terdaftar
                    else:
                        #print ini
                        print(f'Plat nomor {plat_nomor} tidak terdaftar!')
                        #jeda 2 detik
                        sleep(2)
            #jika aksi yang dipilih adalah hapus motor
            elif aksi_dipilih == '3':
                #status plat nomor belum ketemu
                platnomor_ketemu = False

                #selagi plat nomor belum ketemu
                while not platnomor_ketemu:
                    #inputan plat nomor
                    plat_nomor = input('Masukkan plat nomor: ')
                    #cari plat nomor yang diinputkan apakah ada di database
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor, loggedin_user)

                    #jika plat nomor ketemu
                    if platnomor_ketemu:
                        try:
                            #hapus motor berplat nomor tersebut
                            hapusMotor(con, plat_nomor, loggedin_user)
                            #print ini
                            print('Hapus motor berhasil.')
                            #buat baris baru
                            print()
                        except:#jika ada error
                            #print ini
                            print('Hapus motor gagal!')
                            #buat baris baru
                            print()
                        #jeda 2 detik
                        sleep(2)
                    #jika plat nomor tidak terdapat di database
                    else:
                        #print ini
                        print(f'Plat nomor {plat_nomor} tidak terdaftar!')
                        #jeda 2 detik
                        sleep(2)
            #jika aksi yang dipilih adalah kembalikan motor
            elif aksi_dipilih == '4':
                #buat baris baru
                print()
                #inputan id penyewaan
                id_penyewaan = input('Masukkan id penyewaan: ')

                #jika id penyewaan yang diinputkan ditemukan di tabel penyewaan tapi tidak ada di tabel pengembalian
                if cariIdPenyewaanDiPenyewaan(con, id_penyewaan) and (not cariIdPenyewaanDiPengembalian(con, id_penyewaan)):
                    #ambil elemen-elemen penyewaan
                    penyewaan_elements = getPenyewaanElements(con, id_penyewaan)
                    #seperti plat nomor
                    plat_nomor = penyewaan_elements[1]
                    #dan tanggal penyewaan
                    tgl_penyewaan = penyewaan_elements[2]

                    try:
                        #atur tanggal hari ini untuk tanggal pengembalian
                        current_GMT = time.gmtime()
                        ts = calendar.timegm(current_GMT)
                        date_time = datetime.datetime.fromtimestamp(ts)
                        str_date_time = date_time.strftime("%Y-%m-%d")

                        #inisialisasi tanggal pengembalian di tabel penyewaan dari id penyewaan tersebut
                        setTglPengembalian(con, id_penyewaan, str_date_time)
                        #insert data baru ke tabel pengembalian
                        kembalikanMotor(con, id_penyewaan, plat_nomor, tgl_penyewaan, str_date_time)
                        #print ini
                        print('Motor berhasil dikembalikan!')
                        #buat baris baru
                        print()
                        #jeda 2 detik
                        sleep(2)
                    except:#jika ada error
                        #print ini
                        print('Motor gagal dikembalikan!')
                        #buat baris baru
                        print()
                        #jeda 2 detik
                        sleep(2)
                #jika id penyewaan tidak ada di tabel penyewaan atau ada di tabel pengembalian
                else:
                    #print ini
                    print('Id penyewaan tidak ketemu atau motor sudah dikembalikan!')
                    #buat baris baru
                    print()
                    #jeda 2 detik
                    sleep(2)
            #jika aksi yang dipilih adalah menampilkan top 3 motor milik pemilik paling sering disewa
            elif aksi_dipilih == '5':
                #tampilkan grafik batang
                showTop3Rented(con, loggedin_role, loggedin_user)
            #jika aksi yang dipilih adalah logout
            elif aksi_dipilih == '6':
                #keluarkan user
                loggedin_user = ''
                #print ini
                print('Logout berhasil.')
                #buat baris baru
                print()
                #jeda 2 detik
                sleep(2)
                #kembalikan nilai True
                return True
            #jika user asal input aksi
            else:
                #print ini
                print('Inputan salah! Masukkan angka 1-5!')
                #buat baris baru
                print()
                #jeda 2 detik
                sleep(2)
        #jika yang login adalah penyewa
        else:
            #jika penyewa masih login
            while loggedin_user !='':
                #print data-data motor yang ada
                print('Daftar Motor')
                readMotor(con, loggedin_role, loggedin_user)
                print()
                #print data-data penyewaan dari motor-motor si penyewa
                print('Transaksi Penyewaan')
                readPenyewaan(con, loggedin_role, loggedin_user)
                print()

                #aksi-aksi yang bisa dilakukan penyewa
                print('Aksi:')
                print('1. Sewa Motor')
                print('2. Tampilkan motor yang paling sering disewa')
                print('3. Logout')
                #inputan aksi
                aksi_dipilih = input('Pilih aksi [1/2]: ')

                #jika aksi yang dipilih adalah sewa motor
                if aksi_dipilih == '1':
                    #buat baris baru
                    print()
                    #inputan plat nomor
                    plat_nomor = input('Plat Nomor: ')
                    
                    #cari apakah plat nomor yang diinputkan ada di database
                    platnomor_ketemu = cariPlatnomor(con, plat_nomor)

                    #jika plat nomor ada di database
                    if platnomor_ketemu:
                        #ambil elemen-elemen motor
                        motor_elements = getMotorElements(con, plat_nomor)
                        #seperti merek motor
                        merek = motor_elements[1]
                        #tipe motor
                        tipe = motor_elements[2]
                        #biaya sewa perhari
                        sewa_perhari = motor_elements[3]
                        #dan id pemilik
                        id_pemilik = motor_elements[4]

                        try:
                            #atur tanggal hari ini untuk tanggal pengembalian
                            current_GMT = time.gmtime()
                            ts = calendar.timegm(current_GMT)
                            date_time = datetime.datetime.fromtimestamp(ts)
                            str_date_time = date_time.strftime("%Y-%m-%d")

                            #insert data baru ke tabel penyewaan
                            sewaMotor(con, str_date_time, plat_nomor, merek, tipe, sewa_perhari, id_pemilik, loggedin_user)
                            #print ini
                            print('Sewa motor berhasil!')
                            #buat baris baru
                            print()
                            #jeda 2 detik
                            sleep(2)
                        except:#jika ada error
                            #print ini
                            print('Sewa motor gagal!')
                            #buat baris baru
                            print()
                            #jeda 2 detik
                            sleep(2)
                #jika aksi yang dipilih adalah menampilkan top 3 motor paling sering disewa
                elif aksi_dipilih == '2':
                    #tampilkan grafik batang
                    showTop3Rented(con, loggedin_role)
                #jika aksi yang dipilih adalah logout 
                elif aksi_dipilih == '3':
                    #keluarkan user
                    loggedin_user = ''
                    #print ini
                    print('Logout berhasil.')
                    #buat baris baru
                    print()
                    #jeda 2 detik
                    sleep(2)
                    #kembalikan nilai True
                    return True
                #jika user asal input aksi
                else:
                    #print ini
                    print('Inputan salah! Masukkan angka 1 atau 2!')
                    #buat baris baru
                    print()
                    #jeda 2 detik
                    sleep(2)

#fungsi program utama
def main(con):
    #status user belum login
    belum_login = True
    loggedin_user = ''
    loggedin_role = ''

    #selagi user belum login
    while belum_login:
        #menu awal
        print('Menu')
        print('1. Register')
        print('2. Login')
        print('3. Hentikan Program')
        #inputan menu
        menu_dipilih = input('Pilih menu [1/2]: ')

        #jika menu yang dipilih adalah register
        if menu_dipilih == '1':
            #status role belum dipilih
            role_dipilih = False

            #print ini
            print('Registrasi User')

            #selagi role belum dipilih
            while not role_dipilih:
                #buat baris baru
                print()
                #role yang bisa dipilih
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
                print('0. Kembali')
                #inputan role
                role = input('Pilih role [1/2]: ')

                #jika role yang dipilih adalah pemilik
                if role == '1':
                    #status role sudah dipilih
                    role_dipilih = True
                    #status inputan masih kosong
                    inputan_kosong = True
                    
                    #selagi inputan masih kosong
                    while inputan_kosong:
                        #status username belum sesuai
                        username_sesuai = False

                        #selagi username belum sesuai
                        while not username_sesuai:
                            #buat baris baru
                            print()
                            #inputan informasi pemilik
                            nik = input('NIK: ')
                            nama = input('Nama: ')
                            no_hp = input('Nomor HP: ')
                            username = input('Username: ')
                            password = input('Password: ')

                            #jika inputan diisi semua
                            if nik!='' or nama!='' or no_hp!='' or username!='' or password!='':
                                #status inputan sudah tidak kosong
                                inputan_kosong = False
                                #regex untuk validasi username
                                pattern = re.compile("^[a-z0-9_.]+$")

                                #jika inputan username tidak sesuai regex
                                if not pattern.match(username):
                                    #print ini
                                    print('Username hanya boleh berupa huruf kecil, angka, underscore, dan titik!')
                                    #jeda 2 detik
                                    sleep(2)
                                #jika inputan username sudah sesuai regex
                                else:
                                    #inisialisasi role yang dipilih sebagai pemilik
                                    chosen_role = 'pemilik'
                                    #cari apakah username yang diinputkan ada di tabel pemilik
                                    username_sudah_ada = cariUsername(con, chosen_role, username)

                                    #jika username ada di tabel pemilik
                                    if username_sudah_ada:
                                        #print ini
                                        print('Username sudah terdaftar!')
                                        #jeda 2 detik
                                        sleep(2)
                                    #jika username tidak ada di tabel pemilik
                                    else:
                                        #status username sudah sesuai
                                        username_sesuai = True
                                        try:
                                            #buat pemilik baru menggunakan informasi yang diinputkan user
                                            registrasiPemilik(con, username, password, nik, nama, no_hp)
                                            #print ini
                                            print('Registrasi pemilik berhasil.')
                                            #buat baris baru
                                            print()
                                        except:#jika ada error
                                            #print ini
                                            print('Registrasi gagal!')
                                            #buat baris baru
                                            print()
                                        #jeda 3 detik
                                        sleep(2)
                            #jika inputan ada yang kosong
                            else:
                                print('Inputan tidak boleh kosong!')
                                #jeda 2 detik
                                sleep(2)
                #jika role yang dipilih adalah penyewa
                elif role == '2':
                    #status role sudah dipilih
                    role_dipilih = True
                    #status inputan masih kosong
                    inputan_kosong = True

                    #selagi inputan masih kosong
                    while inputan_kosong:
                        #status username belum sesuai
                        username_sesuai = False

                        #selagi username belum sesuai
                        while not username_sesuai:
                            #buat baris baru
                            print()
                            #inputan informasi penyewa
                            nik = input('NIK: ')
                            nama = input('Nama: ')
                            no_hp = input('Nomor HP: ')
                            username = input('Username: ')
                            password = input('Password: ')

                            #jika inputan diisi semua
                            if nik!='' or nama!='' or no_hp!='' or username!='' or password!='':
                                #status inputan sudah tidak kosong
                                inputan_kosong = False
                                #regex untuk validasi inputan username
                                pattern = re.compile("^[a-z0-9_.]+$")
                                #jika inputan username tidak sesuai regex
                                if not pattern.match(username):
                                    #print ini
                                    print('Username hanya boleh berupa huruf kecil, angka, underscore, dan titik!')
                                    #jeda 2 detik
                                    sleep(2)
                                #jika inputan username sudah sesuai regex
                                else:
                                    #inisialisasi role yang dipilih sebagai penyewa
                                    chosen_role = 'penyewa'
                                    #cari apakah username yang diinputkan ada di tabel penyewa
                                    username_sudah_ada = cariUsername(con, chosen_role, username)

                                    #jika username ada di tabel penyewa
                                    if username_sudah_ada:
                                        #print ini
                                        print('Username sudah terdaftar!')
                                        #jeda 2 detik
                                        sleep(2)
                                    #jika username tidak ada di tabel penyewa
                                    else:
                                        #status username sudah sesuai
                                        username_sesuai = True

                                        try:
                                            #buat penyewa baru menggunakan informasi yang diinputkan user
                                            registrasiPenyewa(con, username, password, nik, nama, no_hp)
                                            #print ini
                                            print('Registrasi penyewa berhasil.')
                                            #buat baris baru
                                            print()
                                        except:#jika ada error
                                            #print ini
                                            print('Registrasi gagal!')
                                            #buat baris baru
                                            print()
                                        #jeda 2 detik
                                        sleep(2)
                            #jika ada inputan yang kosong
                            else:
                                #print ini
                                print('Inputan tidak boleh kosong!')
                                #jeda 2 detik
                                sleep(2)
                #jika user memilih kembali ke menu sebelumnya
                elif role == '0':
                    #kembali ke menu sebelumnya
                    role_dipilih = True
                #jika inputan role kosong
                elif role == '':
                    #print ini
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    #jeda 2 detik
                    sleep(2)
                #jika user asal input role
                else:
                    #print ini
                    print('Inputan salah! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    #jeda 2 detik
                    sleep(2)
        #jika menu yang dipilih adalah login
        elif menu_dipilih == '2':
            #status role belum dipilih
            role_dipilih = False

            #print ini
            print('Login User')

            #selagi role belum dipilih
            while not role_dipilih:
                #buat baris
                print()
                #role yang bisa dipilih
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
                print('0. Kembali')
                #inputan role
                role = input('Pilih role [1/2]: ')

                #jika role yang dipilih adalah pemilik
                if role == '1':
                    #status role sudah dipilih
                    role_dipilih = True
                    #status inputan masih kosong
                    inputan_kosong = True

                    #selagi inputan masih ada yang kosong
                    while inputan_kosong:
                        #status belum berhasil login
                        login_berhasil = False

                        #selagi belum berhasil login
                        while not login_berhasil:
                            #buat baris baru
                            print()
                            #inputan username
                            username = input('Username: ')
                            #inputan password
                            password = input('Password: ')

                            #jika inputan username dan password diisi semua
                            if username!='' or password!='':
                                #status inputan sudah tidak kosong
                                inputan_kosong = False
                                #inisialisasi role yang dipilih sebagai pemilik
                                chosen_role = 'pemilik'
                                #cari apakah username yang diinputkan ada di tabel pemilik
                                username_ditemukan = cariUsername(con, chosen_role, username)

                                #jika username tidak ada di tabel pemilik
                                if not username_ditemukan:
                                    #print ini
                                    print(f'Username {username} belum terdaftar!')
                                    #jeda 2 detik
                                    sleep(2)
                                #jika username ada di tabel pemilik
                                else:
                                    #cek apakah password yang diinputkan sudah benar
                                    password_benar = cekPassword(con, chosen_role, username, password)
                                    
                                    #jika password sudah benar
                                    if password_benar:
                                        #status login berhasil
                                        login_berhasil = True
                                        #inisialiasi role pemilik yang sedang login
                                        loggedin_role = chosen_role
                                        #inisialisasi username pemilik yang sedang login
                                        loggedin_user = username
                                        #print ini
                                        print('Berhasil Login.')
                                        #buat baris baru
                                        print()
                                        #jeda 2 detik
                                        sleep(2)
                                        #jalankan dashboard pemilik
                                        belum_login = dashboard(con, loggedin_user, loggedin_role)
                                    #jika password salah
                                    else:
                                        #print ini
                                        print('Password salah!')
                                        #jeda 2 detik
                                        sleep(2)
                            #jika inputan username atau password ada yang kosong
                            else:
                                #print ini
                                print('Inputan tidak boleh kosong!')
                                #jeda 2 detik
                                sleep(2)
                #jika role yang dipilih adalah penyewa
                elif role == '2':
                    #status role sudah dipilih
                    role_dipilih = True
                    #status inputan masih kosong
                    inputan_kosong = True

                    #selagi inputan masih kosong
                    while inputan_kosong:
                        #status login belum berhasil
                        login_berhasil = False

                        #selagi login belum berhasil
                        while not login_berhasil:
                            #buat baris baru
                            print()
                            #inputan username
                            username = input('Username: ')
                            #inputan password
                            password = input('Password: ')
                            
                            #jika inputan username dan password diisi semua
                            if username!='' or password!='':
                                #status inputan sudah tidak kosong
                                inputan_kosong = False
                                #inisialisasi role yang dipilih sebagai penyewa
                                chosen_role = 'penyewa'
                                #cari apakah username yang diinputkan ada di tabel penyewa
                                username_ditemukan = cariUsername(con, chosen_role, username)

                                #jika username tidak ada di tabel penyewa
                                if not username_ditemukan:
                                    #print ini
                                    print(f'Username {username} belum terdaftar!')
                                    #jeda 2 detik
                                    sleep(2)
                                #jika username ada di tabel penyewa
                                else:
                                    #cek apakah password yang diinputkan benar
                                    password_benar = cekPassword(con, chosen_role, username, password)
                                    
                                    #jika password benar
                                    if password_benar:
                                        #status login berhasil
                                        login_berhasil = True
                                        #inisialisasi role penyewa yang sedang login
                                        loggedin_role = chosen_role
                                        #inisialisasi username pemilik yang sedang login
                                        loggedin_user = username
                                        #print ini
                                        print('Berhasil Login.')
                                        #buat baris baru
                                        print()
                                        #jeda 2 detik
                                        sleep(2)
                                        #jalankan dashboard penyewa
                                        belum_login = dashboard(con, loggedin_user, loggedin_role)
                                    #Jika password salah
                                    else:
                                        #print ini
                                        print('Password salah!')
                                        #jeda 2 detik
                                        sleep(2)
                            #jika inputan username atau password ada yang kosong
                            else:
                                #print ini
                                print('Inputan tidak boleh kosong!')
                                #jeda 2 detik
                                sleep(2)
                #jika memilih kembali ke menu sebelumnya
                elif role == '0':
                    #kembali ke menu sebelumnya
                    role_dipilih = True
                #jika inputan role kosong
                elif role == '':
                    #print ini
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    #jeda 2 detik
                    sleep(2)
                #jika user asal input role
                else:
                    #print ini
                    print('Inputan salah! Masukkan 1 untuk pemilik, 2 untuk penyewa, atau 0 untuk kembali.')
                    #jeda 2 detik
                    sleep(2)
        #jika menu yang dipilih adalah hentikan program
        elif menu_dipilih == '3':
            #hentikan program
            belum_login = False
            #print ini
            print('Program dihentikan...')
            #jeda 2 detik
            sleep(2)
        #jika user asal input
        else:
            #print ini
            print('Inputan salah! Masukkan angka 1/2/3')
            #buat baris baru
            print()
            #jeda 2 detik
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