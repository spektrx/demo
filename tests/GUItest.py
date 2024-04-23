from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# В отличии от UNIT теста, ваш сайт должен быть запущен!
# сейчас тест написан так, что-бы выполнялся как можно быстрее, но вы можете везде поставить time.sleep(1), что бы всё рассмотреть

driver = webdriver.Chrome() # Используем драйвер от Chrome. вы можете использовать только браузеры с ядром Chromium (Яндекс, Firefox, Edge), можно как-то запустить на сафари, но я хз как, Сафари не на Chromium

wait = WebDriverWait(driver, 10) # тут указываем, что если через 10 секунд не загрузится элемент, то убиваем скрипт

driver.get("http://127.0.0.1:5501/login") # переходим по ссылке и логинемся в аккаунт


    #            Эти функции не выполняются, пока элемент не загрузится, иначе убивает скрипт через 10 сек
    #                               |
    #                               |
    #                               V
cursor = wait.until(EC.presence_of_element_located((By.ID, 'username'))) # ищем на странице HTML элемент с id "username" (это поле ввода)
cursor.click() # тыкаем на поле ввода
cursor.send_keys("admin") # вводим строку

cursor = wait.until(EC.presence_of_element_located((By.ID, 'password'))) # тут всё так-же но с полем password 
cursor.click()
cursor.send_keys("admin")

cursor = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # в этой кнопке нет id, class или других уникальных свойств, но она только одна на странице, ищем просто любую "кнопку"
cursor.click()

driver.get("http://127.0.0.1:5501/createticket") # переходим на страницу, где создают тикет. 

cursor = wait.until(EC.presence_of_element_located((By.ID, 'number'))) # так же просто ищем поля ввода, тыкаем и вводим строки  
cursor.click()
cursor.send_keys("Т333СТ99")

cursor = wait.until(EC.presence_of_element_located((By.ID, 'text')))
cursor.click()
cursor.send_keys("тест тЕст теСт тесТ ТЕст ТеСт ТесТ тЕСт тЕсТ тест тЕст теСт тесТ ТЕст ТеСт ТесТ тЕСт тЕсТ")

cursor = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # такая же тем с уникальной кнопкой
cursor.click()


driver.get("http://127.0.0.1:5501/admin") # в админку переходим


cursor = Select(wait.until(EC.presence_of_element_located((By.ID, 'pet-select'))))  # тут у нас форма селект, так что ищем сам селект по id (я хз, почему у него такой id, скорее всего я просто украл где-то эту часть кода. Мне лень её менять)


cursor.select_by_value('delete') # ищем нужную функцию по value


cursor = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # тема с кнопкой, но тут она может быть не единственной на странице, скорее всего, селениум найдёт первое что попадётся
cursor.click()


driver.get("http://127.0.0.1:5501/logout") # разлогиневаемся

# Закрываем браузер
driver.quit()