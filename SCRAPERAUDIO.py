from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
import os

# Chemin vers le ChromeDriver
driver_path = "E:\\driver\\chromedriver.exe"

# Initialiser le navigateur
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Exécuter en mode sans tête

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def scrape_podcasts():
    # URL de la page des podcasts
    url = "https://www.mfmradio.ma/%D8%A8%D9%88%D8%AF%D9%83%D8%A7%D8%B3%D8%AA/"
    driver.get(url)
    time.sleep(5)  # Attendre que la page se charge complètement

    # Trouver tous les éléments qui contiennent le titre et le lien du podcast
    podcasts = driver.find_elements(By.XPATH, "//div[@class='col-7 d-flex align-items-center']/a")

    podcast_data = []
    for podcast in podcasts:
        title = podcast.find_element(By.XPATH, ".//h4").text
        link = podcast.get_attribute("href")
        if title and link:
            podcast_data.append([title, link])  # Ajouter les titres et liens au tableau

    return podcast_data

def save_to_csv(data, filename=r"C:\Users\INKA\Desktop\EfficientNet-B0\mfm_podcasts.csv"):
    # Si le fichier n'existe pas, créer le fichier et ajouter les entêtes
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writerow(["Titre", "Lien"])  # Ajouter les entêtes
        writer.writerows(data)

if __name__ == "__main__":
    # Scraper les podcasts
    podcast_data = scrape_podcasts()
    if podcast_data:
        save_to_csv(podcast_data)
        print(f"{len(podcast_data)} podcasts ont été ajoutés dans le fichier CSV.")
    else:
        print("Aucun podcast trouvé.")

    driver.quit()
