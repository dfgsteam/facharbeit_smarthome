import requests
from bs4 import BeautifulSoup
import csv

ID_pos = None
Typ_pos = None
IP_pos = None


def f_api(id, inp):
    values = []
    typ_id = None

    # Hängt an die Liste "values" als erste Position die Typ-id
    values.clear()
    values.append(id)

    # Packt den Inhalt der devices.csv in die Liste "data"
    with open("smarthome/devices.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    # Packt packt die jeweilige Position der Beschreibung in den jeweiligen Integer
    data_check = str(data[0][0]).split(";")
    for i in range(0, len(data_check)):
        if data_check[i] == "ID":
            ID_pos = i
        if data_check[i] == "TYP-ID":
            Typ_pos = i
        if data_check[i] == "IP":
            IP_pos = i

    if ID_pos != "" and Typ_pos != "" and IP_pos != "":
        print("API: positions loaded")

        # Überprüft die ID mit der devices nach der ID
        if id != "":
            for i in range(1, len(data)):
                data_new = str(data[i][0]).split(";")
                if data_new[ID_pos] == str(id):
                    ip = str(data_new[IP_pos])
                    typ_id = data_new[Typ_pos]
                    break

            # Wenn die ID nicht vorhanden ist, endet das Programm mit den Fehlercode "e2"
            if typ_id == None:
                print("API: id isnt matching: " + str(id))
                values.append("e2")
                return values
                exit()

            print(str("API: TYP-ID: ") + typ_id)
            print(str("API: IP: ") + ip)
            values.append(typ_id)

            try:
                r = requests.get("http://" + str(ip) + "/" + str(inp), timeout=2)
            except requests.exceptions.ConnectionError as error:
                print("API: webserver connectionError")
                values.append("e3")
            except requests.exceptions.ReadTimeout as error:
                print("API: webserver timeout")
                values.append("e3")

            if "e3" not in values:
                soup = BeautifulSoup(r.text, 'html.parser')

                # IDs die es auf der Seite gibt, werden in den Array "values" geladen
                ids = [tag['id'] for tag in soup.select('span[id]')]
                for i in range(0, len(ids)):
                    a = str(soup.find(id=ids[i]))
                    a = a.split(">")
                    a = a[1]
                    a = a[:-6]
                    values.append(a)

        # Wenn keine ID gegeben wird.
        else:
            print("API: id is missing")
            values.append("e2")

    else:
        print("API: devices.csv is missing")
        values.clear()
        values.append("e1")

    print(str("API: VALUES -  ['TYP-ID/ERROR', 'STATE/TEMP', 'DIM', 'COLOR']"))
    print(str("API: VALUES -  ") + str(values))

    return values


values = f_api(id=1101, inp="")
print(values)
