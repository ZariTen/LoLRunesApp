import tkinter as tk
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageTk
from urllib.request import urlopen
import os

#Remember name of runes
runePrecision = ["Press the Attack","Lethal Tempo","Fleet Footwork","Conqueror","Overheal","Triumph","Presence of Mind","Legend: Alacrity","Legend: Tenacity","Legend: Bloodline","Coup de Grace","Cut Down"]
runeDomination = ["Electrocute","Predator","Dark Harvest","Hail of Blades","Cheap Shot","Taste of Blood","Sudden Impact","Zombie Ward","Ghost Poro","Eyeball Collection","Ravenous Hunter","Ingenious Hunter","Relentless Hunter","Ultimate Hunter"]
runeSorcery = ["Summon Aery","Manaflow Band","Arcane Comet","Phase Rush","Nullifying Orb","Nimbus Cloak","Transcendence","Celerity","Absolute Focus","Scorch","Waterwalking","Gathering Storm","Unflinching","Last Stand"]
runeResolve = ["Grasp of the Undying","Aftershock","Guardian","Demolish","Font of Life","Shield Bash","Conditioning","Second Wind","Bone Plating","Overgrowth","Revitalize","Approach Velocity"]
runeInspiration = ["Glacial Augment","Unsealed Spellbook","Prototype: Omnistone","Hextech Flash","Magical Footwear","Perfect Timing","Future's Market","Minion Dematerializer","Biscuit Delivery","Cosmic Insight","Time Warp Tonic"]

allRunes = runePrecision + runeDomination + runeSorcery + runeResolve + runeInspiration

path = os.getcwd()

if not os.path.isdir(f"{path}/cache"):
    os.mkdir(f"{path}/cache")
    
version_control = "11.18.1"

def get_between(txt, first, last):  # Pega a string entre first e last
    try:
        result = txt[txt.find(first) + len(first):txt.find(last)]
        return result
    except ValueError:
        return ""

root = tk.Tk()
root.title("League of Legends Runes")
root.resizable(True,True)


width = 300
height = 300
canvas1 = tk.Canvas(root,width=width,height=height)
background = ImageTk.PhotoImage(file="background.png")
canvas1.create_image(0,0,image=background,anchor="nw")
canvas1.configure(background='grey')
canvas1.pack()

def get_summoner_spell(txt):
    spells = []
    count = 0
    spellImages = ["SummonerFlash.png","SummonerHaste.png","SummonerTeleport.png","SummonerDot.png","SummonerSmite.png","SummonerBarrier.png","SummonerExhaust.png"]

    #Get spell images
    for spellImg in spellImages:
        if spellImg in txt and count < 2:
            spells.append(f"https://ddragon.leagueoflegends.com/cdn/{version_control}/img/spell/{spellImg}")
            count+=1

    # Create spell images
    i=0
    for spell in spells:
        img_data = requests.get(spell).content
        with open('cache/spell%d.jpg'%i,'wb') as handle:
            handle.write(img_data)
        img = Image.open('cache/spell%d.jpg'%i)
        img = img.resize((50,50),Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        label = tk.Label(image=image)
        label.image = image # keep a reference!
        label.pack()
        labels.append(label)
        canvas1.create_image(50+i*70,250,image=image)
        i+=1



def getRunes(champion):
    url = "https://champion.gg/champion/"+champion
    html = requests.get(url).text
    get_summoner_spell(html)
    soup = BeautifulSoup(html,features="html.parser")
    runes = []
    
    for script in soup(["script","style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    limite = 0 
    txt = text.splitlines()
    for line in txt:
        for rune in allRunes:
            if line == rune and limite < 6:
                runes.append(rune+"\n")
                limite += 1

    urlRunes = []
    for rune in runes:
        runeX = rune.replace("\n","")
        runeZ = runeX.replace(":","")
        runeZ = runeZ.replace(" ","")
        runeZ = runeZ.replace("'","")
        if runeZ == "FontofLife":# Some runes have different name on the URL
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
            if runeZ == "Triumph":# some runes have different url
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Triumph.png")
            elif runeZ == "LethalTempo":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png")
            elif runeZ == "Overheal":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Overheal.png")
            else:
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Precision",runeZ,runeZ))

        if runeX in runeDomination:
            if runeZ == "TasteOfBlood":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Domination",runeZ,"GreenTerror_TasteOfBlood"))
            else:
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Domination",runeZ,runeZ))
            
        if runeX in runeSorcery:
            if runeZ == "NimbusCloak":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/NimbusCloak/6361.png")
            elif runeZ == "Celerity":
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/Celerity/CelerityTemp.png")
            else:
                urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Sorcery",runeZ,runeZ))
            
        if runeX in runeResolve:
            urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Resolve",runeZ,runeZ))

        if runeX in runeInspiration:
            urlRunes.append("https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/%s/%s/%s.png"%("Inspiration",runeZ,runeZ))

    
    
    # append to list in order to keep the reference
    indexImg = 0
    for urllR in urlRunes:
        img_data = requests.get(urllR).content
        with open(f'{path}/cache/{indexImg}rune.png','wb') as handle:
            handle.write(img_data)
        indexImg+=1
        
    


    
    
    #canvas1.create_window(300,100+pos,window=label3)

    return runes

labelRunes = tk.Label(root,text="")

canvas1.create_window(100,140,window=labelRunes)

entry1 = tk.Entry(root)
canvas1.create_window(200,20,window=entry1)
image = None
labels =[]
def searchChampion():
    x1 = entry1.get()
    runes = getRunes(x1)
    labelRunes.config(text=''.join(runes))
    pos=0
    indexImg=0
    for labelz in labels: labelz.destroy()

    try: #Champion Splash Art
        img_data = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version_control}/img/champion/%s.png"%x1).content
        with open(f'{path}/cache/champsplash.jpg','wb') as handle:
            handle.write(img_data)
        img = Image.open(f'{path}/cache/champsplash.jpg')
        img = img.resize((50,50),Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        label = tk.Label(image=image)
        label.image = image # keep a reference!
        label.pack()
        labels.append(label)
        canvas1.create_image(100,40,image=image)
    except:pass

    for i in range(6):
        img = Image.open(f'{path}/cache/{indexImg}rune.png')
        img = img.resize((50,50),Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        

        label = tk.Label(image=image)
        label.image = image # keep a reference!
        label.pack()
        labels.append(label)
        if i > 3:# Another error from riot itself
            canvas1.create_image(200+60,pos-100,image=image)
        else:
            canvas1.create_image(200,100+pos,image=image)
        
        pos+= 50
        indexImg+=1
        root.geometry('{}x{}'.format(width, height))
    
    
    
    
button1 = tk.Button(text='Search for champion', command=searchChampion)
canvas1.create_window(200, 50, window=button1)




root.mainloop()
