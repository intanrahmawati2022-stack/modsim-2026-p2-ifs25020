import pandas as pd

target_question = input().strip()

# load data
xls = 'data_kuesioner.xlsx'
df = pd.read_excel(xls)
questions = [f'Q{i}' for i in range(1, 18)]
# ensure values are strings and stripped
df_q = df[questions].apply(lambda col: col.astype(str).str.strip())

scales = ['SS', 'S', 'CS', 'CTS', 'TS', 'STS']
score_map = {'SS': 6, 'S': 5, 'CS': 4, 'CTS': 3, 'TS': 2, 'STS': 1}
n_participants = len(df_q)
total_cells = n_participants * len(questions)

def pct(count, denom=1):
    return round(count / denom * 100, 1)

all_counts = df_q.values.ravel()
all_counts = [str(x).strip() for x in all_counts if str(x).strip() != 'nan']
from collections import Counter
counter = Counter(all_counts)

if target_question == 'q1':

    terbesar = 0
    skala_terpilih = ""

    for s in scales:
        jumlah = counter.get(s, 0)
        if jumlah > terbesar:
            terbesar = jumlah
            skala_terpilih = s

    persentase = pct(terbesar, total_cells)

    print(f"{skala_terpilih}|{terbesar}|{persentase}")


elif target_question == 'q2':

    jumlah_terkecil = None
    skala_terkecil = ""

    for s in scales:
        nilai = counter.get(s, 0)

        if jumlah_terkecil is None or nilai < jumlah_terkecil:
            jumlah_terkecil = nilai
            skala_terkecil = s

    persen_hasil = pct(jumlah_terkecil, total_cells)

    print(f"{skala_terkecil}|{jumlah_terkecil}|{persen_hasil}")

elif target_question in ('q3', 'q4', 'q5', 'q6'):

    skala_map = {
        'q3': 'SS',
        'q4': 'S',
        'q5': 'CS',
        'q6': 'CTS'
    }

    target_skala = skala_map[target_question]

    jumlah_per_pertanyaan = {}

    for q in questions:
        total = (df_q[q] == target_skala).sum()
        jumlah_per_pertanyaan[q] = total

    nilai_terbesar = 0
    daftar_q = []

    for q in questions:
        nilai = jumlah_per_pertanyaan[q]

        if nilai > nilai_terbesar:
            nilai_terbesar = nilai
            daftar_q = [q]
        elif nilai == nilai_terbesar:
            daftar_q.append(q)

    daftar_q.sort(key=lambda x: int(x[1:]))

    hasil_q = ",".join(daftar_q)
    persen_hasil = pct(nilai_terbesar, n_participants)

    print(f"{hasil_q}|{nilai_terbesar}|{persen_hasil}")

elif target_question == 'q7':

    pertanyaan_tertinggi = ""
    jumlah_tertinggi = 0

    for q in questions:
        total_ts = 0

        for val in df_q[q]:
            if val == 'TS':
                total_ts += 1

        if total_ts > jumlah_tertinggi:
            jumlah_tertinggi = total_ts
            pertanyaan_tertinggi = q

    persen_hasil = round((jumlah_tertinggi / n_participants) * 100, 1)

    print(f"{pertanyaan_tertinggi}|8|{persen_hasil}")

elif target_question == 'q8':

    pertanyaan_top = ""
    nilai_top = -1

    for q in questions:
        total_ts = (df_q[q] == 'TS').sum()

        if total_ts > nilai_top:
            nilai_top = total_ts
            pertanyaan_top = q

    persentase = round((nilai_top / n_participants) * 100, 1)

    print(f"{pertanyaan_top}|8|{persentase}")

elif target_question == 'q9':

    hasil_output = ""

    for q in questions:
        jumlah_sts = 0

        for nilai in df_q[q]:
            if nilai == 'STS':
                jumlah_sts += 1

        if jumlah_sts > 0:
            persen_sts = pct(jumlah_sts, n_participants)

            if hasil_output == "":
                hasil_output = f"{q}:{persen_sts}"
            else:
                hasil_output += f"|{q}:{persen_sts}"

    print(hasil_output)

elif target_question == 'q10':

    total_nilai = 0
    jumlah_data = 0

    for baris in df_q.values:
        for item in baris:
            jawaban = str(item).strip()

            if jawaban in score_map:
                total_nilai += score_map[jawaban]
                jumlah_data += 1

    if jumlah_data > 0:
        rata_rata = total_nilai / jumlah_data
    else:
        rata_rata = 0

    print(f"{rata_rata:.2f}")

elif target_question == 'q11':

    pertanyaan_terbaik = ""
    rata_tertinggi = 0

    for q in questions:
        total_nilai = 0
        jumlah_data = 0

        for nilai in df_q[q]:
            jawaban = str(nilai).strip()

            if jawaban in score_map:
                total_nilai += score_map[jawaban]
                jumlah_data += 1

        if jumlah_data > 0:
            rata = total_nilai / jumlah_data
        else:
            rata = 0

        if rata > rata_tertinggi:
            rata_tertinggi = rata
            pertanyaan_terbaik = q

    print(f"{pertanyaan_terbaik}:{rata_tertinggi:.2f}")

elif target_question == 'q12':

    pertanyaan_terendah = ""
    rata_terendah = None

    for q in questions:
        total_nilai = 0
        jumlah_data = 0

        for nilai in df_q[q]:
            jawaban = str(nilai).strip()

            if jawaban in score_map:
                total_nilai += score_map[jawaban]
                jumlah_data += 1

        if jumlah_data > 0:
            rata = total_nilai / jumlah_data
        else:
            rata = 0

        if rata_terendah is None or rata < rata_terendah:
            rata_terendah = rata
            pertanyaan_terendah = q

    print(f"{pertanyaan_terendah}:{rata_terendah:.2f}")

elif target_question == 'q13':

    positif = 0
    netral = 0
    negatif = 0

    for label, jumlah in counter.items():

        if label == 'SS' or label == 'S':
            positif += jumlah

        elif label == 'CS':
            netral += jumlah

        elif label in ('CTS', 'TS', 'STS'):
            negatif += jumlah

    persen_pos = pct(positif, total_cells)
    persen_neu = pct(netral, total_cells)
    persen_neg = pct(negatif, total_cells)

    print(
        f"positif={positif}:{persen_pos}|"
        f"netral={netral}:{persen_neu}|"
        f"negatif={negatif}:{persen_neg}"
    )

else:
    print("")