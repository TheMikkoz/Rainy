#Removes "Visit pygame forum" text !!Need to be before import pygame
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#Import 
import pygame, random, json, psutil, urllib3, re, ast, threading
from pygame.locals import *

#Class
class Main:
    def Quit():
        try:
            run = False
            pygame.quit()
        except:
            quit()

    def Name(name):
        name = name.lower()
        re.sub(r'[^\w]', ' ', name)
        newName = ''
        if len(name) >= 5:
            for i in range(len(name)):
                if i <= 4:
                    newName = newName + name[i]
            name = newName
        if len(name) <= 2:
            for i in range(3 - len(name)):
                name += str(random.randint(0,9))
        return name

    def json():
        with open('assets/settings.json', 'w') as outfile:
            json.dump(({"Volume":{"Music":musicVolume,"FX":effectVolume},"Player":{"Name":re.sub(r'[^\w]', ' ', myName)}}), outfile)
                
    def addEnemy(x, y, var):
        enemies.append([x, y, imgDic["enemies"][var]["Hp"], imgDic["enemies"][var]["Height"], imgDic["enemies"][var]["Width"], imgDic["enemies"][var],imgDic["enemies"][var]["Points"]])

    def http_get(url):
        try:
            http = urllib3.PoolManager(num_pools=50, maxsize=50)
            result = {"url": url, "data": http.request('GET', url, timeout=1).data.decode()}
            return result["data"]
        except:
            print(" -\n - No internet - \n -")

    #Threading <
    def thread1():
        global top
        data = Main.http_get('http://dreamlo.com/lb/5f04b7fd377eda0b6ccc264b/json')
        data = ast.literal_eval(data)
        for i in range(5):
            try:
                top[i] = data["dreamlo"]["leaderboard"]["entry"][i]
            except:
                top[i] = {"name":"00000", "score":"0"}
            
        top[i]["name"] = Main.Name(top[i]["name"])

    def thread2():
        data = Main.http_get('http://dreamlo.com/lb/pIT5fNAznUCd_zXvuy72dwihLgPcXhxkWW9VapRU9wOQ/add/' + myName +'/' + str(scorePoints))
    #>

if __name__ == "__main__":

    #Fix sound delay
    pygame.mixer.pre_init(44100, -16, 1, 512)

    #Leaderboard!! http://dreamlo.com/lb/pIT5fNAznUCd_zXvuy72dwihLgPcXhxkWW9VapRU9wOQ

    #Init
    pygame.init()
    pygame.mixer.init()
    #Hide Mouse
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    #Shorten
    sound = pygame.mixer.Sound
    clock = pygame.time.Clock()

    def scale(img, size):
        return pygame.transform.scale(img, size)

    def image(png):
        img = pygame.image.load("assets/" + png)
        return img

    def music(ogg):
        track = pygame.mixer.music.load("assets/" + ogg)
        return track    

    #Settings
    Title = "Rainy"
    wHeight = 800
    wWidth = 800
    wBorder = 10

    pos_x = 0
    pos_y = 0
    environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
    environ['SDL_VIDEO_CENTERED'] = '0'

    #Score number scale
    psX = 4 * 3
    psY = 5 * 3

    #Dictionaries
    imgDic = {}
    usereventDic = {}
    eventTimerDic = {}
    musicDic = {}

    try:
        musicDic = {
            "background":{
                "normal":music("sounds/music/reini_mutta_parempi.ogg"),
            },
            "Sounds":{
                "Hit":sound("assets/sounds/vesipisara2.ogg"),
                "Enemy":sound("assets/sounds/hurt.ogg"),
                "Defeat":sound("assets/sounds/kuolema.ogg"),
                "Healthboost":sound("assets/sounds/hp_aani.ogg"),
                "Powerup":sound("assets/sounds/Powerup.ogg"),
                "Hover":sound("assets/sounds/hover.ogg"),
                "Click":sound("assets/sounds/click.ogg")
            },
        }

        imgDic = {
            "icon":image("Rainyicon.png"),
            "Cursor":image("cursor.png"),

            "defeat":image("defeat.png"),
            "loading":image("Loading.png"), 

            "tittlescreen":image("tittlescreen.png"),
            "pressanything":{
                0:image("pressanything.png"),
                1:image("blankpress.png"),
            },
            "leaderboard":image("leaderboard.png"),
            "continue":image("continue.png"),
            "pause":{
                "BG":image("settings/bg.png"),
                "BG2":image("settings/bg2.png"),
                "x":{
                    0:image("Settings/x-1.png"),
                    1:image("Settings/x-0.png"),

                },
                "plus":image("settings/plus.png"),
                "Border":{
                    0:image("Settings/border0.png"),
                    1:image("Settings/border1.png"),
                },
                "BorderS":{
                    0:image("Settings/border0-S.png"),
                    1:image("Settings/border1-S.png"),
                },
                "Settings":{
                    0:image("Settings/Settings.png"),
                    1:image("Settings/Settings2.png"),
                },
                "Slider":image("Settings/Slide.png"),
                "SlideButton":image("Settings/SlideButton.png"),
                "Volume":image("Settings/Volume.png"),
                "Music":image("Settings/Music.png"),
                "Credits":{
                    0:image("Settings/Credits.png"),
                    1:image("Settings/Credits2.png")
                },
            },

            "background":image("bg.png"),
            "nameBG":image("nameBG.png"),

            "ammo":{
                0:image("ammo/ammo.png"),
                1:image("ammo/ammo2.png"),
            },

            #hearts
            "fheart":image("health/fullHeart.png"),
            "bheart":image("health/brokenHeart.png"),
            "addHealth": {
                0:image("health/addHealth1.png"),
                1:image("health/addHealth2.png"),
            },

            "powerup":{
                0:image("powerup/powerup0.png"),
                1:image("powerup/powerup1.png"),
                2:image("powerup/powerup2.png"),
                3:image("powerup/powerup3.png"),
                4:image("powerup/powerup4.png"),
            },

            "player":{
                0:image('character/Cloud.png'),
                1:image('character/Cloud-2.png'),
                2:image("character/cloud-bigwater-1.png"),
                3:image("character/cloud-bigwater-2.png"),
                4:image("character/cloud-lightning-1.png"),
                5:image("character/cloud-lightning-2.png"),
                6:image("character/cloud-lightning2-1.png"),
                7:image("character/cloud-lightning2-2.png"),
            },
            
            "enemies":{
                0:{
                    0:image('enemy/co2-1.png'),
                    1:image('enemy/co2-2.png'),
                    "Height":32,
                    "Width":32,
                    "Hp":10,
                    "Points":20
                },
                1:{
                    0:image('enemy/co2-2-1.png'),
                    1:image('enemy/co2-2-2.png'),
                    "Height":32,
                    "Width":32,
                    "Hp":5,
                    "Points":10
                },
                2:{
                    0:image('enemy/Dityppioksidi1.png'),
                    1:image('enemy/Dityppioksidi2.png'),
                    "Height":32,
                    "Width":32,
                    "Hp":20,
                    "Points":30
                },
                "Boss1":{
                    0:image('enemy/Boss2a1.png'),
                    1:image('enemy/Boss2a2.png'),
                }
            },
            "scoreDic":{
                0:image("score/0.png"),
                1:image("score/1.png"),
                2:image("score/2.png"),
                3:image("score/3.png"),
                4:image("score/4.png"),
                5:image("score/5.png"),
                6:image("score/6.png"),
                7:image("score/7.png"),
                8:image("score/8.png"),
                9:image("score/9.png"),
                "score":image("score/score.png")
            },
            "abc":{
                "a":image("abc/a.png"),
                "b":image("abc/b.png"),
                "c":image("abc/c.png"),
                "d":image("abc/d.png"),
                "e":image("abc/e.png"),
                "f":image("abc/f.png"),
                "g":image("abc/g.png"),
                "h":image("abc/h.png"),
                "i":image("abc/i.png"),
                "j":image("abc/j.png"),
                "k":image("abc/k.png"),
                "l":image("abc/l.png"),
                "m":image("abc/m.png"),
                "n":image("abc/n.png"),
                "o":image("abc/o.png"),
                "p":image("abc/p.png"),
                "q":image("abc/q.png"),
                "r":image("abc/r.png"),
                "s":image("abc/s.png"),
                "t":image("abc/t.png"),
                "u":image("abc/u.png"),
                "v":image("abc/v.png"),
                "w":image("abc/w.png"),
                "x":image("abc/x.png"),
                "y":image("abc/y.png"),
                "z":image("abc/z.png"),
                " ":image("abc/blank.png")
            }
        }
        #Icon
        pygame.display.set_icon(imgDic["icon"])

        #Scale images
        imgDic["background"] = scale(imgDic["background"], (800, 800))

        imgDic["defeat"] = scale(imgDic["defeat"], (65 * 10, 16 * 10))

        imgDic["loading"] = scale(imgDic["loading"], (44 * 3, 5 * 3))

        imgDic["bheart"] = scale(imgDic["bheart"], (7 * 3, 7 * 3))
        imgDic["fheart"] = scale(imgDic["fheart"], (7 * 3, 7 * 3))

        imgDic["nameBG"] = scale(imgDic["nameBG"], (43 * 3, 13 * 3))

        imgDic["tittlescreen"] = scale(imgDic["tittlescreen"], (56 * 10, 19 * 10))

        imgDic["leaderboard"] = scale(imgDic["leaderboard"], (100 * 3, 50 * 3))
        imgDic["continue"] = scale(imgDic["continue"],(45 * 4, 11 * 4))

        for abc in imgDic["abc"]:
            imgDic["abc"][abc] = scale(imgDic["abc"][abc], (5 * 3, 5 * 3))

        for i in imgDic["pressanything"]:
            imgDic["pressanything"][i] = scale(imgDic["pressanything"][i], (123 * 3, 5 * 3))

        #Pause menu
        imgDic["pause"]["BG"] = scale(imgDic["pause"]["BG"], (175*4, 175*4))
        imgDic["pause"]["BG2"] = scale(imgDic["pause"]["BG2"], (80*3, 80*3))
        RainyLogoSettings = scale(imgDic["tittlescreen"], (56 * 2, 19 * 2))
        imgDic["pause"]["Volume"] = scale(imgDic["pause"]["Volume"], (60 * 2, 14 * 2))
        imgDic["pause"]["Music"] = scale(imgDic["pause"]["Music"], (46 * 2, 14 * 2))

        imgDic["pause"]["plus"] = scale(imgDic["pause"]["plus"], (3 * 3, 3 * 3))
        
        imgDic["pause"]["Slider"] = scale(imgDic["pause"]["Slider"], (64 * 2, 16 * 2))
        imgDic["pause"]["SlideButton"] = scale(imgDic["pause"]["SlideButton"], (21 * 2, 14 * 2))
        for num in range(2):
            imgDic["pause"]["x"][num] = scale(imgDic["pause"]["x"][num], (16 * 2, 16 * 2))
            imgDic["pause"]["Settings"][num] = scale(imgDic["pause"]["Settings"][num], (90 * 2 , (17 - num)* 2 ))
            imgDic["pause"]["Credits"][num] = scale(imgDic["pause"]["Credits"][num], (57 * 2, 14 * 2))
            imgDic["pause"]["Border"][num] = scale(imgDic["pause"]["Border"][num], (8 * 3, 8 * 3))
            imgDic["pause"]["BorderS"][num] = scale(imgDic["pause"]["BorderS"][num], (30 * 3, 8 * 3))

        bigwater = scale(imgDic["ammo"][0], ( 7* 2, 11*2))

        for abc in imgDic["scoreDic"]:
            if abc == "score":
                imgDic["scoreDic"][abc] = scale(imgDic["scoreDic"][abc], (27*3, 5*3))
            else:
                imgDic["scoreDic"][abc] = scale(imgDic["scoreDic"][abc], (psX, psY))
        
        #Window
        win = pygame.display.set_mode((wWidth, wHeight), pygame.NOFRAME)
        pygame.display.set_caption(Title)


        #Events (Must be between 0-32)
        usereventDic = {
            "animation":pygame.USEREVENT + 1, # 25
            "enemy":pygame.USEREVENT + 2, # 26
            "ammo":pygame.USEREVENT + 3, # 27
            "powerupLast":pygame.USEREVENT + 5, # 29
            "healthboost":pygame.USEREVENT + 6, # 30
            "tittlescreen":pygame.USEREVENT - 1, # 23
            "mouseCD":pygame.USEREVENT # 24
        }
        #Event timers
        eventTimerDic = {
            "animation":300,
            "enemy":2000,
            "ammo":100,
            "powerupLast":10000,
            "healthboost":10300,
            "tittlescreen":500,
            "mouseCD":100
        }

        #Set event timers
        for dic in usereventDic:
            pygame.time.set_timer(usereventDic[dic], eventTimerDic[dic])

        pygame.mixer.music.play(-1)

    except Exception as e:
        input(e)
        Main.Quit()


    #Character
    x = int(wWidth/2)
    y = int(wHeight/2)
    Width = 32
    Height = 32
    Vel = 5
    playerSpriteNum = 0
    playerHealth = 5
    playerPlus = 0
    extraSpeed = 0
    myName = "NoName"
    nameEditor = False

    #ammo
    ammoHeight = 11
    ammoWidth = 7
    ammoBool = True
    bullets = []

    #Defeat
    defeatBool = False
    defeatBool2 = True

    #leaderboard
    top = { 0:{"name":"nnn", "score":"000"},
            1:{"name":"nnn", "score":"000"},
            2:{"name":"nnn", "score":"000"},
            3:{"name":"nnn", "score":"000"},
            4:{"name":"nnn", "score":"000"}}

    #enemy
    enemyWidth = 32
    enemyHeight = 32
    enemies = []
    enemySpeed = 1
    enemyHealth = 3
    enemySpawnHeight = wHeight
    NO = False
    TAKETHIS = False

    #Kills
    killpoints = 0

    #Next wave
    nextwave = 5

    #Score
    scorePoints = 0

    #Powerup
    powerupActive = -1
    powerups = []
    powerupMusic = True

    #healthboosts
    healthboost = []
    maxHp = 5

    #Menu
    escMenu = False
    quitPosX = int(wWidth/2 - 34)
    quitPosY = int(wHeight/2 + 80)
    hoverquit = 0

    creditsPosX = int(wWidth/2 - 60)
    creditsPosY = int(wHeight/2 + 40)
    hoverCredits = 0
    creditsScreen = False

    ResumePosX = int(wWidth/2 - 51)
    ResumePosY = int(wHeight/2 - 40)
    hoverResume = 0

    msCD = False

    #settings
    pauseMenu = False
    Slider1PosX = 425
    Slider1PosY = 450
    Slider1ButtonX = 475
    Slider1ButtonY = Slider1PosY + 2
    Slider2ButtonX = 475
    Slider2ButtonY = Slider1PosY + 52
    msliderBool = False
    ExitX = 650
    ExitY = 120
    hoverExit = 0
    hoverSettings = 0
    SettingsPosX = int(wWidth/2 - 68)
    SettingsPosY = int(wHeight/2 )

    #Tittlescreen
    tittlesceen = True
    tittlescreenNum = 0
    rains = []

    #Settings
    try:
        with open('assets/settings.json') as json_file:
            data = json.load(json_file)
            musicVolume = data["Volume"]["Music"]
            effectVolume = data["Volume"]["FX"]
            Slider1ButtonX = int(128 * data["Volume"]["Music"] + Slider1PosX - 21)
            Slider2ButtonX = int(128 * data["Volume"]["FX"] + Slider1PosX - 21)
            myName = data["Player"]["Name"]
            myName = Main.Name(myName)
        
    except Exception as e:
        print(e)
        musicVolume = 0.1
        effectVolume = 0.1
        myName = "nameh"


    #Game volume
    def Volume():
        global powerupMusic, timestamp
        pygame.mixer.music.set_volume(musicVolume)
        for mus in musicDic["Sounds"]:
            musicDic["Sounds"][mus].set_volume(effectVolume)

        if powerupMusic == True:
            if powerupActive == 3 or powerupActive == 4:
                powerupMusic = False

    Volume()
    
    #Set flying hearts
    def healthboostset():
        var = random.randint(0,1)
        pos = 0
        
        rng = random.randint(100,700)

        if var == 1:
            pos = wWidth - 22
        else:
            pos = 0 + 1

        healthboost.append([imgDic["addHealth"], pos, rng, 21, var])

    #Flying hearts
    def healthboosts():
        global healthboost

        for b in range(len(healthboost)):
            if healthboost[b][4] == 1:
                healthboost[b][1] -= 1
            else:
                healthboost[b][1] += 1

        for hpb in healthboost[:]:
            if hpb[1] > wWidth or hpb[1] < 0:
                healthboost.remove(hpb)

        for hpb in healthboost:
            win.blit(hpb[0][playerSpriteNum], pygame.Rect(hpb[1], hpb[2], hpb[3], hpb[3]))

    #Set powerup
    def powerupset():
        global powerups
        var = random.randint(0, 4)
        powerups.append([imgDic["powerup"][var], rnd(), 0, 32, var])
        
    #Reset powerup
    def powerupReset():
        global powerupActive, playerPlus, extraSpeed, powerupMusic
        powerupActive = -1
        playerPlus = 0
        extraSpeed = 0
        powerupMusic = True
        
    #Powerup
    def powerup():
        global powerups
        for b in range(len(powerups)):
            powerups[b][2] += 1

        for pwr in powerups[:]:
            if pwr[2] > wHeight:
                powerups.remove(pwr)

        for pwr in powerups:
            win.blit(pwr[0], pygame.Rect(pwr[1], pwr[2], pwr[3], pwr[3]))

    #Restart
    def reset():
        global x, y, playerHealth, enemySpeed, WaitFor, scorePoints, defeatBool2, nextwave
        #player
        x = int(wWidth/2)
        y= int(wHeight/2)
        
        playerHealth = maxHp

        defeatBool2 = True

        powerupReset()

        #enemy
        eventTimerDic["enemy"] = 2000
        pygame.time.set_timer(usereventDic["enemy"], eventTimerDic["enemy"])
        enemySpeed = 1
        nextwave = 5

        #score
        scorePoints = 0

    #Random enemy
    def rndEnemy():
        var = 1
        if scorePoints > 500 and scorePoints < 1000:
            var = random.randint(0,1)
        elif scorePoints > 1000:
            var = random.randint(0,2)
        return var

    #Set enemy
    def enemySet():
        global enemyHeight, enemyWidth, TAKETHIS

        if TAKETHIS:
            TAKETHIS = False
            powerupset()
            for i in range(5):
                Main.addEnemy(275 + i * 50, enemySpawnHeight, rndEnemy())
            for i in range(4):
                Main.addEnemy(300 + i * 50, enemySpawnHeight + 32, rndEnemy())
            for i in range(3):
                Main.addEnemy(325 + i * 50, enemySpawnHeight + 32 * 2, rndEnemy())
        else:
            Main.addEnemy(rnd(), enemySpawnHeight, rndEnemy())

    #Ammo
    def Ammo():
        for b in range(len(bullets)):
            bullets[b][1] += 10

        for bullet in bullets[:]:
            if bullet[1] > wHeight:
                bullets.remove(bullet)

        for bullet in bullets:
            win.blit(bullet[5], pygame.Rect(bullet[0], bullet[1], bullet[3], bullet[4]))

    #Random
    def rnd():
        return random.randint(wBorder, wWidth - wBorder - enemyWidth)

    #Speed enemy
    def speedUp():
        global enemySpeed, eventTimerDic

        if eventTimerDic["enemy"] > 1000:
            eventTimerDic["enemy"] -= 10
        if enemySpeed < 10 and eventTimerDic["enemy"] == 1000:
            enemySpeed += 0
        pygame.time.set_timer(usereventDic["enemy"], eventTimerDic["enemy"])
        
    #Enemy
    def Enemy():
        global enemies, playerHealth, enemySpeed, scorePoints, killpoints, nextwave

        for b in range(len(enemies)):
            enemies[b][1] -= enemySpeed

        for ene in enemies[:]:
            if ene[1] < 0:
                speedUp()
                enemies.remove(ene)
                playerHealth -= 1

            if ene[2] < 1:
                speedUp()
                scorePoints += ene[6]
                killpoints += 1
                nextwave -= 1
                enemies.remove(ene)
                

        #ene 0 = x, 1 = y, 2 = health, 3 = Height, 4 = Width, 5 = img  
        for ene in enemies:
            win.blit(ene[5][playerSpriteNum], pygame.Rect(ene[0], ene[1], ene[4], ene[3]))

    #Collision
    def collision():
        global enemies, bullets, powerups, playerHealth, powerupActive, ammoDmg, playerPlus, extraSpeed
        playerRect = pygame.Rect(x, y, Width, Height)

        for hpb in healthboost[:]:
            hpbRect = pygame.Rect(hpb[1],hpb[2],hpb[3],hpb[3])
            if pygame.Rect.colliderect(hpbRect, playerRect) and playerHealth < maxHp:
                musicDic["Sounds"]["Healthboost"].play()
                healthboost.remove(hpb)
                playerHealth += 1

        for pwr in powerups[:]:
            powerupRect = pygame.Rect(pwr[1],pwr[2],pwr[3],pwr[3])
            if pygame.Rect.colliderect(powerupRect, playerRect):
                musicDic["Sounds"]["Powerup"].stop()
                musicDic["Sounds"]["Powerup"].play()
                powerups.remove(pwr)
                powerupActive = pwr[4]
                pygame.time.set_timer(usereventDic["powerupLast"], eventTimerDic["powerupLast"])
                if powerupActive == 0:
                    playerPlus = 2
                if powerupActive == 3:
                    playerPlus = 4
                    extraSpeed = 2
                if powerupActive == 4:
                    playerPlus = 6
                    extraSpeed = 2
                

        for ene in enemies[:]:
            enemyRect = pygame.Rect(ene[0],ene[1],ene[4],ene[3])

            for bullet in bullets[:]:
                ammoRect = pygame.Rect(bullet[0],bullet[1],bullet[3],bullet[4])
                if pygame.Rect.colliderect(ammoRect, enemyRect):
                    musicDic["Sounds"]["Hit"].stop()
                    musicDic["Sounds"]["Hit"].play()
                    bullets.remove(bullet)
                    ene[2] -= bullet[2]

            if pygame.Rect.colliderect(playerRect, enemyRect):
                enemies.remove(ene)
                playerHealth -= 1
                musicDic["Sounds"]["Enemy"].stop()
                musicDic["Sounds"]["Enemy"].play()

    #Tittlescreen rain
    def tittless():
        global rains
        for b in range(len(rains)):
            rains[b][1] += 10

        for rain in rains[:]:
            if rain[1] > wHeight:
                rains.remove(rain)

        for rain in rains:
            win.blit(imgDic["ammo"][0], pygame.Rect(rain[0], rain[1], ammoWidth, ammoHeight))

    #Attack / Ammo
    def ammoAttack():
        if powerupActive == 0:
            bullets.append([int(x + (Width/2) - 7), int(y + Height - ammoHeight/1.5), 10, 7*2, 11*2, bigwater]) 
        elif powerupActive == 1:
            bullets.append([int(x + (Width/2) + ammoWidth), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1, 7,11,imgDic["ammo"][0]]) 
            bullets.append([int(x + (Width/2) - ammoWidth * 2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1,7,11,imgDic["ammo"][0]]) 

        elif powerupActive == 2:
            bullets.append([int(x + (Width/2) + ammoWidth), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1,7,11,imgDic["ammo"][0]]) 
            bullets.append([int(x + (Width/2) - ammoWidth/2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1,7,11,imgDic["ammo"][0]]) 
            bullets.append([int(x + (Width/2) - ammoWidth * 2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1,7,11,imgDic["ammo"][0]]) 
        
        elif powerupActive == 3:
            bullets.append([int(x + (Width/2) - ammoWidth/2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 2,7,11,imgDic["ammo"][1]]) 
        
        elif powerupActive == 4:
            bullets.append([int(x + (Width/2) + ammoWidth), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 2,7,11,imgDic["ammo"][1]]) 
            bullets.append([int(x + (Width/2) - ammoWidth * 2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 2,7,11,imgDic["ammo"][1]])
        
        else:
            bullets.append([int(x + (Width/2) - ammoWidth/2), int(y + Height - (ammoHeight * 2 - ammoHeight/2)), 1,7,11,imgDic["ammo"][0]]) 
        

    #Death
    def death():
        healthboost.clear()
        bullets.clear()
        enemies.clear()
        powerups.clear()
        musicDic["Sounds"]["Defeat"].play()

    #Movement
    def Movement():
        global x, y, ammoBool, ammoWidth, ammoHeight, Height, Width, defeatBool, defeatBool2
        keys = pygame.key.get_pressed()
        #Controls
        if playerHealth > 0:
            defeatBool = False
            if keys[pygame.K_LEFT] and x > wBorder or keys[pygame.K_a] and x > wBorder:
                x -= (Vel + extraSpeed)

            if keys[pygame.K_RIGHT] and x < (wWidth - Width - wBorder) or keys[pygame.K_d] and x < (wWidth - Width - wBorder):
                x += (Vel + extraSpeed)

            if keys[pygame.K_UP] and y > wBorder or keys[pygame.K_w] and y > wBorder:
                y -= (Vel + extraSpeed)

            if keys[pygame.K_DOWN] and y < (wHeight - Height - wBorder) or keys[pygame.K_s] and y < (wHeight - Height - wBorder):
                y += (Vel + extraSpeed)

            #Attack / ammo
            if keys[pygame.K_SPACE] and ammoBool == True:
                ammoBool = False
                ammoAttack()
        #Play again
        else:
            if defeatBool2 == True:
                defeatBool = True
                defeatBool2 = False
                death()
                Draw.Loading()

    #Draw
    class Draw:
        def Main():
            win.blit(imgDic["background"], (0,0))
            if tittlesceen == True:
                tittless()
                win.blit(imgDic["tittlescreen"], (int(wWidth/2 - 56 * 10 / 2), int(wHeight/2 - 19 * 10 / 2)))
                win.blit(imgDic["pressanything"][tittlescreenNum], (int(wWidth/2 - (123 * 3) / 2), int(wHeight/2 + 5 * 3 * 10 )))
                
            elif pauseMenu == True:
                Draw.pauseMenuF()
            elif nameEditor == True:
                Draw.nameEditorF()
            elif creditsScreen == True:
                Draw.creditsF()
            elif escMenu == True:
                Draw.escMenuF()
            else:
                Draw.HP()
                Draw.Score()
                if defeatBool == False:
                    Draw.NameF()
                    Ammo()
                    Enemy()
                    powerup()
                    healthboosts()
                    win.blit(imgDic["player"][playerSpriteNum + playerPlus], (x, y, Width, Height))
                    
                else:
                    tittless()
                    win.blit(imgDic["defeat"], (int(wWidth/2 - 65 * 10 / 2), int(wHeight/2 - 160)))
                    win.blit(imgDic["continue"],(int(wWidth/2 - 90), int(wHeight/2 + 25)))
                    win.blit(imgDic["leaderboard"],(int(wWidth/2 - 150), int(wHeight/2 + 150)))
                    Draw.top5()

            
            Draw.Cursor()
            pygame.display.update()

        def HP():
            #Healthbar
            for hp in range(maxHp):
                if playerHealth > hp:
                    win.blit(imgDic["fheart"], (10 + hp * 8 * 3, (wHeight - 10) - 8 * 3)) 
                else:
                    win.blit(imgDic["bheart"], (10 + hp * 8 * 3, (wHeight - 10) - 8 * 3)) 
        def Score():
            #Scorebar
            scoreSplit = [int(d) for d in str(scorePoints)]
            win.blit(imgDic["scoreDic"]["score"], (10, wHeight - 8 * 6 - 10))
            spaceBetween = 0
            for scr in scoreSplit:
                win.blit(imgDic["scoreDic"][scr], ( (27 * 3 + 20) + spaceBetween, wHeight - 8 * 6 - 10))
                if scr == 1:
                    spaceBetween += 12
                else:
                    spaceBetween += 15

        def Loading():
            win.blit(imgDic["background"], (0,0))
            win.blit(imgDic["defeat"], (int(wWidth/2 - 65 * 10 / 2), int(wHeight/2 - 160)))
            win.blit(imgDic["continue"],(int(wWidth/2 - 90), int(wHeight/2 + 25)))
            win.blit(imgDic["leaderboard"],(int(wWidth/2 - 150), int(wHeight/2 + 150)))
            win.blit(imgDic["loading"],(800 - (132 + 5),800 - (15 + 5)))
            Draw.HP()
            Draw.Score()

            pygame.display.update()

            re.sub(r'[^\w]', ' ', myName)
            threading.Thread(target=Main.thread1).start()
            threading.Thread(target=Main.thread2).start()
            
        def top5():
            for i in top:
                top5count = 0
                topHeight = int(wHeight/2 + (200 + i * 15 + 3 * i))
                topWidth = int(wWidth/2)
                for srt in top[i]["name"]:
                    
                    try:
                        win.blit(imgDic["abc"][srt],(topWidth - (110 - top5count), topHeight))
                    except:
                        inte = int(srt)
                        win.blit(imgDic["scoreDic"][inte],(topWidth - (110 - top5count), topHeight))
                    top5count += 17
                top5count = 0
                win.blit(imgDic["scoreDic"]["score"],(topWidth - (0 - top5count), topHeight))
                for scr in top[i]["score"]:
                    inte = int(scr)
                    win.blit(imgDic["scoreDic"][inte],(topWidth + (100 + top5count), topHeight))
                    top5count += 17

        def NameF():
            win.blit(imgDic["nameBG"], (-35 - ((5 - len(myName)) * 17), -10))
            nameCount = 0
            for i in myName:
                try:
                    win.blit(imgDic["abc"][i],((5 + nameCount), 5))
                except:
                    inte = int(i)
                    win.blit(imgDic["scoreDic"][inte],((5 + nameCount), 5))
                nameCount += 17
        
        def nameEditorF():
            tittless()
            win.blit(imgDic["pause"]["BG"], (50, 50))
            win.blit(imgDic["pause"]["x"][hoverExit], (ExitX, ExitY))
            win.blit(RainyLogoSettings, (int(wWidth/2 - 56), 120))
            Draw.dText(myName, 357, 240, playerSpriteNum)
            Draw.dText("space", 250, 340, 0)
            Draw.dText("backspace", 420, 340, 0)
            x = 250
            y = 400
            for i in imgDic["abc"]:
                Draw.dText(i, x, y, 0)
                x += 30
                if x > 550:
                    x = 250
                    y += 30
            x = 250
            y = 370
            for i in imgDic["scoreDic"]:
                if i != "score":
                    Draw.dText(str(i), x, y, 0)
                    x += 30
                    if x > 550:
                        x = 250
                        y += 30 
                        

        def pauseMenuF():
            #X = 120 - 700, Y = 120 - 700
            tittless()
            win.blit(imgDic["pause"]["BG"], (50, 50))
            win.blit(RainyLogoSettings, (int(wWidth/2 - 56), 120))
            win.blit(imgDic["pause"]["x"][hoverExit], (ExitX, ExitY))
            Draw.dText(" ", int(wWidth/2 + 39), 130, 1)

            #Controls
            offsetY = 30
            Draw.dText("controls", 332, 200 + offsetY, 0)
            win.blit(imgDic["pause"]["Border"][playerSpriteNum], (300, 250 + offsetY))
            Draw.dText("W", 304, 254 + offsetY, 0)
            win.blit(imgDic["pause"]["Border"][playerSpriteNum], (270, 280 + offsetY))
            Draw.dText("A", 276, 284 + offsetY, 0)
            win.blit(imgDic["pause"]["Border"][playerSpriteNum], (300, 280 + offsetY))
            Draw.dText("S", 306, 284 + offsetY, 0)
            win.blit(imgDic["pause"]["Border"][playerSpriteNum], (330, 280 + offsetY))
            Draw.dText("D", 336, 284 + offsetY, 0)
            win.blit(imgDic["pause"]["plus"], (395, 270 + offsetY))
            win.blit(imgDic["pause"]["BorderS"][playerSpriteNum], (440, 280 + offsetY))
            Draw.dText("space", 444, 284 + offsetY, 0)

            #Volume settings
            Draw.dText("volume settings" , Slider1PosX - 150, Slider1PosY - 45 , 0)
            Draw.dText("music", Slider1PosX - 150, Slider1PosY + 5, 0)
            win.blit(imgDic["pause"]["Slider"], (Slider1PosX, Slider1PosY))
            win.blit(imgDic["pause"]["SlideButton"], (Slider1ButtonX, Slider1ButtonY))
            Draw.dText("fx", Slider1PosX - 150, Slider1PosY + 55, 0)
            win.blit(imgDic["pause"]["Slider"], (Slider1PosX, Slider1PosY + 50))
            win.blit(imgDic["pause"]["SlideButton"], (Slider2ButtonX, Slider2ButtonY))
        
        def escMenuF():
            tittless()
            win.blit(imgDic["pause"]["BG2"], (int(wWidth/2 - 120), 290))
            win.blit(RainyLogoSettings, (int(wWidth/2 - 56), 310))
            Draw.dText("resume", ResumePosX, ResumePosY, hoverResume)
            Draw.dText("settings", SettingsPosX, SettingsPosY, hoverSettings)
            Draw.dText("credits", creditsPosX, creditsPosY, hoverCredits)
            Draw.dText("quit", quitPosX, quitPosY, hoverquit)

        def creditsF():
            tittless()
            win.blit(imgDic["pause"]["BG"], (50, 50))
            win.blit(imgDic["pause"]["x"][hoverExit], (ExitX, ExitY))
            win.blit(RainyLogoSettings, (int(wWidth/2 - 56), 120))
            Draw.dText(" ", int(wWidth/2 + 39), 130, 1)
            offsetY = 30
            Draw.dText("code mikko j", int(wWidth/2 - 120), 200 + offsetY, 0)
            Draw.dText("music vilho m", int(wWidth/2 - 120), 240 + offsetY, 0)
            Draw.dText("art elias k", int(wWidth/2 - 120), 280 + offsetY, 0)
            Draw.dText("desing1 mikko j", int(wWidth/2 - 120), 330 + offsetY, 0)
            Draw.dText("desing2 elias k", int(wWidth/2 - 120), 370 + offsetY, 0)
            Draw.dText("fx1 vilho m", int(wWidth/2 - 120), 420 + offsetY, 0)
            Draw.dText("fx2 mikko j", int(wWidth/2 - 120), 460 + offsetY, 0)

        #draw text
        def dText(txt, wdth, hght, mode):
            txt = txt.lower()
            widthBetween = 0
            for i in txt:
                try:
                    win.blit(imgDic["abc"][i],(wdth + widthBetween, hght))
                except: 
                    inte = int(i)
                    win.blit(imgDic["scoreDic"][inte],(wdth + widthBetween, hght))
                widthBetween += 17
            if mode == 1:
                win.blit(imgDic["pause"]["SlideButton"],(wdth + widthBetween, hght))

        def Cursor():
            pos = pygame.mouse.get_pos()
            win.blit(imgDic["Cursor"], (pos[0]-4, pos[1]-4))

    #Main loop
    run = True
    while run:

        #Mouse position
        ms = pygame.mouse.get_pos()

        #Mouse button
        button = pygame.mouse.get_pressed()

        clock.tick(60)
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                    run = False
            
            #Spawn rains
            if event.type == usereventDic["tittlescreen"]:
                    if tittlesceen == True or pauseMenu == True or defeatBool == True or nameEditor == True or escMenu == True or creditsScreen == True:
                        for i in range(30):
                            rains.append([random.randint(0, wWidth - 7), 0 - i * 10])
                    tittlescreenNum = 0 if tittlescreenNum == 1 else 1

            #Animation event
            if event.type == usereventDic["animation"]:
                playerSpriteNum = 0 if playerSpriteNum == 1 else 1

            #Mouse cd
            if event.type == usereventDic["mouseCD"]:
                msCD = False

            #Defeat screen
            if defeatBool == True:
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                    defeatBool = False
                    onceDefeat = False
                    reset()
                    rains.clear()

                if ms[0] > int(wWidth/2 - 90) and ms[0] < int(wWidth/2 + 90) and ms[1] > int(wHeight/2 + 25) and ms[1] < int(wHeight/2 + 69):
                    if hoverExit == 0:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()

                    hoverExit = 1

                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].stop()
                        musicDic["Sounds"]["Click"].play()
                        defeatBool = False
                        onceDefeat = False
                        reset()
                        rains.clear()
                else: 
                    hoverExit = 0

            #Tittlescreen
            elif tittlesceen == True:
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    tittlesceen = False
                    rains.clear()
            
            #Pause menu
            elif pauseMenu == True:
                #Music Slider
                if ms[0] > Slider1PosX and ms[0] < Slider1PosX + 64 * 2 and ms[1] > Slider1PosY and ms[1] < Slider1PosY + 16 * 2 and button[0] != 0:
                    Slider1ButtonX = ms[0] - 21
                    musicVolume = (ms[0] - Slider1PosX) / 128

                #FX Slider
                if ms[0] > Slider1PosX and ms[0] < Slider1PosX + 64 * 2 and ms[1] > Slider1PosY + 50 and ms[1] < Slider1PosY + 50 + 16 * 2 and button[0] != 0:
                    Slider2ButtonX = ms[0] - 21
                    effectVolume = (ms[0] - Slider1PosX) / 128
                
                #Exit
                if ms[0] > ExitX and ms[0] < ExitX + 16 * 2 and ms[1] > ExitY and ms[1] < ExitY + 16 * 2:
                    if hoverExit == 0:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    
                    hoverExit = 1

                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].stop()
                        musicDic["Sounds"]["Click"].play()
                        Main.json()
                        pauseMenu = False
                        escMenu = True
                else: 
                    hoverExit = 0

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                    Main.json()
                    pauseMenu = False
                    escMenu = True

                #Volume set
                Volume()
            
            #Name editor
            elif nameEditor == True:
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    nameEditor = False
                    Main.json()
                    rains.clear()
                    myName = Main.Name(myName)
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()

                #Exit
                if ms[0] > ExitX and ms[0] < ExitX + 16 * 2 and ms[1] > ExitY and ms[1] < ExitY + 16 * 2:
                    if hoverExit == 0:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverExit = 1
                    if button[0] != 0:
                        nameEditor = False
                        Main.json()
                        rains.clear()
                        myName = Main.Name(myName)
                        musicDic["Sounds"]["Click"].stop()
                        musicDic["Sounds"]["Click"].play()
                else: 
                    hoverExit = 0

                if ms[0] > 250 and ms[0] < 250 + 85 and ms[1] > 340 and ms[1] < 340 + 15 and button[0] != 0 and len(myName) < 5 and msCD == False:
                    myName = myName + " "
                    msCD = True
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()

                if ms[0] > 420 and ms[0] < 420 + 153 and ms[1] > 340 and ms[1] < 340 + 15 and button[0] != 0 and msCD == False:
                    myName = myName[:-1]
                    msCD = True
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()

                fX = 250
                fY = 400
                for letter in imgDic["abc"]:
                    if letter != " ":
                        if ms[0] > fX and ms[0] < fX + 15 and ms[1] > fY and ms[1] < fY + 15 and button[0] != 0 and len(myName) < 5 and msCD == False:
                            myName = myName + letter
                            msCD = True
                            musicDic["Sounds"]["Click"].stop()
                            musicDic["Sounds"]["Click"].play()
                        fX += 30
                        if fX > 550:
                            fX = 250
                            fY += 30

                fX = 250
                fY = 370
                for number in imgDic["scoreDic"]:
                    number = str(number)
                    if number != "score":
                        if ms[0] > fX and ms[0] < fX + 15 and ms[1] > fY and ms[1] < fY + 15 and button[0] != 0 and len(myName) < 5 and msCD == False:
                            myName = myName + number
                            msCD = True
                            musicDic["Sounds"]["Click"].stop()
                            musicDic["Sounds"]["Click"].play()
                        fX += 30
                        if fX > 550:
                            fX = 250
                            fY += 30

            #Credits
            elif creditsScreen == True:
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    creditsScreen = False
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                #Exit
                if ms[0] > ExitX and ms[0] < ExitX + 16 * 2 and ms[1] > ExitY and ms[1] < ExitY + 16 * 2:
                    if hoverExit == 0:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverExit = 1
                    if button[0] != 0:
                        creditsScreen = False
                        musicDic["Sounds"]["Click"].stop()
                        musicDic["Sounds"]["Click"].play()
                else: 
                    hoverExit = 0

            #Menu
            elif escMenu == True:
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    escMenu = False
                    rains.clear()
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                
                if ms[0] > ResumePosX and ms[0] < ResumePosX + 102 and ms[1] > ResumePosY and ms[1] < ResumePosY + 16 * 2:
                    if hoverResume != 1:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverResume = 1
                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].play()
                        escMenu = False
                        rains.clear()
                else:
                    hoverResume = 0
                    
                #Hover settings    
                if ms[0] > SettingsPosX and ms[0] < SettingsPosX + 136 and ms[1] > SettingsPosY and ms[1] < SettingsPosY + 16 * 2:
                    if hoverSettings != 1:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverSettings = 1
                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].play()
                        pauseMenu = True
                else:
                    hoverSettings = 0

                #Hover quit
                if ms[0] > quitPosX and ms[0] < quitPosX + 68 and ms[1] > quitPosY and ms[1] < quitPosY + 16 * 2:
                    if hoverquit != 1:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverquit = 1
                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].play()
                        run = False
                else:
                    hoverquit = 0

                #Hover credits
                if ms[0] > creditsPosX and ms[0] < creditsPosX + 117 and ms[1] > creditsPosY and ms[1] < creditsPosY + 16 * 2:
                    if hoverCredits != 1:
                        musicDic["Sounds"]["Hover"].stop()
                        musicDic["Sounds"]["Hover"].play()
                    hoverCredits = 1
                    if button[0] != 0:
                        musicDic["Sounds"]["Click"].play()
                        creditsScreen = True
                else:
                    hoverCredits = 0

            else:
                #Click name
                if ms[0] > 0 and ms[0] < 10 + 17 * len(myName) and ms[1] > 0 and ms[1] < 30 and button[0] != 0:
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                    nameEditor = True

                #Press esc to pause
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    musicDic["Sounds"]["Click"].stop()
                    musicDic["Sounds"]["Click"].play()
                    escMenu = True

                #Enemy event
                if event.type == usereventDic["enemy"]:
                    enemySet() 

                #Ammo cooldown
                if event.type == usereventDic["ammo"]:
                    ammoBool = True

                #Powerup wear off
                if event.type == usereventDic["powerupLast"]:
                    powerupReset()

                #Spawn extra hp
                if event.type == usereventDic["healthboost"]:
                    healthboostset()

        #Game movement if isn't paused
        if pauseMenu != True and tittlesceen != True and defeatBool != True and nameEditor != True and escMenu != True and creditsScreen != True:
            Movement()
            collision()

        #Wave manager
        if TAKETHIS == False:
            if nextwave <= 0:
                TAKETHIS = True
                nextwave = 20
        
        #Draw
        Draw.Main()

    #Quit
    Main.Quit()