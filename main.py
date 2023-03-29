import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os.path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="идёт загрузка. не вызывайте команду ещё раз пока не придёт расписание на следующий день.\nВажно, NaN значит пусто.")
    d = datetime.date.today()
    dd = d.day + 1
    if dd == 32:
        dd = 1
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
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(result_column))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="бот под лицензией GNU. всем доступен и открыт. https://github.com/boroveen/mmt")

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
