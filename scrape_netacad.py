from bs4 import BeautifulSoup
import requests
import json
import mysql.connector
NB_PAGES = 2122
DB_HOST = "localhost"
DB_NAME = "netacad"
DB_USER = ""
DB_PASSWORD = ""

def get_page(nb):
    """
    Gets the content of the page number [nb]
    """
    PAGE='https://www.netacad.com/fr/nextgen-academies?field_ngacademy_address_country=All&page='
    res = requests.get(PAGE + str(nb))
    return res.content

def get_acad_list():
    """
    Iterates over the pages of netacad and extracts the academies and their information.
    After each page the result is stored in the database.
    """
    empty = False
    i = 0
    while not empty:
        acad_list = []
        print(f"page={i}; progress = {(i/NB_PAGES)*100}%")
        content = get_page(i)
        soup = BeautifulSoup(content, features="lxml")
        academies = soup.findAll("td", {"class":"views-field"})
        if len(academies) == 0:
            empty = True
            print("No academies on this page. Stopping")
            return
        for academy in academies:
            acad_entry = dict()
            link = academy("a")[0]
            acad_id = link.get("href")
            acad_entry['ID'] = acad_id.split("/")[-1].split("?")[0]
            acad_entry['name'] = link.text
            try:
                acad_entry['street'] = academy("div", {"class":"thoroughfare"})[0].text
            except:
                try:
                    acad_entry['street'] = academy("span", {"class":"thoroughfare"})[0].text
                except:
                    pass
            try:
                acad_entry['locality'] = academy("div", {"class":"locality"})[0].text
            except:
                try:
                    acad_entry['locality'] = academy("span", {"class":"locality"})[0].text
                except:
                    pass
            try:
                acad_entry['state'] = academy("div", {"class":"state"})[0].text
            except:
                try:
                    acad_entry['state'] = academy("span", {"class":"state"})[0].text
                except:
                    pass
            try:
                acad_entry['country'] = academy("div", {"class":"country"})[0].text
            except:
                try:
                    acad_entry['country'] = academy("span", {"class":"country"})[0].text
                except:
                    acad_entry['country'] = "Unknown"
            try:
                acad_entry['country_code'] = academy("div", {"class":"locality-block"})[0].get("class")[-1].split("-")[-1]
            except:
                try:
                    acad_entry['country_code'] = academy("span", {"class":"locality-block"})[0].get("class")[-1].split("-")[-1]
                except:
                    acad_entry['country_code'] = "Unknown"
            acad_list.append(acad_entry)
        save_db(acad_list)
        i+=1
    return 


def save_db(acad_list):
    """
    Save the list of academies and their countries in the database.
    """
    connection = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    cursor = connection.cursor(dictionary=True)
    countries = {c["country_code"]: c["country"] for c in acad_list}
    for code, name in countries.items():
        cursor.execute("INSERT IGNORE INTO countries(country_code, country) values(%s,%s)", (code, name))
    connection.commit()

    for acad in acad_list:
        country = acad.pop("country")
        keys = ','.join(acad.keys())
        values = tuple(acad.values())
        wildcard = ",".join(["%s"]*len(acad.keys()))
        q = f"INSERT IGNORE INTO academies({keys}) VALUES ({wildcard})"
        cursor.execute(q, values)
    connection.commit()


def main():
    """
    Scrapes the content of netacad website to collect the information about existing academies.
    Stores the results in a mysql database.
    """
    get_acad_list()

if __name__ == "__main__":
    main()
 
