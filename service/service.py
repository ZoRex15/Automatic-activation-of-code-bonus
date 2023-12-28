import time
import ffmpeg
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from seleniumwire import webdriver
from fake_useragent import UserAgent
import speech_recognition as sr
from selenium.webdriver import Keys


name_audio_file = 'audio_file.mp3'

def write_audio(url):
    response = requests.get(url)
    with open(f'{name_audio_file}', 'wb') as file:
        file.write(response.content)

def audio_to_text(name_audio_file):
    with open(f'{name_audio_file}', 'rb') as files:
        path_to_mp3 = name_audio_file
        path_to_wav = 'audio_file_wav.wav'
        sound = ffmpeg.input(path_to_mp3)
        sound = ffmpeg.output(sound, path_to_wav)
        ffmpeg.run(sound)
        sample_audio = sr.AudioFile(path_to_wav)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
            key = r.recognize_google(audio, show_all=True)
            return key['alternative'][0]['transcript']

def set_code(code: str) -> None:
    options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=C:\Users\Станислав\AppData\Local\Google\Chrome\User Data')
    with webdriver.Chrome(chrome_options=options) as browser:
        browser.get('https://zooma6.casino/affilates')
        browser.implicitly_wait(10)
        
        browser.find_element(By.CSS_SELECTOR, 'input[id="activatePromoName2023_3"]').send_keys(code)
        

        # #переключение на iframe капчи
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='reCAPTCHA']")))

        # #клик по чекбоксу капчи
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]'))).click()
        browser.implicitly_wait(10)

        # возвращаемся к основному контексту веб-страницы.
        browser.switch_to.default_content()

        #Ожидаем доступность iframe и кликаем по готовности
        #iframe с набором картинок
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='текущую проверку reCAPTCHA можно пройти в течение ещё двух минут']")))

        # Ожидаем кликабельность кнопки с аудио
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-audio-button"]'))).click()

        #Находим тег аудио по ID и излекаем содержимое атрибута src
        src = browser.find_element(By.ID, "audio-source").get_attribute("src")
        print(f"[INFO] Audio src: {src}")
        write_audio(src)
        

        browser.find_element(By.CSS_SELECTOR, 'input[id="audio-response"]').send_keys(audio_to_text(name_audio_file))
        browser.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)

        #Переключаемся обратно на основной контент страницы
        browser.switch_to.default_content()
        # WebDriverWait(browser, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="activatePromo"]'))).click()
        time.sleep(1.5)
        browser.find_element(By.CSS_SELECTOR, 'input[id="activatePromo"]').click()
        browser.quit()
   