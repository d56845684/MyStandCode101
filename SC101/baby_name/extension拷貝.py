"""
File: extension.py
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10890537
Female Number: 7939153
---------------------------
2000s
Male Number: 12975692
Female Number: 9207577
---------------------------
1990s
Male Number: 14145431
Female Number: 10644002
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s' , '2000s', '1990s']:
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        targets = soup.find_all("table", {'class': "t-stripe"})
        total_male_number = 0
        total_female_number = 0
        for target in targets:
            list_total = target.tbody.text             # 得到全部的名子+數量
            with open("test.txt", "w") as f:           # 先全部寫入txt
                f.write(list_total)
        with open("test.txt", "r") as k:                # 讀取檔案
            for line in k:
                data = line.split()
                if len(data) == 4:
                    total_male_number += int(data[1].replace(",", ""))
                    total_female_number += int(data[3].replace(",", ""))
        print('---------------------------')
        print(year)
        print(f"Male number: {total_male_number}")
        print(f"Female number: {total_female_number}")


if __name__ == '__main__':
    main()
