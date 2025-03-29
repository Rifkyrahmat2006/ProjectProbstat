from flask import Flask, render_template, request
import csv
import os
import math
import matplotlib
matplotlib.use('Agg')  # Set backend ke Agg sebelum mengimpor pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# Dictionary untuk mapping nama bidang
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

def read_csv_data(subject):
    """Membaca data dari file CSV sesuai bidang"""
    data = []
    try:
        # Tentukan nama file berdasarkan bidang
        filename = f"data/{subject.capitalize()}.csv"
        print(f"Reading file: {filename}")
        
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                # Bersihkan data dari whitespace
                row = [cell.strip() for cell in row]
                if any(cell for cell in row):  # Hanya tambahkan baris yang tidak kosong
                    data.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        raise
    return data

def get_subject_data(data, subject):
    """Mendapatkan data untuk bidang tertentu"""
    subject_data = []
    count = 0  # Counter untuk membatasi jumlah data
    
    print(f"\nProcessing data for subject: {subject}")
    
    # Skip header row
    for row in data[1:]:  # Mulai dari baris kedua (setelah header)
        if count >= 20:  # Batasi hanya 20 data
            print(f"Reached maximum data limit (20)")
            break
            
        if not row or len(row) < 5:  # Skip baris kosong atau tidak lengkap
            print(f"Skipping invalid row: {row}")
            continue
            
        try:
            # Debug: print nilai sebelum konversi
            print(f"Processing row: {row}")
            print(f"Score before conversion: {row[4]}")
            
            score = float(row[4].replace(',', '.'))
            print(f"Score after conversion: {score}")
            
            subject_data.append({
                'rank': row[0],
                'nama': row[1],
                'sekolah': row[2],
                'provinsi': row[3],
                'nilai': score
            })
            count += 1  # Increment counter
            print(f"Successfully added data. Count: {count}")
        except (ValueError, IndexError) as e:
            print(f"Error processing row: {e}")
            print(f"Problematic row: {row}")
            continue
    
    print(f"Total data collected: {len(subject_data)}")
    return subject_data

def calculate_statistics(data):
    """Menghitung statistik dasar"""
    if not data:
        return None
    
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
    std_dev = math.sqrt(variance)
    
    # Kuartil
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    q1 = sorted_values[q1_idx]
    q3 = sorted_values[q3_idx]
    
    # Skewness
    skewness = sum((x - mean) ** 3 for x in values) / (n * std_dev ** 3)
    
    # Kurtosis
    kurtosis = sum((x - mean) ** 4 for x in values) / (n * std_dev ** 4) - 3
    
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
        'skewness': skewness,
        'kurtosis': kurtosis,
        'mode': mode,
        'frequency_distribution': freq_dist,
        'sorted_data': sorted_values
    }

def create_stem_leaf_plot(data):
    """Membuat stem and leaf plot"""
    plt.clf()  # Clear figure
    plt.figure(figsize=(10, 6))
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
    plt.stem(stems, leaves)
    plt.title('Stem and Leaf Plot')
    plt.xlabel('Stem')
    plt.ylabel('Leaf')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode()

def create_histogram(data):
    """Membuat histogram"""
    plt.clf()  # Clear figure
    plt.figure(figsize=(10, 6))
    values = [d['nilai'] for d in data]
    
    # Buat histogram
    sns.histplot(values, bins=5)
    plt.title('Histogram')
    plt.xlabel('Nilai')
    plt.ylabel('Frekuensi')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode()

def create_box_plot(data):
    """Membuat box plot"""
    plt.clf()  # Clear figure
    plt.figure(figsize=(10, 6))
    values = [d['nilai'] for d in data]
    
    # Buat box plot
    sns.boxplot(y=values)
    plt.title('Box Plot')
    plt.ylabel('Nilai')
    
    # Simpan plot ke buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/')
def home():
    subject = request.args.get('subject', 'matematika')
    current_subject = subject.lower()
    
    try:
        # Baca data dari file CSV yang sesuai
        print(f"\n=== Starting data processing for subject: {current_subject} ===")
        data = read_csv_data(current_subject)
        print(f"Total rows in CSV: {len(data)}")
        
        # Dapatkan data untuk bidang yang dipilih
        subject_data = get_subject_data(data, current_subject)
        print(f"Found {len(subject_data)} rows for subject {current_subject}")
        
        if not subject_data:
            print("WARNING: No data found for the selected subject!")
        
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

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True) 