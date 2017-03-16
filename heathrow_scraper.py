import requests
from bs4 import BeautifulSoup as BS
import csv
import time

operational_data_url = "http://heathrowoperationaldata.com/daily-operational-data/"
operational_data_page = requests.get(operational_data_url).text

soup = BS(operational_data_page, "html.parser")

data_div = soup.find_all("ul", class_="sub-menu")

data_links = []
for menu in data_div:
    list_items = menu.find_all("li")
    for links in list_items:
        data_link = links.find("a")
        data_links.append(data_link.get("href"))

with open("heathrow_data.csv", "w") as heathrow_data:

    fields = ["date", "total num arrivals", "total num departures", "total num of people making complaints", "total number of all complaints (phone, email, web, letters)"]

    writer = csv.DictWriter(heathrow_data, fields)
    writer.writeheader()

    for page in data_links:
        #final_data = []
        data_page = requests.get(page).text
        #print(page)
        soup = BS(data_page, "html.parser")
        date = soup.find("title")
        table = soup.find("tbody")
        rows = table.find_all("tr", class_=["row-3", "row-4", "row-36", "row-37"])
        data = {
            "date" : [],
            "arrivals" : [],
            "departures" : [],
            "complaints" : [],
            "total complaints" : [],
        }
        for day in date:
            data["date"].append(day)

        if "2016" or "2015" in day:
            notes = [row.find_all("td", class_="column-1")[0] for row in rows]
            for note in notes:
                note_text = note.get_text()

            cols = [row.find_all("td", class_="column-2")[0] for row in rows]

            if len(cols)==4:
                if "Notes" in note_text:
                    data["arrivals"].append(cols[0].get_text())
                    data["departures"].append(cols[1].get_text())
                    #data["complaints"].append(cols[3].get_text())
                    data["total complaints"].append(cols[2].get_text())
                    row = {"date": day, "total num arrivals": data["arrivals"][0], "total num departures": data["departures"][0], "total number of all complaints (phone, email, web, letters)": data["total complaints"][0] }

                else:
                    data["arrivals"].append(cols[0].get_text())
                    data["departures"].append(cols[1].get_text())
                    data["complaints"].append(cols[2].get_text())
                    data["total complaints"].append(cols[3].get_text())
                    row = {"date": day, "total num arrivals": data["arrivals"][0], "total num departures": data["departures"][0], "total num of people making complaints": data["complaints"][0], "total number of all complaints (phone, email, web, letters)": data["total complaints"][0] }
            else:
                data["arrivals"].append(cols[0].get_text())
                data["departures"].append(cols[1].get_text())
                data["total complaints"].append(cols[2].get_text())
                row = {"date": day, "total num arrivals": data["arrivals"][0], "total num departures": data["departures"][0], "total number of all complaints (phone, email, web, letters)": data["total complaints"][0] }


            time.sleep(1)
            writer.writerow(row)
            print("{} - ok".format(page))
        else:
            print("END".format(page))
            break
