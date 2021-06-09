from flask import Blueprint
from flask import render_template, session, redirect
from flask_compress import *
from smarthome.lang import de, en
from smarthome.themes import darkmode, lightmode
from datetime import datetime
from smarthome.api import f_api
import csv
import os


sh = Blueprint('sh', __name__, template_folder='templates', static_folder='static')
sh.secret_key = "lhsgff90873wkljdfg3754jkgasdf53"

@sh.route('/service-worker.js')
def sh_sw():
    return sh.send_static_file('service-worker.js')


@sh.route("/new")
def sh_index_new():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        # New Rooms implementation
        with open('smarthome/rooms.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            next(reader, None)
            roomlist = list(reader)
        # Alle Devices werden zur Anzeige gelistet
        with open('smarthome/devices.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
            # Liste aus allen ID's und IP's erstellen
            devices_to_check = []
            counter = 1
            for item in data[counter]:
                d_id = data[counter][0]
                d_ip = data[counter][4]
                counter += 1
                devices_to_check.append([d_id, d_ip])
            # Statuscheck der Devices
            status_devices = []
            for item in devices_to_check:
                inp = ""
                values = f_api(item[0], inp)
                status_devices.append(values)
            print("ERGEBNIS: ", status_devices)
        return render_template("index_new.html", t=theme, l=language, username=username, data=data,
                               status_devices=status_devices, roomlist=roomlist)
    return redirect("/smarthome/login", code=302)


# Unter 0.0.0.0:5010/ wird index.html ausgegeben.
@sh.route("/")
def sh_index():
    # Alle Devices werden zur Anzeige gelistet
    with open('smarthome/devices.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    print(data)
    # Liste aus allen ID's und IP's erstellen
    devices_to_check = []
    counter = 1
    for item in data[counter]:
        d_id = data[counter][0]
        d_ip = data[counter][4]
        counter += 1
        devices_to_check.append([d_id, d_ip])
    # Statuscheck der Devices
    status_devices = []
    for item in devices_to_check:
        inp = ""
        values = f_api(item[0], inp)
        status_devices.append(values)
    print("ERGEBNIS: ", status_devices)

    # Alle Räume werden zur Anzeige gelistet
    rooms = []
    f = open("smarthome/rooms.txt", "r", encoding="utf-8")
    for i in f:
        rooms.append(i)
    f.close()
    # Die Platform des Nutzers wird bestimmt
    ua_platform = request.user_agent.platform
    print(ua_platform)
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        path = "smarthome/settings/" + username + "_favs.txt"
        favs = []
        with open(path, "r") as file:
            favs = file.readlines()
        favorites = []
        for element in favs:
            element = element[3:-1]
            favorites.append(element)
        print(favorites)
    else:
        username = None
        theme = lightmode
        language = de
        favorites = ""
    if ua_platform == "linux" or "windows" or "macos":
        return render_template("index.html", l=language, username=username, rooms=rooms, data=data,
                               t=theme, status_devices=status_devices, favorites=favorites)
    elif ua_platform == "iphone":
        return render_template("index_mobile.html", l=language, username=username, rooms=rooms, data=data, t=theme,
                               status_devices=status_devices)


@sh.route("/room/<raumname>")
def sh_single_room(raumname):
    room = raumname
    # Alle Räume werden zur Anzeige gelistet
    rooms = []
    f = open("smarthome/rooms.txt", "r", encoding="utf-8")
    for i in f:
        rooms.append(i)
    f.close()
    # Alle Devices werden zur Anzeige gelistet
    with open('smarthome/devices.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    # Liste aus allen ID's und IP's erstellen
    devices_to_check = []
    counter = 1
    for item in data[counter]:
        d_id = data[counter][0]
        d_ip = data[counter][4]
        counter += 1
        devices_to_check.append([d_id, d_ip])
    # Statuscheck der Devices
    status_devices = []
    for item in devices_to_check:
        inp = ""
        values = f_api(item[0], inp)
        status_devices.append(values)
    print("ERGEBNIS: ", status_devices)
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        elif lan == "de":
            language = de
        if appearance == "darkmode":
            theme = darkmode
        elif appearance == "lightmode":
            theme = lightmode
    else:
        username = None
        theme = lightmode
        language = de
    return render_template("single_room.html", room=room, l=language, username=username, t=theme, data=data,
                           status_devices=status_devices, rooms=rooms)


# Es folgt unnötiger Kram
@sh.route("/profile/<profilename>")
def sh_profile(profilename):
    profile = profilename
    # Alle Räume werden zur Anzeige gelistet
    rooms = []
    f = open("smarthome/rooms.txt", "r", encoding="utf-8")
    for i in f:
        rooms.append(i)
    f.close()
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
    else:
        username = None
        theme = lightmode
        language = de
    return render_template("profile.html", l=language, username=username, profile=profile, t=theme,
                           rooms=rooms)


# Unter 0.0.0.0:5010/admin wird admin.html ausgegeben.
@sh.route("/admin")
def sh_admin():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        return render_template("admin.html", username=username, l=language, t=theme)
    else:
        return redirect("/smarthome/login", code=302)


@sh.route("/admin/rooms")
def sh_admin_rooms():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        # Alle Räume werden zur Anzeige gelistet
        rooms = []
        f = open("smarthome/rooms.txt", "r", encoding="utf-8")
        for i in f:
            rooms.append(i)
        f.close()
        return render_template("admin/rooms.html", l=language, username=username, rooms=rooms, t=theme)
    else:
        return redirect("/smarthome/login", code=302)


@sh.route("/admin/rooms/delete/<room>")
def sh_admin_rooms_delete(room):
    # Es werden alle Räume gelistet
    rooms = []
    f = open("smarthome/rooms.txt", "r")
    for i in f:
        rooms.append(i)
    f.close()
    # Der zu löschende Raum wird entfernt
    room_to_remove = room+"\n"
    rooms.remove(room_to_remove)
    # Die Datei wird überschrieben
    f = open("smarthome/rooms.txt", "w")
    for i in rooms:
        f.write(i)
    f.close()
    return redirect("/smarthome/admin/rooms", code=302)


@sh.route("/admin/rooms/add", methods=['POST'])
def sh_admin_rooms_add():
    # Der neue Raum wird an die rooms.txt angehängt
    f = open("smarthome/rooms.txt", "a", encoding="utf-8")
    f.write(request.form['newroom'] + "\n")
    f.close()
    return redirect("/smarthome/admin/rooms", code=302)


@sh.route("/admin/devices")
def sh_admin_devices():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        with open('smarthome/devices.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
        return render_template("/admin/devices.html", l=language, username=username, t=theme, data=data)
    else:
        return redirect("/smarthome/login", code=302)


@sh.route("/admin/devices/add", methods=['POST'])
def sh_admin_devices_add():
    id = request.form['nd_id']
    ip = request.form['nd_ip']
    name = request.form['nd_name']
    room = request.form['nd_room']
    typ_id = request.form['nd_type']
    if typ_id == "1":
        typ = "Lampe"
    elif typ_id == "2":
        typ = "Steckdose"
    elif typ_id == "3":
        typ = "PC"
    else:
        typ = "Temp-Sensor"
    new_device = id + ";" + room + ";" + name + ";" + typ + ";" + ip + ";" + typ_id + "\n"
    print(new_device)
    with open('smarthome/devices.csv', 'a', encoding="utf-8") as file:
        file.write(new_device)

    return redirect("/smarthome/admin/devices", code=302)


@sh.route("/admin/users")
def sh_admin_users():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        # Alle Nutzer werden gelistet um sie auf der Seite anzeigen zu können
        users = []
        with open('smarthome/users.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                users.append(row)
        return render_template("admin/users.html", l=language, username=username, users=users, t=theme)
    else:
        return redirect("/smarthome/login", code=302)


@sh.route("/admin/users/add", methods=['POST'])
def sh_admin_users_add():
    # Formular wird abgerufen
    new_username = request.form['newuser']
    new_password = request.form['pass']
    # Name und Passwort werden eingetragen
    with open('smarthome/users.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([new_username, new_password])
    # Persönliche Einstellungsdatei wird erstellt und mit den Standardwerten gefüllt
    settingspath = "settings/" + request.form['newuser'] + ".txt"
    f = open(settingspath, "w")
    f.write("darkmode")
    f.write("\n")
    f.write("de")
    f.close()
    # Weiterleitung ins Admin Panel
    return redirect("/smarthome/admin/users", code=302)


@sh.route("/admin/users/delete/<user>")
def sh_admin_users_remove(user):
    # Alle Nutzer werden in eine Liste gelesen
    users = []
    with open('smarthome/users.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            users.append(row)
    counter = 0
    # Es werden alle Nutzer überprüft ob sie gemeint sind, der gemeinte wird rausgeschmissen
    for i in users:
        if user in i:
            users.pop(counter)
        counter += 1
    # Die Nutzerdatei wird neu geschrieben
    with open('smarthome/users.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        for i in users:
            writer.writerow(i)
    # Die persönlichen Einstellungen vom Nutzer werden gelöscht
    settingspath = "settings/" + user + ".txt"
    os.remove(settingspath)
    return redirect("/smarthome/admin/users", code=302)


@sh.route("/admin/users/usersettings")
def sh_admin_usersettings():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        return render_template("/admin/user_settings.html", username=username, l=language, t=theme)
    else:
        return redirect("/smarthome/login", code=302)


@sh.route("/admin/users/usersettings/appearance", methods=['POST'])
def sh_admin_usersettings_submit():
    # Das Formular wird abgerufen
    theme = request.form['appearance']
    language = request.form['language']
    # Die neuen Einstellungen werden geschrieben und die Session aktualisiert
    settingspath = "smarthome/settings/" + session['username'] + ".txt"
    f = open(settingspath, "w")
    f.write(theme)
    f.write("\n")
    f.write(language)
    f.close()
    session['language'] = language
    session['theme'] = theme
    return redirect("/smarthome/admin/users/usersettings", code=302)


@sh.route("/admin/speechrecognition")
def sh_admin_speech_recognition():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        with open("sr_settings.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
        for setting in data:
            if setting[0] == "OWM Key":
                owm_key = setting[1]
        return render_template("/admin/speech_recognition_settings.html", username=username, l=language, t=theme,
                               owm_key=owm_key)
    return redirect("/login", code=302)


@sh.route("/admin/speechrecognition/changesettings", methods=['POST'])
def sh_admin_speech_recognition_submit():
    new_api_key_owm = request.form['api_key_owm']
    with open("sr_settings.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    for item in data:
        if item[0] == "OWM Key":
            item[1] = new_api_key_owm
    print(data)
    with open("sr_settings.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        for setting in data:
            if setting != "":
                writer.writerow(setting)
    return redirect("/smarthome/admin/speechrecognition", code=302)


@sh.route("/admin/users/favorites")
def sh_admin_user_favorites():
    if 'username' in session:
        username = session['username']
        lan = session['language']
        appearance = session['theme']
        appearance = appearance.rstrip()
        if lan == "en":
            language = en
        else:
            language = de
        if appearance == "darkmode":
            theme = darkmode
        else:
            theme = lightmode
        with open('smarthome/devices.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
            print(data)
        data.pop(0)
        for device in data:
            device.pop(3)
            device.pop(3)
            device.pop(3)
        print(data)
        return render_template("/admin/user_favorites.html", l=language, t=theme, username=username, data=data)
    return redirect("/login", code=302)


@sh.route("/admin/users/favorites/submit", methods=['Post'])
def sh_admin_user_favorites_submit():
    if 'username' in session:
        username = session['username']
        favs = []
        d1 = request.form['d1']
        d2 = request.form['d2']
        d3 = request.form['d3']
        d4 = request.form['d4']
        favs.append(d1 + "\n")
        favs.append(d2 + "\n")
        favs.append(d3 + "\n")
        favs.append(d4 + "\n")
        path = "smarthome/settings/" + username + "_favs.txt"
        with open(path, "w") as f:
            for item in favs:
                f.write(item)
        return redirect("/smarthome/admin/users/favorites")
    return redirect("/login", code=302)


# Unter 0.0.0.0:5010/login wird login .html ausgegeben.
@sh.route("/login", methods=['GET', 'POST'])
def sh_login():

    # Wenn das Formular abgeschickt wurde wird geprüft ob Nutzer und PW übereinstimmen
    if request.method == 'POST':
        with open('smarthome/users.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if row[0] == request.form['username']:
                    if row[1] == request.form['password']:
                        # LOG
                        now = datetime.now()
                        date = now.strftime("%Y/%m/%d %H:%M:%S")
                        log_entry = date + " " + row[0] + " Login Successful\n"
                        f = open("smarthome/logs/log_logins.txt", "a")
                        f.write(log_entry)
                        # Die Session wird geschrieben / Einstellungen werden aus der txt übernommen
                        session['username'] = request.form['username']
                        settingspath = "smarthome/settings/"+request.form['username']+".txt"
                        f = open(settingspath, "r")
                        usersettings = []
                        for i in f:
                            usersettings.append(i)
                        f.close()
                        session['theme'] = usersettings[0]
                        session['language'] = usersettings[1]
                        # man gelangt ins Admin Panel
                        return redirect("/smarthome/admin")
                else:
                    f = open("smarthome/logs/log_logins.txt", "a")
                    user_ip = request.environ['REMOTE_ADDR']
                    now = datetime.now()
                    date = now.strftime("%Y/%m/%d %H:%M:%S")
                    log_entry = date + "Login Failed (Wrong Username)" + user_ip
                    f.write(log_entry)
                    f.close()
            # Oder auch nicht
            return redirect("/smarthome/login", code=302)
    # Die Login Seite wird auf Deutsch (Default) angezeigt
    if request.method == 'GET':
        return render_template("login.html", l=de, t=darkmode)


@sh.route("/logout")
def sh_logout():
    # Die Session wird gelöscht, der Nutzer wird auf die Startseite weitergeleitet
    session.pop('username', None)
    session.pop('language', None)
    session.pop('theme', None)
    return redirect("/smarthome", code=302)


@sh.route("/api")
def sh_api():
    return render_template("api.html")


@sh.route("/api/<id>/on")
def sh_api_device_on(id):
    id = id
    with open('smarthome/devices.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    inp = "on"
    for i in data:
        if i[0] in id:
            f_api(i[0], inp)

    return redirect("/smarthome", code=302)


@sh.route("/api/<id>/off")
def sh_api_device_off(id):
    id = id
    with open('smarthome/devices.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    inp = "off"
    for i in data:
        if i[0] in id:
            f_api(i[0], inp)

    return redirect("/smarthome", code=302)


@sh.route("/api/<id>/brightness", methods=['POST'])
def sh_api_light_brightness(id):
    id = id
    inp = request.form['brightness']
    with open('smarthome/devices.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    for i in data:
        if i[0] in id:
            f_api(i[0], inp)
    return redirect("/smarthome", code=302)


@sh.route("/api/<id>/<color>")
def sh_api_light_color(id, color):
    d_id = id
    inp = color
    with open('smarthome/devices.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    for i in data:
        if i[0] in id:
            f_api(i[0], inp)
    return redirect("/smarthome", code=302)