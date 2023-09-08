from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

def get_data_from_url(url):
    driver = webdriver.Firefox(executable_path=r'C:\Users\ctmiraperceval\Downloads\geckodriver-v0.33.0-win32\geckodriver.exe')
def get_data_from_url(url):
    driver = webdriver.Firefox()  # o puedes usar webdriver.Chrome() si tienes Chrome
    driver.get(url)

    # Espera a que se cargue el contenido dinámico
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'area')))

    # Encuentra todos los elementos que satisfacen las condiciones
    areas = driver.find_elements_by_css_selector('area[shape="poly"][id*="VPARTICELLE"]')

    ids = [area.get_attribute('id') for area in areas]

    driver.quit()

    return ids

if __name__ == '__main__':
    url = 'http://cartografia.infobat.it/bat/index.jsp?application=CAT'
    print(get_data_from_url(url))
