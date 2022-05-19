import tkinter as tk
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageTk
import os

# Remember name of runes
runePrecision = ["Press the Attack", "Lethal Tempo", "Fleet Footwork", "Conqueror", "Overheal", "Triumph",
                 "Presence of Mind", "Legend: Alacrity", "Legend: Tenacity", "Legend: Bloodline", "Coup de Grace", "Cut Down"]
runeDomination = ["Electrocute", "Predator", "Dark Harvest", "Hail of Blades", "Cheap Shot", "Taste of Blood", "Sudden Impact",
                  "Zombie Ward", "Ghost Poro", "Eyeball Collection", "Ravenous Hunter", "Ingenious Hunter", "Relentless Hunter", "Ultimate Hunter"]
runeSorcery = ["Summon Aery", "Manaflow Band", "Arcane Comet", "Phase Rush", "Nullifying Orb", "Nimbus Cloak",
               "Transcendence", "Celerity", "Absolute Focus", "Scorch", "Waterwalking", "Gathering Storm", "Unflinching", "Last Stand"]
runeResolve = ["Grasp of the Undying", "Aftershock", "Guardian", "Demolish", "Font of Life", "Shield Bash",
               "Conditioning", "Second Wind", "Bone Plating", "Overgrowth", "Revitalize", "Approach Velocity"]
runeInspiration = ["Glacial Augment", "Unsealed Spellbook", "Prototype: Omnistone", "Hextech Flash", "Magical Footwear",
                   "Perfect Timing", "Future's Market", "Minion Dematerializer", "Biscuit Delivery", "Cosmic Insight", "Time Warp Tonic"]

allRunes = runePrecision + runeDomination + \
    runeSorcery + runeResolve + runeInspiration

path = os.getcwd()

if not os.path.isdir(f"{path}/cache"):
    os.mkdir(f"{path}/cache")

version_control = "11.18.1"


def get_between(txt, first, last):
    try:
        result = txt[txt.find(first) + len(first):txt.find(last)]
        return result
    except ValueError:
        return ""


root = tk.Tk()
root.title("LoLRunes")
root.resizable(True, True)


width = 800
height = 600
canvas1 = tk.Canvas(root, width=width, height=height)
background_image = Image.open("background.png").resize(
    (800, 600), Image.Resampling.LANCZOS)
background = ImageTk.PhotoImage(image=background_image)
canvas1.create_image(0, 0, image=background, anchor="nw")
canvas1.configure(background='grey')
canvas1.pack()


def getRunes(champion):
    url = "https://champion.gg/champion/"+champion
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    runes = []

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    limite = 0
    txt = text.splitlines()
    for line in txt:
        for rune in allRunes:
            if rune in line and limite < 6:
                runes.append(rune+"\n")
                limite += 1

    urlRunes = []
    for rune in runes:
        runeX = rune.replace("\n", "")
        runeZ = runeX.replace(":", "")
        runeZ = runeZ.replace(" ", "")
        runeZ = runeZ.replace("'", "")
        if runeZ == "FontofLife":  # Fix rune names on URL
            runeZ = "FontOfLife"
        if runeZ == "PresstheAttack":
            runeZ = "PressTheAttack"
        if runeZ == "HailofBlades":
            runeZ = "HailOfBlades"
        if runeZ == "TasteofBlood":
            runeZ = "TasteOfBlood"
        if runeZ == "PresenceofMind":
            runeZ = "PresenceOfMind"
        if runeZ == "Legend:Bloodline":
            runeZ = "LegendBloodline"
        if runeZ == "CoupdeGrace":
            runeZ = "CoupDeGrace"
        if runeZ == "Aftershock":
            runeZ = "VeteranAftershock"
        if runeZ == "GraspoftheUndying":
            runeZ = "GraspOfTheUndying"
        if runeZ == "ShieldBash":
            runeZ = "MirrorShell"

        if runeX in runePrecision:
            if runeZ == "Triumph":  # Fix rune names on URL
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Triumph.png")
            elif runeZ == "LethalTempo":
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png")
            elif runeZ == "Overheal":
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Overheal.png")
            else:
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" % ("Precision", runeZ, runeZ))

        if runeX in runeDomination:
            if runeZ == "TasteOfBlood":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" %
                                ("Domination", runeZ, "GreenTerror_TasteOfBlood"))
            else:
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" % ("Domination", runeZ, runeZ))

        if runeX in runeSorcery:
            if runeZ == "NimbusCloak":
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/NimbusCloak/6361.png")
            elif runeZ == "Celerity":
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/Celerity/CelerityTemp.png")
            else:
                urlRunes.append(
                    "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" % ("Sorcery", runeZ, runeZ))

        if runeX in runeResolve:
            urlRunes.append(
                "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" % ("Resolve", runeZ, runeZ))

        if runeX in runeInspiration:
            urlRunes.append(
                "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png" % ("Inspiration", runeZ, runeZ))

    for indexImg, urllR in enumerate(urlRunes):
        img_data = requests.get(urllR).content
        with open(f'{path}/cache/{indexImg}rune.png', 'wb') as handle:
            handle.write(img_data)

    return runes


labelRunes = tk.Label(root, text="")

canvas1.create_window(360, 340, window=labelRunes)

champion_name_entry = tk.Entry(root)
canvas1.create_window(400, 100, window=champion_name_entry)
image = None
labels = []


def fetch_champion_splash(champion_name):
    img_data = requests.get(
        f"http://ddragon.leagueoflegends.com/cdn/{version_control}/img/champion/{champion_name}.png").content
    with open(f'{path}/cache/champsplash.jpg', 'wb') as handle:
        handle.write(img_data)


def add_champion_splash(champion_name):
    fetch_champion_splash(champion_name)
    img = Image.open(f'{path}/cache/champsplash.jpg')
    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(img)
    label = tk.Label(image=image)
    label.image = image
    label.pack()
    labels.append(label)
    canvas1.create_image(200, 120, image=image)


def add_champion_runes():
    rune_ypos = 150
    for rune_count in range(6):  # Get all champion runes
        img = Image.open(f'{path}/cache/{rune_count}rune.png')
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)

        label = tk.Label(image=image)
        label.image = image
        label.pack()
        labels.append(label)
        if rune_count > 3:
            canvas1.create_image(490+60, rune_ypos-100, image=image)
        else:
            canvas1.create_image(490, 100+rune_ypos, image=image)

        rune_ypos += 50
        root.geometry('{}x{}'.format(width, height))


def searchChampion():
    champion_name = champion_name_entry.get()
    labelRunes.config(text=''.join(getRunes(champion_name)))
    for labelz in labels:
        labelz.destroy()

    try:
        add_champion_splash(champion_name)
        add_champion_runes()
    except:
        pass


search_champion_btn = tk.Button(
    text='Search for champion', command=searchChampion)
canvas1.create_window(400, 150, window=search_champion_btn)
root.mainloop()
