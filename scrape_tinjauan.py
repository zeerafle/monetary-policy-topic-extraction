from bs4 import BeautifulSoup
import requests
import os

bulan_list = ['Januari', 'Februari', 'Maret', 'April',
              'Mei', 'Juni', 'Juli', 'Agustus',
              'September', 'Oktober', 'November', 'Desember']
tahun_list = [2019, 2020, 2021, 2022]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42"}

if not os.path.exists('teks_laporan'):
    os.makedirs('teks_laporan')

for tahun in tahun_list:
    for bulan in bulan_list:
        filename = f'{str(tahun)}-{bulan}-.txt'
        print(filename)
        if os.path.exists(f'teks_laporan\\tinjauan\\{filename}'):
            continue
        # https://www.bi.go.id/id/publikasi/laporan/Pages/Tinjauan-Kebijakan-Moneter-Februari-2022.aspx
        link = f'https://www.bi.go.id/id/publikasi/laporan/Pages/Tinjauan-Kebijakan-Moneter-{bulan}-{str(tahun)}.aspx'
        webpage = requests.get(link, headers=headers)
        dom = BeautifulSoup(webpage.content, "html.parser")
        text_container = dom.find('div', {'id': 'ctl00_PlaceHolderMain_ctl04__ControlWrapper_RichHtmlField'})
        if text_container is not None:
            text = text_container.text
        else:
            continue

        # hilangkan karakter escape
        escapes_list = [chr(char) for char in range(1, 32)]
        escapes_list.remove(u'\n')  # buang karakter newline dari list
        escapes_list.append(chr(160))  # tambah karakter \xa0
        escapes = ''.join(escapes_list)
        translator = str.maketrans('', '', escapes)
        text = text.translate(translator).strip(u'\u200b')

        # save to file
        with open(os.path.join('teks_laporan', 'tinjauan', filename), 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()

        print(text[1000])
