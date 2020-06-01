
import sqlgame as db
import random
import math
import json





def existing_char(ID):
    if db.exists(ID) != None:
        return "exists"
    else:
        return None

def start(a): #a = @user
    if existing_char(a) == None:
        return (f"Welcome to the world of Yae <@{a}>. You have decided to become someone special , someone who might save this world thus, as the goddess Tozen,  let me grant you some blessings. To get my powers , you will need to pass the divine ceremony. Oh young soul , tell me your name")
    else:
        return None

def welcome(a):
    return f"Dear {a}, are you male or female?"

def getgender(b): #b =  gender of user
    if b.lower() == "female":
        return b
    elif b.lower() == "male":
        return b
    else:
        return None

def createchar(a, b, c):
    if getgender(b) == None:
        return "Gender chosen is not available, please restart the ceremony with ^start"
    else:
        b = getgender(b)
        ID = c
        db.new_player(c, a, b)
        return f'''
         The first part of the divine ceremony is over. Your current status is : 
         Name = {a},  Race = {db.select("character","race", ID)},  Gender = {b} and Level = {db.select("character", "level", ID)}.
         Your current stats are : 
         {db.select("character","hp", ID)} hp,  {db.select("character","ad", ID)} strength,  {db.select("character","ap", ID)} intelligence,  {db.select("character","spd", ID)} agility and {db.select("character","mana", ID)} mana.
         Welcome to Floor 1: The Amethyst Forest
         To continue to the second part, please write ^learnskill '''

def checkskill(ID):
    if existing_char(ID)!= None:
        if db.select("character","wornactskill", ID) != None or db.select("character","wornpassskill", ID)!= None:
            return None #exists and at least one skill
        else:
            return "exists but no skill" #exists but no skill
    else:
        return "does not exist"#does not exist

def randomskill(ID, m):
    active = ["Slash[Common]", "Cut[Common]", "Thunderbolt[Common]", "Firebolt[Common]", "Triple Slash[Rare]",
              "Storm[Rare]", "Sword of Judgement[Epic]", "Flames of Destruction[Epic]", "Azrael[Legendary]",
              "Amaterasu[Legendary]", "Divine Punishment[Mythic]", "Divine Light[Mythic]"]
    passive = ["Regeneration[Common]", "Focus[Common]", "Warrior's Determination[Rare]", "Sage's Determination[Rare]",
               "Golem's Strength[Epic]", "Eye of Serluth[Epic]", "Partial Draconic Transformation[Legendary]",
               "Dragon's Wisdom[Legendary]",
               "Sin of Envy[Mythic]", "Sin of Wrath[Mythic]", "Sin of Gluttony[Mythic]", "Sin of Lust[Mythic]", "Sin of Pride[Mythic]", "Sin of Sloth[Mythic]", "Sin of Greed[Mythic]"]
    if existing_char(ID)!= None:
        if m.lower() == "active": #i'd recommend taking an active skill since i did not add the passive skill features yet
            a = random.choices(active, weights=[15, 15, 15, 15, 10, 10, 5, 5, 3.5, 3.5, 1.5, 1.5], k=1)
            db.update("character", "wornactskill", ID, a[0])
            db.update_list("character", "actskills", ID, a)
            return f"<@{ID}> has obtained the active skill {a[0]}. You have directly worn it."
        elif m.lower() == "passive":
            b = random.choices(passive, weights=[30, 30, 10, 10, 5, 5, 3.25, 3.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], k=1)
            db.update("character", "wornpassskill", ID, b[0])
            db.update_list("character", "passskills", ID, b)
            return f"<@{ID}> has obtained the passive skill {b[0]}. You have directly worn it."
    else:
        return "You didn't create a character yet."

def skillafif(ID, m): #for testing purposes
    if existing_char(ID) != None:
        if m.lower() == "passive":
            a = "Sin of Gluttony[Mythic]"
            db.update("character", "wornpasskill", ID, a)
            a = list(a)
            db.update_list("character", "passskills", ID, a)
            return f"You are the finest being and thus deserve this divine skill {a}"
        elif m.lower() == "active":
            b = "Divine Punishment[Mythic]"
            db.update("character", "wornactskill", ID, b)
            b = list(b)
            db.update_list("character", "passskills", ID, b)
            return f"You are the finest being and thus deserve this divine skill {b}"
    else:
        return "You didn't create a character yet."

def statpoints(ID):
    if existing_char(ID) != None:
        a = db.select("character", "statpoints", ID)
        return a
    else:
        return None

def add_mana(ID): #only for testing purposes
    if existing_char(ID) != None:
        if db.select("character", "curmana", ID) < db.select("character", "mana", ID):
            max_stamina = db.select("character", "mana", ID)
            db.update("character", "curmana", ID, max_stamina)
            return "You are full mana now."
        else:
            return "You are already full mana."
    else:
        return "You do not have a character yet. Use ^start to start your adventure."

def add_hp(ID): #only for testing purposes
    if existing_char(ID) != None:
        if db.select("character", "curhp", ID) < db.select("character", "hp", ID):
            max_stamina = db.select("character", "hp", ID)
            db.update("character", "curhp", ID, max_stamina)
            return "You are full hp now."
        else:
            return "You are already full hp."
    else:
        return "You do not have a character yet. Use ^start to start your adventure."
def use_statpoints(ID, m):
    if m.lower() == "no":
        return None
    elif m.lower() == "yes":
        return f"You currently have {db.select('character', 'curhp',ID)}/{db.select('character', 'hp',ID)} hp , {db.select('character', 'ad',ID)} strength, {db.select('character', 'ap',ID)} intelligence, {db.select('character', 'spd',ID)} agility and {db.select('character', 'curmana',ID)}/{db.select('character', 'mana',ID)} mana. The stat you choose will get 5 of your free points and if you have more than 5 free points, please use the command again. Which stat do you choose?"
    else:
        return None

def chosen_statpoint(ID, m):
    m = m.lower()
    if m == "hp" or m=="strength" or m=="agility" or m=="intelligence" or m=="wisdom":
        if m =="hp":
            a = db.select('character', 'hp',ID)
            b = db.select('character', 'curhp', ID)
            c = db.select('character', 'statpoints',ID)
            db.update("character", "curhp", ID, a+5)
            db.update("character", "hp", ID, b+5)
            db.update("character", "statpoints", ID,c-5 )
            return "You have put 5 points into hp"
        elif m =="strength":
            a = db.select('character', 'ad', ID)
            b = db.select('character', 'statpoints',ID)
            db.update("character", "ad", ID, a+5)
            db.update("character", "statpoints", ID,b-5 )
            return "You have put 5 points into strength"
        elif m == "agility":
            a = db.select('character', 'spd', ID)
            b = db.select('character', 'statpoints', ID)
            db.update("character", "spd", ID, a + 5)
            db.update("character", "statpoints", ID, b - 5)
            return "You have put 5 points into speed"
        elif m == "intelligence":
            a = db.select('character', 'ap', ID)
            b = db.select('character', 'statpoints', ID)
            db.update("character", "ap", ID, a + 5)
            db.update("character", "statpoints", ID, b - 5)
            return "You have put 5 points into intelligence"
        elif m == "wisdom":
            a = db.select('character', 'mana', ID)
            b = db.select('character', 'statpoints', ID)
            db.update("character", "mana", ID, a + 5)
            db.update("character", "statpoints", ID, b - 5)
            return "You have put 5 points into wisdom"
        else:
            return "Wrong answer. Please do ^statpoints again if you wish to level up a stat."

def stats(ID):
    if existing_char(ID) != None:
        return f"You currently have {db.select('character', 'curhp',ID)}/{db.select('character', 'hp',ID)} hp , {db.select('character', 'ad',ID)} strength, {db.select('character', 'ap',ID)} intelligence, {db.select('character', 'spd',ID)} agility and {db.select('character', 'curmana',ID)}/{db.select('character', 'mana',ID)} mana."
    else:
        return f"You don't have a character."

def floor(ID):
    if existing_char(ID) != None:
        if db.select('character', 'highestfloor', ID) == 1:
            return f"You currently only have access to the first floor: The Amethyst Forest, please save the Amethyst Forest by beating the monstrous Orc Chef to access the next floor."
        else:
            a = db.select('character', 'highestfloor', ID)
            return f"Your highest floor is floor {a}, please beat the {db.select('character', 'boss', ID)} to reach higher floors."
    else:
        return "You don't have a character."

def enough_hp(ID):
    if db.select("character", "curhp", ID)>0:
        return "nice"
    else:
        return None

def monsterrecog(ID):
    m = db.select("character", "curfloor", ID)
    with open("Floors.json", "r") as f:
        txt = json.load(f)
        floor = str(m)
        if floor in txt.keys():
            randmon = [txt[floor][2][0], txt[floor][3][0], txt[floor][4][0], txt[floor][5][0]]
            monster = random.choice(randmon)
            c = len(txt[floor])
            for i in range(2, c):
                if monster in txt[floor][i]:
                    db.new_monster(monster, ID, txt[floor][i][1], txt[floor][i][2], txt[floor][i][3])
                    return f"You will be fighting a {monster}"

def floorboss(ID):
    m = db.select("character", "boss", ID)
    curfloor = db.select("character", "curfloor", ID)
    with open("Boss.json", "r") as f:
        txt = json.load(f)
        if m == txt["Boss"][curfloor-1][0]:
            db.new_boss(m,ID, txt["Boss"][curfloor-1][7], txt["Boss"][curfloor-1][1], txt["Boss"][curfloor-1][2], txt["Boss"][curfloor-1][3], txt["Boss"][curfloor-1][4], txt["Boss"][curfloor-1][5], txt["Boss"][curfloor-1][6])

def welcomemessage(ID):
    return db.select("boss", "welcome", ID)

def hp(ID):
    try:
        if db.select("character", "curhp", ID) == 0:
            return "1"
        elif db.select("monster","hp", ID) == 0:
            return "2"
        else:
            return None
    except TypeError:
        return "3"

def actskillmana(ID):
    with open("Skills.json", "r") as file:
        b = json.load(file)
        c = len(b["Actives"])
        for i in range(0, c):
            if db.select("character", "wornactskill", ID) in b["Actives"][i][0]:
                return int(b["Actives"][i][3])

def enoughmana(ID):
    p = actskillmana(ID)
    if db.select("character", "curmana", ID) >= p:
        return "yes"
    else:
        return None

def useskill(ID):
    with open("Skills.json", "r") as file:
        b = json.load(file)
        c = len(b["Actives"])
        for i in range(0, c):
            if b["Actives"][i][0] == db.select("character", "wornactskill", ID):
                dmg = round(((int(b["Actives"][i][1])/100)*db.select("character", "ad", ID))+((int(b["Actives"][i][2])/100)*db.select("character", "ap", ID)))
                return dmg

def fight(ID):
    return f"You are fighting against a {db.select('monster','name', ID)}.Would you like to attack with your Sword, use a Skill or Quit?Quitting means losing all your hp. Please answer with either Sword,Skill or Quit."

def automode2(ID, m):
    h = existing_char(ID)
    if h!= None:
        if hp(ID) == None:
            if enoughmana(ID)!= None:
                if m.lower() == "sword":
                    sword_dmg = db.select("monster", "hp", ID) - (db.select("character", "ap", ID)+db.select("character", "ad", ID))
                    db.update("monster", "hp", ID, sword_dmg)
                    if db.select("monster", "hp", ID) <= 0:
                        db.update("monster", "hp", ID, 0)
                        name = db.select("monster", "name", ID)
                        xp = db.select("character", "curfloor", ID) * 450
                        db.del_monster(ID)
                        return f"You have dealt {db.select('character', 'ap', ID)+db.select('character', 'ad', ID)}dmg with your sword and killed the {name}.{gold_monster(ID)} gold. {getexp(ID, xp)}"
                    else:
                        return f"You have dealt {db.select('character', 'ap', ID)+db.select('character', 'ad', ID)} dmg with your sword. {db.select('monster', 'name', ID)} has {db.select('monster', 'hp', ID)}hp left."
                elif m.lower() == "skill":
                    skill_dmg = db.select("monster", "hp", ID) - useskill(ID)
                    db.update("monster", "hp", ID, skill_dmg)
                    skill_mana = db.select("character", "curmana", ID) - actskillmana(ID)
                    db.update("character", "curmana", ID, skill_mana)
                    if db.select("monster", "hp", ID) <= 0:
                        db.update("monster", "hp", ID, 0)
                        name = db.select("monster", "name", ID)
                        xp = db.select("character", "curfloor", ID) * 450
                        db.del_monster(ID)
                        return f"You have dealt {useskill(ID)}dmg with {db.select('character', 'wornactskill', ID)} and killed the {name}.{gold_monster(ID)} gold . {getexp(ID, xp)}"
                    else:
                        return f"You have dealt {useskill(ID)}dmg with {db.select('character', 'wornactskill', ID)}. {db.select('monster', 'name', ID)} has {db.select('monster', 'hp', ID)}hp left."
                elif m.lower() == "quit":
                    db.update("character", "curhp", ID, 0)
                    db.del_monster(ID)
                    return f"You have given up thus you have lost all your hp."
                else:
                    db.update("character", "curhp", ID, 0)
                    db.del_monster(ID)
                    return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."


            else:
                if m.lower() == "sword":
                    sword_dmg = db.select("monster", "hp", ID) - (db.select("character", "ap", ID) + db.select("character", "ad", ID))
                    db.update("monster", "hp", ID, sword_dmg)
                    if db.select("monster", "hp", ID) <= 0:
                        db.update("monster", "hp", ID, 0)
                        name = db.select("monster", "name", ID)
                        xp = db.select("character", "curfloor", ID) * 450
                        db.del_monster(ID)
                        return f"You have dealt {db.select('character', 'ap', ID)+db.select('character', 'ad', ID)}dmg with your sword and killed the {name}.{gold_monster(ID)} gold. {getexp(ID, xp)}"
                    else:
                        return f"You have dealt {db.select('character', 'ap', ID)+db.select('character', 'ad', ID)} dmg with your sword.  {db.select('monster', 'name', ID)} has {db.select('monster', 'hp', ID)}hp left."
                elif m.lower() == "quit":
                    db.update("character", "curhp", ID, 0)
                    db.del_monster(ID)
                    return f"You have given up thus you have lost all your hp"
                else:
                    db.update("character", "curhp", ID, 0)
                    db.del_monster(ID)
                    return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."



        else:
            return f"You have no hp"
    else:
        return "You don't have a character yet"

def monsteratt(ID):
    monst_dmg = db.select("character", "curhp", ID) - db.select("monster", "dmg", ID)
    db.update("character", "curhp", ID, monst_dmg)
    if db.select("character", "curhp", ID)<= 0:
        db.update("character", "curhp", ID, 0)
        dmg = db.select("monster", "dmg", ID)
        name = db.select("monster", "name", ID)
        db.del_monster(ID)
        return f"{name} attacked back. You have lost {dmg}hp and died."
    else:
        name = db.select("monster", "name", ID)
        return f"{name} attacked back. You have lost {db.select('monster', 'dmg', ID)}hp."

def currentinfo(ID):
    h = existing_char(ID)
    if h!=None:
        return f"Your current informations are: Name : {db.select('character','name',ID)}, Level : {db.select('character','level',ID)}, Gender : {db.select('character','gender',ID)}, Race : {db.select('character','race',ID)}, Title : {db.select('character','titleequipped',ID)}, Highest Floor reached : Floor {db.select('character','highestfloor',ID)}"
    else:
        return "You don't have a character yet."

def valuecheck(k):
    try:
        val = int(k)
        return val
    except ValueError:
        return None

def floormonsters(ID, m):
    h = existing_char(ID)
    if h!= None:
        if  m <= db.select("character", "highestfloor", ID):
            with open("Floors.json", "r") as f:
                txt = json.load(f)
                floor = str(m)
                if floor in txt.keys():
                    return f"Monsters of Floor {floor} are : {txt[floor][2][0]}, {txt[floor][3][0]}, {txt[floor][4][0]} and {txt[floor][5][0]}"
                else:
                    return "Soon to come"
        else:
            return "You have not reached that floor yet thus you cannot see its informations."
    else:
        return "You don't have a character"

def Yatori(ID):
    h = existing_char(ID)
    if h != None:
        if ID == 257115950623490049:
            if "God of Creation" not in db.select_list("character", "titleavailable", ID) and "God of Creation" != db.select("character", "titleequipped", ID):
                add_title = db.select_list("character", "titleavailable", ID)
                add_title.append("God of Creation")
                db.update_list("character", "titleavailable", ID, add_title)
                db.update("character", "race", ID, "God")
                return "You have gotten your lost strength back"
            else:
                return "You already are divine, Master"

        else:
            return "You are not the creator of this bot"
    else:
        return "You have not created a character yet"

def current_titles_available(ID):
    h = existing_char(ID)
    if h!= None:
        if len(db.select_list("character", "titleavailable", ID))>=1:
            titles_in_order = [f"- {x}" for x in db.select_list("character", "titleavailable", ID)]
            c = "\n".join(titles_in_order)
            return f"The titles available to be equipped are: {c}"
        else:
            return "You don't have a title except the one which is equipped"
    else:
        return"You don't have a character yet"

def weartitle(ID, m):
    if m in db.select_list("character", "titleavailable", ID):
        cur_title = db.select("character", "titleequipped", ID)
        available = db.select_list("character", "titleavailable", ID)
        available.append(cur_title)
        available.remove(m)
        db.update_list("character", "titleavailable", ID, available)
        db.update("character", "titleequipped", ID, m)
        #db.update_list("character", "titleavailable", ID, cur_title)
        #db.update("character", "titleequipped", ID, m)
        #b = db.select_list("character", "titleavailable", ID)
        #b.remove(db.select("character", "titleequipped", ID))
        #db.update_list("character", "titleavailable", ID, b)
        return f"The title {db.select('character', 'titleequipped', ID)} has been equipped"
    else:
        return f"This is not an available title."

def skills(ID):
    h = existing_char(ID)
    if h!= None:
        if db.select_list("character", "actskills", ID) != [""] and db.select_list("character", "passskills", ID) != [""]:
            actives = [f"--{x}" for x in db.select_list("character", "actskills", ID)]
            passives = [f"--{y}" for y in db.select_list("character", "passskills", ID)]
            passives2 = "".join(passives)
            actives2 = "".join(actives)
            return f"The active skills available to you are: \n {actives2} \n The passive skills available to you are: \n {passives2}"
        elif db.select_list("character", "actskills", ID)!= [""] and db.select_list("character", "passskills", ID)==[""]:
            actives = [f"--{x}" for x in db.select_list("character", "actskills", ID)]
            print(db.select_list("character", "actskills", ID))
            print(actives)
            actives2 = "".join(actives)
            print(actives2)
            return f"The active skills available to you are: \n {actives2} \n You have no passive skill."
        elif db.select_list("character", "passskills", ID)!= [""] and db.select_list("character", "actskills", ID)==[""]:
            passives = [f"--{y}" for y in db.select_list("character", "passskills", ID)]
            passives2 = "".join(passives)
            return f"The passive skills available to you are: \n {passives2} \n You have no active skill"
        else:
            return "You don't have a skill yet. Get your first skill using ^learnskill"
    else:
        return "You don't have a character yet."

def titleon(ID):
    h = existing_char(ID)
    if h!= None:
        if db.select("character", "titleequipped", ID) == "God of Creation":
            return f" You currently have the title {db.select('character', 'titleequipped', ID)} equipped , this title can only be given to the creator of this bot."
        elif db.select('character', 'titleequipped', ID) == "Beginner":
            return f" You currently have the title {db.select('character', 'titleequipped', ID)} equipped. Thank you for trying out this game."
        else:
            return f" You currently have the title {db.select('character', 'titleequipped', ID)} equipped. Further details on titles coming soon."
    else:
        return "You don't have a character yet."

def gold_monster(ID):
    m = db.select('character', 'curfloor', ID)
    radon = random.randrange(0,250)
    money = 300*m + radon*m
    bal = db.select('character', 'gold', ID) + money
    db.update("character", "gold", ID, bal)
    return f"You have obtained {money}"

def getbal(ID):
    h = existing_char(ID)
    if h!= None:
        return f"You currently have {db.select('character', 'gold', ID)} Gold"
    else:
        return "You don't have a character yet."

def shop(ID, m):
    h = existing_char(ID)
    if h!= None:
        if m.lower() == "life potion":
            if db.select('character', 'gold', ID) >= 600:
                inventory = db.select_list("character", "inventory", ID)
                inventory.append("Life Potion")
                db.update_list("character", "inventory", ID, inventory)
                new_gold = db.select("character", "gold", ID) - 600
                db.update("character", "gold", ID, new_gold)
                return f"You have obtained a Life Potion. You have {db.select('character', 'gold', ID)} Gold remaining."
            if db.select('character', 'gold', ID) < 600:
                return "You do not have enough Gold."
        elif m.lower() == "stamina potion":
            if db.select('character', 'gold', ID) >= 600:
                inventory = db.select_list("character", "inventory", ID)
                inventory.append("Stamina Potion")
                db.update_list("character", "inventory", ID, inventory)
                new_gold = db.select("character", "gold", ID) - 600
                db.update("character", "gold", ID, new_gold)
                return f"You have obtained a Stamina Potion. You have {db.select('character', 'gold', ID)} Gold remaining."
            if db.select('character', 'gold', ID)<600:
                return "You do not have enough Gold."
        else:
            return "This item is not in the shop"
    else:
        return "You do not have a character yet."

def use(ID, m):
    h = existing_char(ID)
    if h!=None:
        if m.lower() == "life potion":
            m = "Life Potion"
            if m in db.select_list("character", "inventory", ID):
                if (db.select("character", "hp", ID)-db.select("character", "curhp", ID)) < 50 and (db.select("character", "hp", ID)-db.select("character", "curhp", ID)) != 0:
                    gainedhp = db.select("character", "hp", ID)-db.select("character", "curhp", ID)
                    max_hp = db.select("character", "hp", ID)
                    db.update("character", "curhp", ID, max_hp)
                    inventory = db.select_list("character", "inventory", ID)
                    new_inventory = inventory.remove("Life Potion")
                    db.update_list("character", "inventory", ID, new_inventory)
                    return f"{gainedhp} hp have been added, you are now full health."
                elif (db.select("character", "hp", ID)-db.select("character", "curhp", ID))>=50:
                    more_hp = db.select("character", "curhp", ID)+50
                    db.update("character", "curhp", ID, more_hp)
                    inventory = db.select_list("character", "inventory", ID)
                    new_inventory = inventory.remove("Life Potion")
                    db.update_list("character", "inventory", ID, new_inventory)
                    return f"50 hp have been added. You currently have {db.select('character', 'curhp', ID)}/{db.select('character', 'hp', ID)}hp."
                elif (db.select("character", "hp", ID)-db.select("character", "curhp", ID)) == 0:
                    return "You are already full health."
        elif m.lower() == "stamina potion":
            m = "Stamina Potion"
            if m in db.select_list("character", "inventory", ID):
                if (db.select("character", "mana", ID)-db.select("character", "curmana", ID)) < 50 and (db.select("character", "mana", ID)-db.select("character", "curmana", ID)) != 0:
                    gained_stamina = db.select("character", "mana", ID) - db.select("character", "curmana", ID)
                    max_stamina = db.select("character", "mana", ID)
                    db.update("character", "curmana", ID, max_stamina)
                    inventory = db.select_list("character", "inventory", ID)
                    new_inventory = inventory.remove("Stamina Potion")
                    db.update_list("character", "inventory", ID, new_inventory)
                    return f"{gained_stamina}stamina has been added, you are now at max Stamina"
                elif (db.select("character", "mana", ID)-db.select("character", "curmana", ID))>=50:
                    more_stamina = db.select("character", "curmana", ID) + 50
                    db.update("character", "curmana", ID, more_stamina)
                    inventory = db.select_list("character", "inventory", ID)
                    new_inventory = inventory.remove("Stamina Potion")
                    db.update_("character", "inventory", ID, new_inventory)
                    return f"50 Stamina has been added. You currently have {db.select('character', 'curmana', ID)}/{db.select('character', 'mana', ID)}stamina"
                elif (db.select("character", "mana", ID)-db.select("character", "curmana", ID)) == 0:
                    return "You already are at max Stamina."
        else:
            return "You do not have that item in your inventory."
    else:
        return "You do not have a character yet."

def hp2(ID):
    try:
        if db.select("character", "curhp", ID) == 0 and db.select("boss", "hp1", ID) == 0:
            return "1"
        elif db.select("character", "curhp", ID) == 0 and db.select("boss", "hp2", ID) == 0:
            return "5"
        elif db.select("character", "curhp", ID) ==0:
            return "3"
        elif db.select("boss", "hp2", ID) == 0:
            return "4"
        else:
            return None
    except TypeError:
        return "5"

def automode3(ID, m):   #for floorboss
    h = existing_char(ID)
    if h!= None:
        if db.select("boss", "mode", ID) == 1:
            if hp2(ID) == None:
                if enoughmana(ID)!= None:
                    if m.lower() == "sword":
                        new_hp1 = db.select("boss", "hp1", ID) -  (db.select("character", "ad", ID)+db.select("character", "ap", ID))
                        db.update("boss", "hp1", ID, new_hp1)
                        if db.select("boss", "hp1", ID) <= 0:
                            db.update("boss", "hp1", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 2)
                            return f"{name} starts becoming redder and redder, {name} has entered the enraged state. His stats will exponentially increase!"
                        else:
                            return f"You have dealt {(db.select('character', 'ad', ID)+db.select('character', 'ap', ID))} dmg with your sword. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp1', ID)}hp left."
                    elif m.lower() == "skill":
                        new_hp1 = db.select("boss", "hp1", ID) - useskill(ID)
                        db.update("boss", "hp1", ID, new_hp1)
                        new_curmana = db.select("character", "curmana", ID) - actskillmana(ID)
                        db.update("character", "curmana", ID, new_curmana)
                        if db.select("boss", "hp1", ID) <= 0:
                            db.update("boss", "hp1", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 2)
                            return f"{name} starts becoming redder and redder, {name} has entered the enraged state. His stats will exponentially increase!"
                        else:
                            return f"You have dealt {useskill(ID)} dmg with {db.select('character', 'wornactskill', ID)}. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp1', ID)}hp left."
                    elif m.lower() == "quit":
                        db.del_boss(ID)
                        db.update("character", "curhp", ID, 0)
                        return f"You have given up thus you have lost all your hp."
                    else:
                        db.update("character", "curhp", ID, 0)
                        db.del_boss(ID)
                        return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."


                else:
                    if m.lower() == "sword":
                        new_hp1 = db.select("boss", "hp1", ID) - (db.select("character", "ad", ID) + db.select("character", "ap", ID))
                        db.update("boss", "hp1", ID, new_hp1)
                        if db.select("boss", "hp1", ID) <= 0:
                            db.update("boss", "hp1", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 2)
                            return f"{name} starts becoming redder and redder, {name} has entered the enraged state. "
                        else:
                            return f"You have dealt {(db.select('character', 'ad', ID)+db.select('character', 'ap', ID))} dmg with your sword. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp1', ID)}hp left."
                    elif m.lower() == "quit":
                        db.del_boss(ID)
                        db.update("character", "curhp", ID, 0)
                        return f"You have given up thus you have lost all your hp."
                    else:
                        db.update("character", "curhp", ID, 0)
                        db.del_boss(ID)
                        return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."
            else:
                return f"You have no hp"
        elif db.select("boss", "mode", ID) == 2:
            if hp2(ID) == None:
                if enoughmana(ID)!= None:
                    if m.lower() == "sword":
                        new_hp2 = db.select("boss", "hp2", ID) - (db.select("character", "ad", ID) + db.select("character", "ap", ID))
                        db.update("boss", "hp2", ID, new_hp2)
                        if db.select("boss", "hp2", ID) <= 0:
                            db.update("boss", "hp2", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 3)
                            return f"Congratulations, you have defeated the {name}. {dropboss(ID)}\n{bossdefeat(ID)}{floor_welcome(ID)}"
                        else:
                            return f"You have dealt {(db.select('character', 'ad', ID)+db.select('character', 'ap', ID))} dmg with your sword. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp2', ID)}hp left."
                    elif m.lower() == "skill":
                        new_hp2 = db.select("boss", "hp2", ID) - useskill(ID)
                        db.update("boss", "hp1", ID, new_hp2)
                        new_curmana = db.select("character", "curmana", ID) - actskillmana(ID)
                        db.update("character", "curmana", ID, new_curmana)
                        if db.select("boss", "hp2", ID) <= 0:
                            db.update("boss", "hp2", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 3)
                            return f"Congratulations, you have defeated the {name}. {dropboss(ID)}\n{bossdefeat(ID)}{floor_welcome(ID)}"
                        else:
                            return f"You have dealt {useskill(ID)} dmg with {db.select('character', 'wornactskill', ID)}. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp2', ID)}hp left."
                    elif m.lower() == "quit":
                        db.del_boss(ID)
                        db.update("character", "curhp", ID, 0)
                        return f"You have given up thus you have lost all your hp."
                    else:
                        db.update("character", "curhp", ID, 0)
                        db.del_boss(ID)
                        return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."
                else:
                    if m.lower() == "sword":
                        new_hp2 = db.select("boss", "hp2", ID) - (db.select("character", "ad", ID) + db.select("character", "ap", ID))
                        db.update("boss", "hp2", ID, new_hp2)
                        if db.select("boss", "hp2", ID) <= 0:
                            db.update("boss", "hp2", ID, 0)
                            name = db.select("boss", "name", ID)
                            db.update("boss", "mode", ID, 3)
                            return f"Congratulations, you have defeated the {name}. {dropboss(ID)}\n{bossdefeat(ID)}{floor_welcome(ID)}"
                        else:
                            return f"You have dealt {(db.select('character', 'ad', ID)+db.select('character', 'ap', ID))} dmg with your sword. {db.select('boss', 'name', ID)} has {db.select('boss', 'hp2', ID)}hp left."
                    elif m.lower() == "quit":
                        db.del_boss(ID)
                        db.update("character", "curhp", ID, 0)
                        return f"You have given up thus you have lost all your hp."
                    else:
                        db.update("character", "curhp", ID, 0)
                        db.del_boss(ID)
                        return f"You have answered something else thus I consider that as you quitting. You have lost all your hp."


            else:
                return f"You have no hp"
        elif db.select("boss", "mode", ID) == 3: #it does not reach here though
            pass

    else:
        return "You don't have a character yet"

def bossatt(ID):
    monst_dmg = db.select("character", "curhp", ID) - db.select("boss", "dmg1", ID)
    db.update("character", "curhp", ID, monst_dmg)
    if db.select("character", "curhp", ID) <= 0:
        db.update("character", "curhp", ID, 0)
        dmg1 = db.select("boss", "dmg1", ID)
        bossname = db.select("boss", "name", ID)
        db.del_boss(ID)
        return f"{bossname} attacked back. You have lost {dmg1}hp and died."
    else:
        return f"{db.select('boss', 'name', ID)} attacked back. You have lost {db.select('boss', 'dmg1', ID)}hp."

def bossattmad(ID):
    monst_dmg = db.select("character", "curhp", ID) - db.select("boss", "dmg2", ID)
    db.update("character", "curhp", ID, monst_dmg)
    if db.select("character", "curhp", ID) <= 0:
        db.update("character", "curhp", ID, 0)
        dmg2 = db.select("boss", "dmg2", ID)
        bossname = db.select("boss", "name", ID)
        db.del_boss(ID)
        return f"{bossname} attacked back. You have lost {dmg2}hp and died."
    else:
        return f"{db.select('boss', 'name', ID)} attacked back. You have lost {db.select('boss', 'dmg2', ID)}hp."

def dropboss(ID):
    with open("Drop.json", "r") as f:
        txt = json.load(f)
        bossname = db.select("boss", "name", ID)
        if bossname in txt:
            db.update_list("character", "inventory", ID, [txt[bossname][0]])
            db.update_list("character", "titleavailable", ID, [txt[bossname][1]])
            return f"You have received the item: {txt[bossname][0]} and the title: {txt[bossname][1]}.{getexp(ID, txt[bossname][2])}{getgold(ID, txt[bossname][3])}"

def getexp(ID, amount): #make a func for gold too
    xp = db.select("character", "experience", ID)
    db.update("character", "experience", ID, xp + amount)
    obtained_statpoints = 0
    if db.select("character", "experience", ID) < db.select("character", "experiencereq", ID):
        return f"You have obtained {amount} experience points."
    while db.select("character", "experience", ID) >= db.select("character", "experiencereq", ID):
        newexp = db.select("character", "experience", ID)-db.select("character", "experiencereq", ID)
        db.update("character", "experience", ID, newexp)
        newexpreq = db.select("character", "experiencereq", ID)*1.5
        db.update("character", "experiencereq", ID, newexpreq)
        newlevel = db.select("character", "level", ID)+1
        db.update("character", "level", ID, newlevel)
        new_stat_points = db.select("character", "statpoints", ID) + 5
        db.update("character", "statpoints", ID, new_stat_points)
        obtained_statpoints += 5
        heal_user = db.select("character", "hp", ID)
        db.update("character", "curhp", ID, heal_user)
        full_mana = db.select("character", "mana", ID)
        db.update("character", "curmana", ID, full_mana)
    return f" You have obtained {amount} experience points. You are now level {db.select('character', 'level', ID)} thus gaining {obtained_statpoints} free stat points. Use them with ^statpoints. "

def getgold(ID, amount):
    new_bal = db.select("character", "gold", ID) + amount
    db.update("character", "gold", ID, new_bal)
    return f" You have obtained {amount}gold as a bonus loot!"

def floor_welcome(ID):
    return f"\nWelcome to Floor {db.select('character', 'curfloor', ID)}: {db.select('character', 'curfloorname', ID)} "

def bossdefeat(ID):
    new_highest_floor = db.select('character', 'highestfloor', ID)+1
    db.update('character', 'highestfloor', ID, new_highest_floor)
    db.update('character', 'curfloor', ID, new_highest_floor)
    db.del_boss(ID)
    with open("Floors.json", "r") as f:
        txt = json.load(f)
        floor = str(new_highest_floor)
        if floor in txt.keys():
            new_boss = txt[floor][6][0]
            db.update('character', 'boss', ID, new_boss)
            new_curfloorname = txt[floor][0][0]
            db.update('character', 'curfloorname', ID, new_curfloorname)
            return txt[floor][1][0]
