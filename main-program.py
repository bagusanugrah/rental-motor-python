import mysql.connector
import re
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
        select_query = f'SELECT plat_nomor, merek, tipe, sewa_perhari FROM motor"'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua data ke dalam variabel rows
    rows = cursor.fetchall()

    print('no (plat_nomor, merek, tipe, sewa_perhari)')

    #print semua row
    for i in range(len(rows)):
        print(f'{i+1} {rows[i]}')

def cariPlatnomor(con, inputan_platnomor):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()

    #query sql untuk membaca plat nomor dari database
    select_query = f'SELECT plat_nomor FROM motor'

    #jalankan query
    cursor.execute(select_query)

    #simpan semua plat nomor ke dalam variabel rows
    plats = cursor.fetchall()

    #print semua row
    for plat_nomor in plats:
        #jika plat nomor ditemukan di database
        if plat_nomor == (inputan_platnomor,):
            return True

    #jika plat nomor tidak ditemukan di database    
    return False

def tambahMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik):
    #membuat cursor untuk berinteraksi dengan database
    cursor = con.cursor()
    #query sql untuk insert data ke database
    insert_query = 'INSERT INTO motor (plat_nomor, merek, tipe, sewa_perhari, id_pemilik) VALUES (%s, %s, %s, %s, %s)'

    #data yang akan dimasukkan ke database
    value = (plat_nomor, merek, tipe, sewa_perhari, id_pemilik)

    #masukkan data ke database
    cursor.execute(insert_query, value)

    #simpan perubahan
    con.commit()

def main(con):
    belum_login = True
    loggedin_user = ''
    loggedin_role = ''

    while belum_login:
        print()
        print('Menu')
        print('1. Register')
        print('2. Login')
        menu_dipilih = input('Pilih menu [1/2]: ')

        if menu_dipilih == '1':
            role_dipilih = False

            print('Registrasi User')

            while not role_dipilih:
                print()
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
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
                                    choosen_role = 'pemilik'
                                    username_sudah_ada = cariUsername(con, choosen_role, username)

                                    if username_sudah_ada:
                                        print('Username sudah terdaftar!')
                                        sleep(2)
                                    else:
                                        username_sesuai = True
                                        try:
                                            registrasiPemilik(con, username, password, nik, nama, no_hp)
                                            print('Registrasi pemilik berhasil.')
                                        except:
                                            print('Registrasi gagal!')
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
                                    choosen_role = 'penyewa'
                                    username_sudah_ada = cariUsername(con, choosen_role, username)

                                    if username_sudah_ada:
                                        print('Username sudah terdaftar!')
                                        sleep(2)
                                    else:
                                        username_sesuai = True
                                        try:
                                            registrasiPenyewa(con, username, password, nik, nama, no_hp)
                                            print('Registrasi penyewa berhasil.')
                                        except:
                                            print('Registrasi gagal!')
                                        sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)
                elif role == '':
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik dan 2 untuk penyewa.')
                    sleep(2)
                else:
                    print('Inputan salah! Masukkan 1 untuk pemilik dan 2 untuk penyewa.')
                    sleep(2)
        elif menu_dipilih == '2':
            role_dipilih = False

            print('Login User')

            while not role_dipilih:
                print()
                print('Role')
                print('1. Pemilik')
                print('2. Penyewa')
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
                                choosen_role = 'pemilik'
                                username_ditemukan = cariUsername(con, choosen_role, username)

                                if not username_ditemukan:
                                    print(f'Username {username} belum terdaftar!')
                                    sleep(2)
                                else:
                                    password_benar = cekPassword(con, choosen_role, username, password)
                                    
                                    if password_benar:
                                        login_berhasil = True
                                        belum_login = False
                                        loggedin_role = choosen_role
                                        loggedin_user = username
                                        print('Berhasil Login.')
                                        print()
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
                                choosen_role = 'penyewa'
                                username_ditemukan = cariUsername(con, choosen_role, username)

                                if not username_ditemukan:
                                    print(f'Username {username} belum terdaftar!')
                                    sleep(2)
                                else:
                                    password_benar = cekPassword(con, choosen_role, username, password)
                                    
                                    if password_benar:
                                        login_berhasil = True
                                        belum_login = False
                                        loggedin_role = choosen_role
                                        loggedin_user = username
                                        print('Berhasil Login.')
                                        print()
                                    else:
                                        print('Password salah!')
                                    sleep(2)
                            else:
                                print('Inputan tidak boleh kosong!')
                                sleep(2)
                elif role == '':
                    print('Inputan role tidak boleh kosong! Masukkan 1 untuk pemilik dan 2 untuk penyewa.')
                    sleep(2)
                else:
                    print('Inputan salah! Masukkan 1 untuk pemilik dan 2 untuk penyewa.')
                    sleep(2)

    while loggedin_user != '':
        #jika yang login adalah pemilik
        if loggedin_role == 'pemilik':
            readMotor(con, loggedin_role, loggedin_user)

            print('Aksi:')
            print('1. Tambah Motor')
            print('2. Update Motor')
            print('3. Delete Motor')
            print('4. Lihat Motor yang direntalkan')
            print('5. Logout')
            aksi_dipilih = input('Pilih aksi [1-3]: ')

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

                            if not sewa_perhari.isdigit():
                                print('Sewa perhari hanya boleh bilangan integer!')
                                sleep(2)
                            else:
                                platnomor_sudah_ada = cariPlatnomor(con, username)

                                if platnomor_sudah_ada:
                                    print('Plat nomor sudah terdaftar!')
                                    sleep(2)
                                else:
                                    username_sesuai = True
                                    try:
                                        tambahMotor(con, plat_nomor, merek, tipe, sewa_perhari, id_pemilik)
                                        print('Tambah motor berhasil.')
                                    except:
                                        print('Tambah motor gagal!')
                                    sleep(2)
                        else:
                            print('Inputan tidak boleh kosong!')
                            sleep(2)
            elif aksi_dipilih == '2':
                pass
            elif aksi_dipilih == '3':
                pass
            else:
                pass
        #jika yang login adalah penyewa
        else:
            readMotor(con, loggedin_role, loggedin_user)
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