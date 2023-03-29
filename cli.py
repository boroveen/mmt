import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os.path

d = datetime.date.today()
dd = d.day + 1
raspisanieday = str(dd)
print(raspisanieday)

search = "https://msk-murman.ru/main/studentam/raspisanie"

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get(search)
raspisanie = driver.find_element(By.LINK_TEXT, raspisanieday)
zzzz = raspisanie.get_attribute('href')

driver.close()
print(zzzz)

command = "wget -O raspisanie.xlsx " + zzzz
os.system(command)

file = "raspisanie.xlsx"
try:
    df = pd.read_excel(file, sheet_name=0)
    search_value = "0521-11-1"
    row_index = df.loc[df.iloc[:, 3] == search_value].index[0]
    result_column = df.iloc[4:12, row_index]
    print(f"Столбец с индексами 4-11:\n{result_column}")
except IndexError:
    print("Значение не найдено")

os.system("rm raspisanie.xlsx")
