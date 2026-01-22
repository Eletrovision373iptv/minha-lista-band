import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capturar_link():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Roda sem abrir janela
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    print("Acessando a Band...")
    driver.get("https://www.band.com.br/ao-vivo")
    
    # Espera 15 segundos para o player carregar e gerar o token
    time.sleep(15)
    
    # Analisa as requisições de rede do navegador para achar o .m3u8
    logs = driver.execute_script("return window.performance.getEntries();")
    link_m3u8 = None
    
    for entry in logs:
        if "playlist-1080p.m3u8" in entry['name']:
            link_m3u8 = entry['name']
            break
            
    driver.quit()
    return link_m3u8

novo_link = capturar_link()

if novo_link:
    print(f"Link encontrado: {novo_link}")
    with open("band.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Band Ao Vivo\n")
        f.write(novo_link)
else:
    print("Não foi possível capturar o link.")
