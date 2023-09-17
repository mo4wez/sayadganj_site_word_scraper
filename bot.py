import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from models.model import WordBook, db
import re
import logging
from lets.letters import letters

class GetWord:
    driver_path = '.\driver\chromedriver.exe'

    def __init__(self):
        self.driver = self._setup_driver()
        self.url = 'https://sayadganj.netlify.app/'

    def run(self):
        self.get_words()


    def _setup_driver(self):
        driver = webdriver.Chrome(service=Service(executable_path=self.driver_path))
        return driver

    def get_words(self):

        self.driver.get(self.url)
        sleep(1)

        # letters = self.driver.find_elements(By.XPATH, "//a[@class='cursor-pointer p-5 text-2xl border border-gray-300 rounded-md shadow dark:border-gray-700 sm:p-2 md:p-1']")

        for letter in letters:
            word_list_url = f'https://sayadganj.netlify.app/search/{letter}'
            self.driver.get(word_list_url)
            sleep(1)
            
            result_quantity = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='text-center text-2xl p-5 text-gray-800 dark:text-gray-200']/p")
                )
            ).text
            numeric_value = int(re.search(r'\d+', result_quantity).group())
            print(f'{numeric_value} records found.')

            for item in range(1, numeric_value + 1):
                try:
                    xpath = f"//div[@class='dark:bg-gray-800 cursor-pointer relative overflow-hidden items-center min-w-[50vw] w-[90vw] tracking-wider leading-10 m-2 p-4 max-w-sm rounded-lg border dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-800 border-gray-300 shadow-md'][{item}]"

                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, xpath)
                        )
                    )
                    title = element.find_element(By.TAG_NAME, 'h1').text
                    description = element.find_element(By.TAG_NAME, 'p').text

                    word = WordBook.create(
                        full_word=title,
                        full_word_with_symbols=title,
                        definition=description,
                    )
                    word.save()
                    print(f'{item} saved')
                    sleep(1)
                
                except Exception as e:
                    print("Error:" + e)

            self.driver.get(self.url)
            print(f'{item} item saved.')



if __name__ == '__main__':
    gw = GetWord()
    gw.run()
