import sqlite3
import argparse
import requests
import csv
import json

csvarr = [
    ["Count", "Name", "Edition", "Condition", "Language", "Foil"]
]

args = argparse.ArgumentParser(description="Parse a delver lens file into a different format")
args.add_argument(
    "-i", "--input",
    required=True,
    help="Path of the DLENS file to load",
    dest="ipath",
    metavar="PATH"
)
args.add_argument(
    "--csv",
    help="Generate a CSV file",
    metavar="FILENAME.csv",
    dest="opath"
)
args = args.parse_args()

db = sqlite3.connect(args.ipath)
db2 = sqlite3.connect("ut.db")
cursor = db.cursor()
cursor2 = db2.cursor()

cards = []

for id, card, foil, price, quantity, image, creation, list, note, condition, language, publish, tab, downloaded_img, general, img_uuid, uuid, price_acquired, scryfall_id in cursor.execute("SELECT * FROM cards").fetchall():
    cards.append({
        id:id,
        card:card,
        foil:foil,
        price:price,
        quantity:quantity,
        image:image,
        creation:creation,
        list:list,
        note:note,
        condition:condition,
        language:language,
        publish:publish,
        tab:tab,
        downloaded_img:downloaded_img,
        general:general,
        img_uuid:img_uuid,
        uuid:uuid,
        price_acquired:price_acquired,
        scryfall_id:scryfall_id})
    sfid = cursor2.execute(f"SELECT scryfall_id FROM cards WHERE _id={card}").fetchall()[0][0]
    print(sfid, id)
    scrycard = requests.get(f'https://api.scryfall.com/cards/{sfid}').json()
    print([
        int(quantity),
        scrycard["name"],
        scrycard["set"],
        "SP",
        "English",
        'foil' if foil else ''
    ])
    csvarr.append([
        int(quantity),
        scrycard["name"],
        scrycard["set"],
        "NM",
        "English",
        'foil' if foil else ''
    ])

f = open(args.opath, "w")
writer = csv.writer(f)
writer.writerows(csvarr)
f.close()

f = open("cards.json", "w")
f.write(json.dumps(cards))
f.close()