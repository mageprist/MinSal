# Skapad av Sör'n 06/05-22

import pycurl
from io import BytesIO
import csv
from datetime import datetime
from datetime import timedelta
import sys
from os.path import exists

ROOM_NR = ['101125, Ångström', 
       '101127, Ångström', 
       '101130, Ångström', 
       '101132, Ångström', 
       '101136 Del A, Ångström', 
       '101136 Del B, Ångström', 
       '101142, Ångström', 
       '101146, Ångström', 
       '101150, Ångström', 
       '101154, Ångström',
       '101156, Ångström', 
       '101158, Ångström', 
       '101162, Ångström', 
       '101166, Ångström', 
       '101168, Ångström', 
       '101170, Ångström', 
       '101172, Ångström', 
       '101174, Ångström', 
       '101180, Ångström', 
       '101182, Ångström', 
       '101190, Ångström', 
       '101192, Ångström', 
       '101258, Ångström', 
       '101260, Ångström', 
       '10131, Grupprum, Ångström', 
       '10133, Grupprum, Ångström', 
       '10208, Grupprum, Ångström', 
       '10210, Grupprum, Ångström', 
       '10211, Grupprum, Ångström', 
       '10212, Grupprum, Ångström', 
       '10213, Grupprum, Ångström', 
       '11167, Ångström', 
       '12167, Ångström', 
       '1403, Grupprum/Gruppyta, Ångström', 
       '2001, Ångström', '2002, Ångström', 
       '2003, Ångström', 
       '2004, Ångström', 
       '2005, Ångström', 
       '2040, Grupprum, Ångström', 
       '2041, Grupprum, Ångström', 
       '2042, Grupprum, Ångström', 
       '2043, Grupprum, Ångström', 
       '2044, Grupprum, Ångström', 
       '2045, Grupprum, Ångström', 
       '2046, Grupprum, Ångström', 
       '4001, Ångström', 
       '4003, Ångström', 
       '4004, Ångström', 
       '4005, Ångström', 
       '4006, Ångström', 
       '4007, Ångström', 
       '4101, Ångström', 
       '80101, Ångström', 
       '80109, Ångström', 
       '80115, Ångström', 
       '80121, Ångström', 
       '80127, Ångström', 
       '80412, Ångström', 
       '90101, Ångström', 
       '90102, Ångström', 
       '90103, Ångström', 
       '90106, Ångström', 
       '90402, Ångström', 
       '90403, Ångström', 
       '90409, Ångström', 
       'Eva von Bahr, 10K1190, Ångström', 
       'Evelyn Sokolowski, 101136, Ångström', 
       'Heinz-Otto Kreiss, 101195, Ångström', 
       'Häggsalen, 10132, Ångström', 
       'Polhemsalen, 10134, Ångström', 
       'Siegbahnsalen, 10101, Ångström', 
       'Sonja Lyttkens, 101121, Ångström']

URL = "https://cloud.timeedit.net/uu/web/schema/"\
      "ri1Xc0gw6560YbQQY7ZgZZZX89ZZZX8Y0Cy300pZZ"\
      "ZX8a1Y63Q062f5Y7ZZZZX891B6Cv7aFZZZX8da8ZZ"\
      "ZX8Y7y5Yru7wbaZZZX8ZZZX8gY7GnByYduA1pbZZZ"\
      "X8YwC5bLAvC7C8jZZZX8QG5W1l07b3Wa5x6YMcWXY"\
      "jy60qZ40aQWlnW5uv7xwy6d3061X24WXnoWoW6a43"\
      "6KcWWnY55065aL69jV%C3%A4W6v6a0x3Xv5XXj8WK"\
      "w0ZaWQXxZrce0j1Qo5koZl9jo4mQwc.html"


HTML_FILE = "time-edit.html"
PARSED_TEXT_FILE = "parsed.txt"

class Rum:
    def __init__(self, name, time_array=[]):
        self.name = name
        self.occupied = time_array

    def add_occupied(self, time_array):
        if isinstance(time_array, list):
            for x in time_array:
                self.occupied.append(x)
        if isinstance(time_array, str):
            self.occupied.append(x)

    def __str__(self):
        # Morgon | Förmiddag | Lunch | Eftermiddag | Kväll
        output = ["O","O","O","O","O","O","O"]  
        borders = [0, 8, 10, 12, 13, 15, 17, 24] 
        for time in self.occupied:
            split = time.split(" - ")
            start = int(split[0][:2])
            slut = int(split[1][:2])
        
            mellan = False
            for x,edge in enumerate(borders):
                if x == 7:
                    break
                else:
                    if start >= edge and start < borders[x+1]:
                        output[x] = "X" 
                        mellan = True
                    if slut > edge and slut <= borders[x+1]:
                        output[x] = "X"
                        mellan = False

                    if mellan:
                        output[x] = "X"
        
        nice_output = output[0] + \
                "|" + output[1] + \
                output[2] + "|" + \
                output[3] + "|" + \
                output[4] + \
                output[5] + "|" + \
                output[6]
   
        out = f"{self.name : <40}{nice_output : >11}"

        return out

    def brahet(self):
        # Returnerar hur bra ett rum är
        # 0 - 7, 7 bäst
        bra = 0
        for x in str(self):
            if x == "O":
                bra += 1
        return bra


def get_from_internet(url, file= ""):
    # Returns timeedit html
    # Optionally saves to file
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL,url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue()

    if file != "":
        f = open(file, "w")
        f.write(get_body.decode('utf8'))
        f.close()
    return get_body.decode('utf8')

def parse_file(file_parsed, file_read, day):
    # Returns dictionary with room as key and list of 
    # occupied times
    # Day = 0 idag, Day = 1, imorgon 
    rooms = {}

    date = datetime.today() + timedelta(days=day)
    dag = date.strftime('%Y-%m-%d')

    with open(file_read) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        f.close()

    table_lines = []

    f = open(file_parsed, "w")
    tabel_bol = False
    for line in lines:
        if line == "<table>":
            tabel_bol = True 
        elif line == "</table>" and tabel_bol:
            tabel_bol = False
        if tabel_bol:
            f.write(line + "\n")
            table_lines.append(line)

    idag = False 
    for line in table_lines:
        if 'colspan="2"' in line:
            split = line.split(">")
            split2 = split[1].split("<")
            datum = split2[0].split()[1]
            if datum == dag:
                idag = True
            else:
                idag = False

        if "<td id=" in line and idag:
            split = line.split(">")
            tid = split[1][:-4]

        if '<td  class="column' in line and idag:
            split = line.split(">")
            sal = split[1][:-4]
            if sal not in rooms:
                rooms[sal] = [tid]
            else:
                rooms[sal].append(tid)

    f.close()
    return rooms

def get_brahet(obj):
    return obj.brahet()

if __name__ == "__main__":
    update = False
    if len(sys.argv) == 2:
        if "-u" in sys.argv:
           update = True
    
    if not exists(HTML_FILE):
        update = True

    if update:
        get_from_internet(URL, HTML_FILE)

    # Vad händer som idag inte finns med? 
    rooms_from_timeedit = parse_file(PARSED_TEXT_FILE, HTML_FILE, 0)

    list_of_rooms = []
    for room in ROOM_NR:
        if room in rooms_from_timeedit: 
            list_of_rooms.append(Rum(room, rooms_from_timeedit[room]))
        else:
            list_of_rooms.append(Rum(room))
    
    list_of_rooms.sort(key=get_brahet)
    for x in list_of_rooms:
        print(x)

