from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Set backend ke Agg sebelum mengimpor pyplot
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Dictionary untuk mapping kode bidang ke nama lengkap
SUBJECTS = {
    'matematika': 'Matematika',
    'fisika': 'Fisika',
    'kimia': 'Kimia',
    'biologi': 'Biologi',
    'informatika': 'Informatika',
    'astronomi': 'Astronomi',
    'ekonomi': 'Ekonomi',
    'kebumian': 'Kebumian',
    'geografi': 'Geografi'
}

# Data untuk setiap bidang
SUBJECT_DATA = {
    'matematika': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Michael Cenreng', 'SMP Katolik Rajawali', 'SULAWESI SELATAN', '43'],
        ['2', 'I Putu Dickson Partha Hartopo', 'SMPN 3 Denpasar', 'Bali', '35'],
        ['3', 'Ethan Anderson', 'SMP PETRA 1', 'JAWA TIMUR', '32'],
        ['4', 'Ananda Bhakti', 'Little Candle', 'Jawa Barat', '30'],
        ['5', 'Ben Robinson', 'SMP PETRA 1', 'Jawa Timur', '28'],
        ['6', 'Muhammad Irfan Rabbani', 'SMA ABBS Surakarta', 'Jawa Tengah', '28'],
        ['7', 'M. THARIQ AULIA RAHMAN', 'MAS DARUL MURSYID', 'SUMATRA UTARA', '27'],
        ['8', 'Muhammad Allif Qalbiy', 'MAN Insan Cendekia Pekalongan', 'Jawa Tengah', '27'],
        ['9', 'Kenny Wijaya', 'SMA Santa Maria 1 Cirebon', 'Jawa Barat', '25'],
        ['10', 'Alfin Dzakwan Fadhilla', 'SMAN 1 Kota Blitar', 'Jawa Timur', '23'],
        ['11', 'Ahmad Rayhan Faturrifki', 'SMA al-Azhar Mandiri Palu', 'Sulawesi Tengah', '22'],
        ['12', 'Muhammad Widya Tri Atmaja', 'SMA Taruna Nusantara', 'Jawa Tengah', '21'],
        ['13', 'Kelvin Rich Zainal', 'SMA KATOLIK RAJAWALI', 'SULAWESI SELATAN', '18'],
        ['14', 'Muhammad Fauzi Muharam', 'SMP Labschool Cibubur', 'Jawa barat', '18'],
        ['15', 'Fairuz Soraya Hafnidal', 'SMA Al-Adzkar', 'Banten', '18'],
        ['16', 'Trevor Wade Orlando', 'SMA Pradita Dirgantara', 'Jawa Tengah', '17'],
        ['17', 'Muhamad Lukman Hakim', 'SMAN 1 Purwoharjo', 'Jawa Timur', '17'],
        ['18', 'Aldiza Nauval Putra Mulyanto', 'SMP Negeri 27 Jakarta', 'DKI Jakarta', '17'],
        ['19', 'Bayu Reva Nur Mulyadi', 'SMA Negeri 2 Purwakarta', 'Jawa Barat', '16'],
        ['20', 'Jonathan Febrian Kurniawan', 'Smpk 8', 'Jakarta', '16']
    ],
    'fisika': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Fayla Nazilda', 'SMAN 1 Bulukumba', 'Sulawesi Selatan', '23,5'],
        ['2', 'Muthia Izzatul Husna Satriadi', 'SMA MUHAMMADIYAH AHMAD DAHLAN METRO', 'LAMPUNG', '23,5'],
        ['3', 'Ezar Ghazy Amadis', 'SMA Muhammadiyah 1 Pontianak', 'Kalimantan Barat', '23'],
        ['4', 'Yohana Laurensia Br Tarigan', 'SMA NEGERI 5 MEDAN', 'SUMATERA UTARA', '22,5'],
        ['5', 'WILLIAM CHRISTIAN GANI', 'SMAK 1 PENABUR', 'DKI JAKARTA', '22'],
        ['6', 'Sutan Maulana Ismail', 'Nurul Fikri Boarding School Bogor', 'Jawa Barat', '21'],
        ['7', 'Najwa Sabila Aryuda', 'MAN 1 KOTA SEMARANG', 'JAWA TENGAH', '21'],
        ['8', 'Luthfiah Maharani', 'MAN 3 Palembang', 'Sumsel', '21'],
        ['9', 'Nurafiyah Syafa', 'SMA NEGERI 2 PURWAKARTA', 'Jawa Barat', '21'],
        ['10', 'Ria Nurhalijah', 'SMA negeri 1 Bantarujeg', 'Jawa barat', '21'],
        ['11', 'Daniela Amanda Br Ginting', 'SMA KATOLIK RAJAWALI', 'Sulawesi Selatan', '21'],
        ['12', 'Muawanah', 'Sekolah Indonesia Jeddah', 'Makkah', '21'],
        ['13', 'Rainaldy W', 'SMA Zion', 'Sulawesi Selatan', '21'],
        ['14', 'Meilisa Dwi Hanifah', 'SMAN 2 Purwokerto', 'Jawa Tengah', '21'],
        ['15', 'Muhammad Izzan Razin', 'MAN 19 Jakarta', 'DKI Jakarta', '21'],
        ['16', 'CHOIZAH LATHIFATUZ ZAHRO', 'MAN 2 Rembang', 'Jawa tengah', '21'],
        ['17', 'Reza Adi Nurwahid', 'MAN 1 Magelang', 'Jawa Tengah', '21'],
        ['18', 'MITRA PARTOGI', 'SMAN 15 SURABAYA', 'Jawa Timur', '21'],
        ['19', 'Nuri Nuranti', 'Man Bandung barat', 'Jawa barat', '21'],
        ['20', 'Mawar Rafika Fakhira', 'SMAN 1 Ciawi', 'Jawa barat', '21']
    ],
    'kimia': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Putri Nabila Vania N', 'MAN 2 KOTA MALANG', 'JAWA TIMUR', '95'],
        ['2', 'Ezra', 'MAN ICS', 'Banten', '90'],
        ['3', 'Arya Naufal Sihaloho', 'SMAN 1 Jakarta', 'DKI Jakarta', '85'],
        ['4', 'Kriestian Valerio Sugianto', 'SMA Kesatuan Bangsa Yogyakarta', 'D.I Yogyakarta', '69'],
        ['5', 'FAUZAN ATHALLAH FEBRIANSYAH', 'MAN 2 PEKANBARU', 'RIAU', '68'],
        ['6', 'Deandra Rasheesa Maheswari', 'MAN 2 Kota Malang', 'Jawa Timur', '65'],
        ['7', 'Tharfi Thufail Qays Al Hakim', 'SMP Al Muttaqin', 'Jawa Barat', '64'],
        ['8', 'Kaisa Kamila Putri Purnomo', 'MAN 2 Pekanbaru', 'Riau', '62'],
        ['9', 'Anggun Berliana Bandono', 'SMAN 1 Surakarta', 'Jawa Tengah', '61'],
        ['10', 'Nabila Rahma Aisyah', 'MAN 2 Kota Malang', 'Jawa Timur', '57'],
        ['11', 'Muhammad Ainur Ridho Firdausy', 'SMAN 1 Kudus', 'Jawa Tengah', '52'],
        ['12', 'Aryo Razak', 'SMA Katolik Rajawali', 'Sulawesi Selatan', '49'],
        ['13', 'HASBIYALLAH NUR MUHAMMAD', 'SMAS AR ROHMAH DAU', 'Jawa Timur', '48'],
        ['14', 'Baruna Adi Sanjaya', 'SMP Cahaya Rancamaya', 'Jawa Barat', '46'],
        ['15', 'Klarisa Mitzi Tendeanan', 'SMA KATOLIK RAJAWALI', 'Sulawesi Selatan', '43'],
        ['16', 'RIZQ HERSAPUTRA', 'SMAN 5 PURWOKERTO', 'Jawa Tengah', '42'],
        ['17', 'Diva Edenia', 'SMA 1 KUDUS', 'Jawa Tengah', '41'],
        ['18', 'Imam Ropid Alhan Ashari', 'MAN 2 Kota Bengkulu', 'Bengkulu', '40'],
        ['19', 'Radifan Habibul Haqqi', 'SMA Pradita Dirgantara', 'Jawa Tengah', '39'],
        ['20', 'Muhammad Irfan Hanif', 'MAN 2 Kota Malang', 'Jawa Timur', '38']
    ],
    'biologi': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Danish Rafi', 'SMAN 8 Pekanbaru', 'Riau', '156'],
        ['2', 'Nakeisha Jovita Purnomo', 'SMAK Penabur Gading Serpong', 'Banten', '155'],
        ['3', 'Pieter Changcherta', 'Sman 3 banda aceh', 'Aceh', '153'],
        ['4', 'Muhammad Iqbal Maulana Zita', 'MAN 2 Pekanbaru', 'Riau', '152'],
        ['5', 'Labbaika Ziyadul Fikri', 'MAN 2 Kota Malang', 'Jawa Timur', '151'],
        ['6', 'Rafa Darrell Saputra', 'SMA Cendana Pekanbaru', 'Riau', '151'],
        ['7', 'Michiel Aelis Wijaya', 'SMAN 2 JAKARTA', 'DKI Jakarta', '150'],
        ['8', 'Artha Maressa S', 'SMA Sutomo 1 Medan', 'Sumatera Utara', '149'],
        ['9', 'Nauval Rajwaa Raysendria', 'MAN 1 Yogyakarta', 'DIY', '148'],
        ['10', 'Salsa Nabillah Zahira', 'MAN 2 Pekanbaru', 'Riau', '148'],
        ['11', 'Shiva Fauzziyah', 'SMAN 1 Cibadak', 'Jawa Barat', '146'],
        ['12', 'Ni Wayan Pradnyadhari Kusumaputri', 'SMA Negeri 1 Denpasar', 'Bali', '146'],
        ['13', 'Fauzil Azhiim', 'SMAN Modal Bangsa', 'Aceh', '146'],
        ['14', 'Tangkas Eghan Pramudipta', 'SMA N 01 Purwokerto', 'Jawa Tengah', '146'],
        ['15', 'Nisrina Aqilah Mutiallah', 'MAN 2 Kota Malang', 'Jawa Timur', '145'],
        ['16', 'So Ran', 'SMA Global Prestasi', 'Jawa Barat', '145'],
        ['17', 'Ganang Fattahuddien Attar', 'SMA Kesatuan Bangsa', 'DIY', '144'],
        ['18', 'RAHMI MUFIDAH LUBIS', 'MAN 1 MANDAILING NATAL', 'SUMATERA UTARA', '144'],
        ['19', 'Daphne Cheryl Marvella', 'SMA Kristen Petra 2', 'Jawa Timur', '144'],
        ['20', 'Carmelia Carina Halim', 'SMAK PENABUR CIREBON', 'JAWA BARAT', '143']
    ],
    'informatika': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Muhammad Rifqi Ramadhan', 'SMA Unggulan CT Arsa Foundation', 'Sumatera Utara', '150'],
        ['2', 'Muhammad Ricko Pratama', 'SMAN 2 Sampit', 'Kalimantan Tengah', '150'],
        ['3', 'Cut Risfa Zuhra', 'Man 2 Pekanbaru', 'Riau', '130'],
        ['4', 'Diva Dwi Cahyo', 'SMAN CMBBS', 'Banten', '110'],
        ['5', 'Danniel', 'SMAN 1 TUALANG', 'Riau', '110'],
        ['6', 'Joceline Araki', 'SMAK Rajawali', 'Sulawesi Selatan', '90'],
        ['7', 'Sani Muhammad Daveisha Ali', 'SMAN 3 Bogor', 'Jawa Barat', '90'],
        ['8', 'Daffa Rayhan Ananda', 'SMA Semesta Semarang', 'Jawa Tengah', '90'],
        ['9', 'Muhammad Faqih Husain', 'Man Insan Cendekia Pekalongan', 'Jawa Tengah', '90'],
        ['10', 'Muhammad Haidar', 'SMAN 1 Kudus', 'Jawa Tengah', '80'],
        ['11', 'Joe Mathew Rusli', 'SMAN 4 DENPASAR', 'Bali', '80'],
        ['12', 'Nyoman Wiprayanka', 'SMA NEGERI 4 DENPASAR', 'Bali', '80'],
        ['13', 'Giannina Indah Aini', 'MAN 2 Mataram', 'Nusa Tenggara Barat', '80'],
        ['14', 'stanislaus harglen utama', 'SMPK 7 Penabur', 'Jakarta', '80'],
        ['15', 'M. Arvin Wijayanto', 'MAN Insan Cendekia Pekalongan', 'Jawa Tengah', '80'],
        ['16', 'AFDIANA SHAFA NUR KURNIA', 'SMA Negeri 4 Purwokerto', 'Jawa Tengah', '70'],
        ['17', 'Supriyanti', 'SMAN 2 KUDUS', 'Jawa Tengah', '70'],
        ['18', 'ULIL AMRY GHOVARY', 'SMAS AR ROHMAH DAU MALANG', 'JAWA TIMUR', '70'],
        ['19', 'Raihan Maulana Heriandry', 'MAN Insan Cendekia Pekalongan', 'Jawa Tengah', '70'],
        ['20', 'Muhammad Gallan Satria Wirayudha', 'MAN IC Pekalongan', 'Jawa Tengah', '70']
    ],
    'astronomi': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Muhamad Zaky Kurniawan', 'SMAN 1 Pamijahan', 'Jawa Barat', '30'],
        ['2', 'Wanda Kusumawardani', 'SMAN 99 Jakarta', 'DKI Jakarta', '29'],
        ['3', 'Ervan Maulana Ilyas', 'SMA Negeri 1 Babelan', 'Jawa Barat', '29'],
        ['4', 'M. Fadhil Al-Ghani', 'SMA PRADITA DIRGANTARA', 'JAWA TENGAH', '25'],
        ['5', 'Indra Rhamadan', 'SMAN 1 Manggar', 'Kepulauan Bangka Belitung', '23'],
        ['6', 'BAGAS ARYA SAPUTRA', 'SMA NEGERI 2 KUNINGAN', 'JAWA BARAT', '23'],
        ['7', 'Roja Al Afgoni', 'SMAN 2 Purwokerto', 'Jawa Tengah', '22'],
        ['8', 'FAHMI AZIZ FIRMANSYAH', 'SMA AL-KAUTSAR', 'LAMPUNG', '21'],
        ['9', 'Nalendra Ilyasains Kabiro', 'MAN Purbalingga', 'Jawa Tengah', '21'],
        ['10', 'Zahran Nizar Fadhlan', 'SMA Negeri 1 Padang', 'Sumatera Barat', '21'],
        ['11', 'Daffa Muyassar', 'SMAIT NFBS Bogor', 'Jawa Barat', '20'],
        ['12', 'Anugrah Ellysa Widyanasari', 'SMAN 2 Purwokerto', 'Jawa Tengah', '20'],
        ['13', 'TERA WARIH PRANASTI DEWI', 'SMA NEGERI 1 ROWOKELE', 'JAWA TENGAH', '20'],
        ['14', 'Rasendriya Andhika', 'SMAN 11 Bandung', 'Jawa Barat', '20'],
        ['15', 'Lu\'lu\'a Lim\'a Laila', 'MAN 2 Kudus', 'Jawa Tengah', '20'],
        ['16', 'Sesilia Susan Marsela', 'SMAN 1 Maos', 'Jawa Tengah', '20'],
        ['17', 'Rafa Azkiyaul Aula', 'SMAN 1 BUMIAYU', 'Jawa Tengah', '19'],
        ['18', 'ANNIS FAKHIROH AKBAR', 'SMA NEGERI 1 PAMIJAHAN', 'JAWA BARAT', '19'],
        ['19', 'Matthew Wijaya', 'SMAS REGINA PACIS BOGOR', 'Jawa Barat', '18'],
        ['20', 'Anggita Cintya Salsabilla', 'MAN 2 kebumen', 'Jawa tengah', '18']
    ],
    'ekonomi': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Najwa Nafisah Putri', 'MAN 2 Pekanbaru', 'Riau', '80'],
        ['2', 'Vania Wardani', 'MAN 2 Pekanbaru', 'Riau', '75'],
        ['3', 'Naufal Wiwit Putra', 'MAN 2 Kota Malang', 'Jawa Timur', '67,5'],
        ['4', 'Agus Tio Faisal Nizar', 'SMA SEMESTA', 'Jawa Tengah', '67,5'],
        ['5', 'Azrina Rahmah', 'SMA UNGGULAN CT FOUNDATION', 'SUMATERA UTARA', '65'],
        ['6', 'Raisya Tri Cahyani', 'MAN 2 PEKANBARU', 'Riau', '65'],
        ['7', 'Yunita Nurmala Sari', 'MAN 2 Ponorogo', 'Jawa Timur', '62,5'],
        ['8', 'Shakila Azwa Siregar', 'MAN Insan Cendekia Pekalongan', 'Jawa Tengah', '62,5'],
        ['9', 'Lusiana Andini', 'SMAK Penabur Cirebon', 'Jawa Barat', '62,5'],
        ['10', 'Rosalia Rifka Az-Zulfa', 'SMA 1 Trenggalek', 'Jawa Timur', '57,5'],
        ['11', 'Cindy Octavia', 'SMAN 1 MANGGAR', 'Kepulauan Bangka Belitung', '57,5'],
        ['12', 'Hugo Sanyes Praja Sinaga', 'SMAN 3 Tarutung', 'Sumatera Utara', '57,5'],
        ['13', 'Tabina Febiana Kartika Dewi', 'SMA AL-ABIDIN BILINGUAL BOARDING SCHOOL', 'Jawa Tengah', '57,5'],
        ['14', 'Zaira Novelia', 'MAN 2 PEKANBARU', 'Riau', '57,5'],
        ['15', 'Salsabila Inayah Zahra', 'MAN 2 Pekanbaru', 'Riau', '55'],
        ['16', 'Delfi Rahmadini', 'MAN 2 Pekanbaru', 'Riau', '55'],
        ['17', 'Muhammad Faiz Zuhdi Supandi', 'SMA AL ADZKAR', 'Banten', '52,5'],
        ['18', 'Martinus Evan Aristianto', 'SMAS Katolik Mater Dei', 'Banten', '52,5'],
        ['19', 'Chika Tsaabitah Dinaranti', 'SMAN 1 PURI', 'Jawa Timur', '52,5'],
        ['20', 'Amelia Dewi Kartika', 'MAN 2 KLATEN', 'Jawa Tengah', '52,5']
    ],
    'kebumian': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'Nisa Kamila Ramadhani', 'SMA IT Insan Cendekia Payakumbuh', 'Sumatra Barat', '247'],
        ['2', 'Aysha Chansanatha Briant', 'SMA IT Insan Cendekia Payakumbuh', 'Sumatra Barat', '193'],
        ['3', 'Dewi Fortuna Ananda Rudhi', 'SMAN 1 Cibadak', 'Jawa Barat', '142'],
        ['4', 'Dita Ayu Fitriyasari', 'SMAN 2 Purwokerto', 'Jawa Tengah', '137'],
        ['5', 'Saifurrohman Ar Robbani', 'MAN Insan Cendekia Pasuruan', 'Jawa timur', '135'],
        ['6', 'Reksa Okta Ramadhan', 'Man Insan Cendekia Jambi', 'Jambi', '134'],
        ['7', 'Canigias Alliyah Pearly Tri Gunawan', 'SMAN 1 Cibadak', 'Jawa Barat', '134'],
        ['8', 'Fatimah Dwi Adila Azzahro', 'MAN Insan Cendekia Serpong', 'DKI Jakarta', '132'],
        ['9', 'Nathanda Shafira Caroline', 'MAN INSAN CENDEKIA JAMBI', 'JAMBI', '129'],
        ['10', 'Ammara Shifa Andini', 'MAN 2 Kota Malang', 'Jawa Timur', '126'],
        ['11', 'Muhammad Nurul Huda', 'MAN 1 KOTA KEDIRI', 'Jawa Timur', '124'],
        ['12', 'Celline Tania Wijaya', 'SMA Kristen Petra 2', 'Jawa Timur', '122'],
        ['13', 'Hafzulh Usmu Alfalah', 'MAN Insan Cendekia Jambi', 'Jambi', '119'],
        ['14', 'USAMAH HISYAM FATHONI', 'MAN 1 SEMARANG', 'Jawa Tengah', '119'],
        ['15', 'Aqiela Dini Lestari', 'MAN 2 CILACAP', 'Jawa Tengah', '117'],
        ['16', 'ALMUZAKY ABROR', 'Man 3 pekanbaru', 'Riau', '116'],
        ['17', 'Edellouisa Josephin', 'SMA 7 PSKD DEPOK', 'JAWA BARAT', '115'],
        ['18', 'Qatrunnada Nisrina Indari', 'MAN 1 Rembang', 'Jawa Tengah', '115'],
        ['19', 'Ashila Nafi Tsabitha', 'SMAN 1 Batusangkar', 'Sumatera Barat', '114'],
        ['20', 'Kevin Andreas', 'SMA DARMA YUDHA', 'Riau', '113']
    ],
    'geografi': [
        ['Rank', 'Nama', 'Sekolah', 'Provinsi', 'Nilai'],
        ['1', 'ICHA DWI ANGGITA', 'SMAN 2 Purwokerto', 'Jawa Tengah', '231'],
        ['2', 'Nicolas Yap', 'SMAN 34 Jakarta', 'DKI Jakarta', '203'],
        ['3', 'irfannesa jesse candraningtyas', 'Kesatuan Bangsa', 'Yogyakarta', '200'],
        ['4', 'Andi Nabil Fauzan', 'SMAN 1 KOTA GORONTALO', 'GORONTALO', '198'],
        ['5', 'Rahmat Sigit Prasetyo', 'SMA Semesta', 'Jawa Tengah', '195'],
        ['6', 'Razan Na\'ilah Nur Zahrah', 'SMAN 1 SOKARAJA', 'JAWA TENGAH', '192'],
        ['7', 'Retno Azqa Saputra', 'SMAN 1 SOKARAJA', 'Jawa Tengah', '188'],
        ['8', 'RAYHANS NUR AMYAN SYAFII', 'SMA NEGERI 1 SOKARAJA', 'JAWA TENGAH', '185'],
        ['9', 'Khairi Yudhistira Nugraha', 'SMAN 2 PURWOKERTO', 'Jawa tengah', '184'],
        ['10', 'Muhammad Keisya Jirjis Al Hakim', 'MAN IC PEKALONGAN', 'Jawa Tengah', '182'],
        ['11', 'Desvara Arifina Zens', 'SMA N 1 SOKARAJA', 'Jawa Tengah', '180'],
        ['12', 'Natasha Filia Kutamso', 'SMAN 1 Tualang', 'Riau', '180'],
        ['13', 'Aisyah Nur Aini', 'SMAN 1 Teras', 'Jawa Tengah', '180'],
        ['14', 'Satrio Bagus Pamungkas', 'SMA 1 Sokaraja', 'Jawa Tengah', '176'],
        ['15', 'DIKA ALFA REZA', 'SMAN 1 WANGON', 'JAWA TENGAH', '173'],
        ['16', 'SASTA AURELYA MECCA', 'SMAN 1 WANGON', 'JAWA TENGAH', '171'],
        ['17', 'ASTRIA DINA FITRI', 'SMA NEGERI 1 WANGON', 'JAWA TENGAH', '171'],
        ['18', 'Marsa Nur Kholilah', 'MAN 1 Kota Semarang', 'Jawa Tengah', '170'],
        ['19', 'EKA ERINA SURYANI', 'SMA N 1 BOBOTSARI', 'JAWA TENGAH', '169'],
        ['20', 'DWI ARDIANTI PUTRI', 'SMAN 9 KOTA BEKASI', 'Jawa Barat', '169']
    ]
}

def get_subject_data(subject):
    """Mendapatkan data untuk bidang tertentu"""
    subject_data = []
    raw_data = SUBJECT_DATA.get(subject, [])
    
    if not raw_data:
        return []
    
    # Skip header row
    for row in raw_data[1:]:
        score = float(row[4].replace(',', '.'))
        subject_data.append({
            'rank': row[0],
            'nama': row[1],
            'sekolah': row[2],
            'provinsi': row[3],
            'nilai': score
        })
    return subject_data

def calculate_statistics(data):
    """Menghitung statistik dasar"""
    
    # Ekstrak nilai
    values = [d['nilai'] for d in data]
    n = len(values)
    
    # Urutkan nilai
    sorted_values = sorted(values)
    
    # Statistik dasar
    min_val = min(values)
    max_val = max(values)
    mean = sum(values) / n
    
    # Median
    if n % 2 == 0:
        median = (sorted_values[n//2-1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]
    
    # Standar deviasi
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = variance ** 0.5
    
    # Kuartil
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    q1 = sorted_values[q1_idx]
    q3 = sorted_values[q3_idx]
    
    # Modus
    value_counts = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1
    mode = max(value_counts.items(), key=lambda x: x[1])[0]
    
    # Distribusi frekuensi
    class_width = (max_val - min_val) / 5  # 5 kelas
    freq_dist = []
    cumulative_freq = 0
    
    for i in range(5):
        class_start = min_val + (i * class_width)
        class_end = class_start + class_width
        frequency = len([x for x in values if class_start <= x < class_end])
        relative_freq = (frequency / n) * 100
        cumulative_freq += frequency
        
        freq_dist.append({
            'class_range': f"{class_start:.1f}-{class_end:.1f}",
            'frequency': frequency,
            'relative_frequency': relative_freq,
            'cumulative_frequency': cumulative_freq
        })
    
    return {
        'n': n,
        'min': min_val,
        'max': max_val,
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'q1': q1,
        'q3': q3,
        'mode': mode,
        'frequency_distribution': freq_dist,
        'sorted_data': sorted_values
    }

def create_stem_leaf_plot(data):
    """Membuat stem and leaf plot"""
    # Bersihkan plot sebelumnya
    plt.close('all')
    
    # Buat figure baru
    fig, ax = plt.subplots(figsize=(10, 6))
    
    values = [d['nilai'] for d in data]
    
    # Pisahkan stem dan leaf
    stems = []
    leaves = []
    for value in sorted(values):
        stem = int(value // 10)
        leaf = int(value % 10)
        stems.append(stem)
        leaves.append(leaf)
    
    # Buat plot
    ax.stem(stems, leaves)
    ax.set_title('Stem and Leaf Plot')
    ax.set_xlabel('Stem')
    ax.set_ylabel('Leaf')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return base64.b64encode(buf.getvalue()).decode()

def create_histogram(data):
    """Membuat histogram"""
    # Bersihkan plot sebelumnya
    plt.close('all')
    
    # Buat figure baru
    fig, ax = plt.subplots(figsize=(10, 6))
    
    values = [d['nilai'] for d in data]
    
    # Buat histogram
    ax.hist(values, bins=5, edgecolor='black')
    ax.set_title('Histogram')
    ax.set_xlabel('Nilai')
    ax.set_ylabel('Frekuensi')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return base64.b64encode(buf.getvalue()).decode()

def create_box_plot(data):
    """Membuat box plot"""
    # Bersihkan plot sebelumnya
    plt.close('all')
    
    # Buat figure baru
    fig, ax = plt.subplots(figsize=(10, 6))
    
    values = [d['nilai'] for d in data]
    
    # Buat box plot
    ax.boxplot(values)
    ax.set_title('Box Plot')
    ax.set_ylabel('Nilai')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/')
def home():
    subject = request.args.get('subject', 'matematika')
    current_subject = subject.lower()
    
    try:
        # Dapatkan data untuk bidang yang dipilih
        subject_data = get_subject_data(current_subject)
        
        if not subject_data:
            return render_template('home.html',
                                error="No data found for the selected subject",
                                current_subject=current_subject,
                                subjects=SUBJECTS)
        
        # Hitung statistik
        statistics = calculate_statistics(subject_data)
        
        # Buat visualisasi
        stem_leaf_plot = create_stem_leaf_plot(subject_data)
        histogram = create_histogram(subject_data)
        box_plot = create_box_plot(subject_data)
        
        return render_template('home.html',
                             statistics=statistics,
                             current_subject=current_subject,
                             subjects=SUBJECTS,
                             table_data=subject_data,
                             stem_leaf_plot=stem_leaf_plot,
                             histogram=histogram,
                             box_plot=box_plot)
                             
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('home.html',
                             error=str(e),
                             current_subject=current_subject,
                             subjects=SUBJECTS)

if __name__ == '__main__':
    app.run(debug=True) 
