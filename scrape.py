from bs4 import BeautifulSoup
import requests
import os

triwulan_list = ['I', 'II', 'III', 'IV']
tahun_list = [2019, 2020, 2021, 2022]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

if not os.path.exists('teks_laporan'):
    os.makedirs('teks_laporan')

for tahun in tahun_list:
    for triwulan in triwulan_list:
        filename = f'triwulan-{triwulan}-{tahun}.txt'
        filepath = os.path.join('teks_laporan', 'laporan', filename)
        print(f'checking triwulan {triwulan} tahun {tahun}')
        if os.path.exists(filepath):
            print(filename, 'exist')
            continue
        # https://www.bi.go.id/id/publikasi/laporan/Pages/Laporan-Kebijakan-Moneter-Triwulan-II-2022.aspx
        link = f'https://www.bi.go.id/id/publikasi/laporan/Pages/Laporan-Kebijakan-Moneter-Triwulan-{triwulan}-{str(tahun)}.aspx'
        webpage = requests.get(link)
        dom = BeautifulSoup(webpage.content, "html.parser")
        text = dom.find('div', {'id': 'ctl00_PlaceHolderMain_ctl04__ControlWrapper_RichHtmlField'}).text

        # hilangkan karakter escape
        escapes_list = [chr(char) for char in range(1, 32)]
        escapes_list.remove(u'\n')  # buang karakter newline dari list
        escapes_list.append(chr(160))  # tambah karakter \xa0
        escapes = ''.join(escapes_list)
        translator = str.maketrans('', '', escapes)
        text = text.translate(translator).strip(u'\u200b')

        # save to file
        filename = f'triwulan-{triwulan}-{str(tahun)}.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()

        print(text)
