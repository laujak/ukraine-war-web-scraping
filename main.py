from selenium import webdriver
import pandas as pd


DATES = {
    "Січня": "01",
    "Лютий": "02",
    "Березня": "03",
    "Квітня": "04",
    "Травня": "05",
    "Червня": "06",
    "Липень": "07",
    "Серпень": "08",
    "Вересень": "09",
    "Жовтень": "10",
    "Листопада": "11",
    "Грудень": "12"
}

FEATURES = {"собового": "personnel",
            "особовий склад": "personnel",
            "танків": "tanks",
            "бойових броньованих": "apv",
            "ББМ": "apv",
            "артилерійських": "artillery_systems",
            "РСЗВ": "mlrs",
            "ППО": "anti_aircraft_systems",
            "літаків": "aircrafts",
            "гелікоптерів": "helicopters",
            "БПЛА": "drones",
            "рилаті": "cruise_missiles",
            "катери": "boats",
            "катерів": "boats",
            "автомобільної": "vehicles",
            "пеціальна": "special_eq"}


PATH = "C:\Development\chromedriver.exe"
URL = "https://armyinform.com.ua/search/%22%D0%B2%D1%82%D1%80%D0%B0%D1%82%D0%B8+%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%D0%BD%D0%B8%D0%BA%D0%B0+%D0%B7+%22"

driver = webdriver.Chrome(PATH)
driver.get(URL)

section = driver.find_element(by="id", value="main")
tags_a = section.find_elements(by="tag name", value="a")
links = [tag.get_attribute(name="href") for tag in tags_a]
data = dict()
for link in links:
    article = dict()
    article_f = dict()
    driver.get(link)
    index = 0

    date = driver.find_element(by="class name", value="single-date")
    date = date.text.split("хв. ")[1].split(",")[0].split(" ")
    name = date[2] + "-" + DATES[date[1]] + "-" + date[0].zfill(2)

    content = driver.find_element(by="class name", value="single-content")

    paragraphs = content.find_elements(by="tag name", value="li")
    if not paragraphs:
        paragraphs = content.find_elements(by="tag name", value="p")

    for par in paragraphs[:16]:
        for feature in FEATURES:
            if feature in par.text:
                text = par.text[par.text.index(feature):]
                text = text.split("(")[0]
                text = text.split(",")[0]
                num = ""

                for i in text:
                    if i.isnumeric():
                        num += str(i)
                if "тис" in par.text:
                    num += "000"
                article[FEATURES[feature]] = num
    data[name] = article
    print(article)


df = pd.DataFrame(data).T

df.to_csv("data.csv", sep=";")
