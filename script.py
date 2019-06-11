import sys, pygame, math, json, os, threading, time, random

pygame.init()
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption('Clicky')
icon = pygame.image.load(os.path.join(sys.path[0], "images\icon.png"))
pygame.display.set_icon(icon)

# Initialize variables and load files #
font = pygame.font.Font(None, 25)

logo = pygame.image.load(os.path.join(sys.path[0], "images\logo.png"))
pygame.mixer.music.load(os.path.join(sys.path[0], "sounds\\achievement.ogg"))

# Minigame Assets #
asteroidsBG = pygame.image.load(os.path.join(sys.path[0], "images\\asteroidsBG.jpg"))
asteroidsBulletRaw = pygame.image.load(os.path.join(sys.path[0], "images\\asteroidsBullet.png"))
asteroidsBullet = pygame.transform.scale(asteroidsBulletRaw, (20, 20))
asteroidsSpaceshipRaw = pygame.image.load(os.path.join(sys.path[0], "images\\asteroidsSpaceship.png"))
asteroidsSpaceship = pygame.transform.scale(asteroidsSpaceshipRaw, (70, 70))
asteroidsAsteroidRaw = pygame.image.load(os.path.join(sys.path[0], "images\\asteroidsAsteroid.png"))
asteroidsAsteroid = pygame.transform.scale(asteroidsAsteroidRaw, (70, 70))
asteroidsAlienRaw = pygame.image.load(os.path.join(sys.path[0], "images\\asteroidsAlien.png"))
asteroidsAlien = pygame.transform.scale(asteroidsAlienRaw, (70, 70))

white = [255, 255, 255]
black = [0, 0, 0]
green = [65, 221, 37]
red = [244, 95, 66]

counter = 0
clickCount = 0
mult = 1
multCost = 100
perSecond = 0
perSecondCost = 1000
saves = {}
gameRunning = True
errorLoading = False
achievements = [False, False, False, False, False, False]

"""
tips = [
"TIP: Pressing Enter has the same functionality as clicking the 'Get Score' box!",
"TIP: If you have Per Second Bonus, leave the game open and you will gain score without clicking!",
"TIP: Check on your achievement progess once in a while! You can claim rewards for completing them.",
"TIP: Tell the dev to add this if you can see this. Tell him: 'Add the tip code 1'!"
]
"""

# Which screen is the player in and which checks should be run relative to that screen? #
whatScreen = "main"

# Menu variables #
firstTimeOpening = False
inAboutScreen = False
isInErrorScreen = False
splashScreen = True
inAchievementsScreen = False
achievementGet = False
inMinigamesScreen = False

# Minigames Variables #
minigamesUnlocked = [False, False, False]

scoreBox = (325, 75, 300, 100)
getMultBox = (325, 200, 300, 100)
getPerSecondBox = (325, 325, 300, 100)
okBox = (325, 200, 50, 50)
aboutBox = (40, 445, 80, 50)
achievementsBox = (40, 200, 135, 50)

# Minigame Boxes #
minigamesBox = (40, 125, 135, 50)
minigameSelectBox1 = (10, 200, 240, 60)
minigameSelectBox2 = (10, 270, 240, 60)
minigameSelectBox3 = (10, 340, 240, 60)

# Achievement Stuff #
achGetBox = [300, 500, 200, 50]
achGetText = [320, 520]
waitCounter = 0

# -----MINIGAME OBJECTS------ #
# Asteroids
asteroidsSpaceshipPos = [400, 400]
canShoot = True
missiles = {}
asteroids = {}
asteroidsScore = 0
asteroidsHighScore = 0
destroyed = False
asteroidsToPop = []
missilesToPop = []
asteroidsFrameUpdate = False

# Things? #
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

# FUNCTIONS #

def secondLoop():
    global counter
    while gameRunning:
        counter += perSecond
        time.sleep(1)

def asteroidsCollisionChecks():
    global asteroids
    global missiles
    global asteroidsFrameUpdate

    while gameRunning:
        if asteroidsFrameUpdate:
            value = 1 + 1
            asteroidsFrameUpdate = False
        else:
            value = 1+1
        time.sleep(0.25)

def load():
    with open(os.path.join(sys.path[0], "save.json"), "r") as file:
        global counter
        global mult
        global multCost
        global saves
        global perSecond
        global firstTimeOpening
        global perSecondCost
        global achievements
        global clickCount
        global minigamesUnlocked
        global asteroidsHighScore
        saves = json.load(file)
        counter = int(saves["score"])
        mult = int(saves["multi"])
        multCost = int(saves["multCost"])
        perSecond = int(saves["perSecond"])
        firstTimeOpening = saves["firstTimeOpening"]
        perSecondCost = int(saves["perSecondCost"])
        achievements = saves["achievements"]
        clickCount = int(saves["clickCount"])
        minigamesUnlocked = saves["minigamesUnlocked"]
        asteroidsHighScore = int(saves["asteroidsHighScore"])

# Load scores #
try:
    load()
except Exception as e:
    errorLoading = True
    isInErrorScreen = True
    print("An error occured while loading scores. Is the file corrupted or has it been moved? Error screen opened in application.")
    print("Error: {}".format(str(e)))

def save():
    saves["score"] = counter
    saves["multi"] = mult
    saves["multCost"] = multCost
    saves["perSecond"] = perSecond
    saves["firstTimeOpening"] = firstTimeOpening
    saves["perSecond"] = perSecond
    saves["perSecondCost"] = perSecondCost
    saves["achievements"] = achievements
    saves["clickCount"] = clickCount
    saves["minigamesUnlocked"] = minigamesUnlocked
    saves["asteroidsHighScore"] = asteroidsHighScore

    with open(os.path.join(sys.path[0], "save.json"), "w") as file:
        json.dump(saves, file)

def check_click(position, target):
    if ((position[0] > target[0] and position[0] < target[0] + target[2]) and (position[1] > target[1] and position[1] < target[1] + target[3])):
        print("Good!")
    return ((position[0] > target[0] and position[0] < target[0] + target[2]) and (position[1] > target[1] and position[1] < target[1] + target[3]))

def check_screen():
    global firstTimeOpening
    global isInErrorScreen
    global inAchievementsScreen
    global inAboutScreen
    if not firstTimeOpening and not isInErrorScreen and not inAboutScreen and not inAchievementsScreen:
        return True

def exitScreen():
    screen.fill(white)
    screen.blit(font.render("Saving...", True, black), (380, 180))
    pygame.display.flip()
    time.sleep(2)

# Start the loops #
secondLoopThread = threading.Thread(target=secondLoop)
secondLoopThread.start()

asteroidsCollisionChecksLoop = threading.Thread(target=asteroidsCollisionChecks)
asteroidsCollisionChecksLoop.start()

# MAIN GAME LOOP #
while True:

    # Main Screen #
    while whatScreen == "main":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                gameRunning = False
                exitScreen()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if clickCount == 1:
                    pygame.mixer.music.play()
                    achievementGet = True
                    achievements[0] = True

                clickCount += 1

                if check_click(event.pos, okBox):
                    if firstTimeOpening:
                        firstTimeOpening = False
                    elif isInErrorScreen:
                        isInErrorScreen = False
                    elif inAboutScreen:
                        inAboutScreen = False
                    elif inAchievementsScreen:
                        inAchievementsScreen = False

                elif check_click(event.pos, minigamesBox):
                    if whatScreen != "minigameSelect":
                        whatScreen = "minigameSelect"
                
                elif check_click(event.pos, aboutBox):
                    if not inAboutScreen:
                        inAboutScreen = True

                elif check_click(event.pos, achievementsBox):
                    if not inAchievementsScreen:
                        inAchievementsScreen = True

                elif check_click(event.pos, scoreBox):
                    if check_screen():
                        print(counter)
                        counter += 1 * mult
                        print(counter)

                elif check_click(event.pos, getMultBox):
                    if check_screen():
                        if counter >= multCost:
                            if mult == 1 and not achievements[1]:
                                pygame.mixer.music.play()
                                achievementGet = True
                                achievements[1] = True

                            counter -= multCost
                            mult += 1
                            multCost += 100

                elif check_click(event.pos, getPerSecondBox):
                    if check_screen():
                        if counter >= perSecondCost:
                            if perSecond == 0 and not achievements[2]:
                                pygame.mixer.music.play()
                                achievementGet = True
                                achievements[2] = True

                            counter -= perSecondCost
                            perSecond += 1
                            perSecondCost += 500

        if counter >= 10000 and not achievements[3]:
            pygame.mixer.music.play()
            achievementGet = True
            achievements[3] = True

        # Cockatoo Splash Screen #
        if splashScreen:
            screen.fill(white)
            logoScaled = pygame.transform.scale(logo, (300, 300))
            screen.blit(logoScaled, (250, 100))
            screen.blit(font.render("Clicky © 2019 Cockatoo Development Studios. See our website at https://cockatoo.dev!", True, black), (40, 400))
            pygame.display.flip()
            time.sleep(5)
            splashScreen = False


        # If it is the first time the user has opened the game or the database has been reset, show information #
        if firstTimeOpening:
            screen.fill(white)
            screen.fill(black, okBox)
            screen.blit(font.render("Ok", True, white), (335, 210))
            screen.blit(font.render("Welcome to Clicky!", True, black), (10, 10))
            screen.blit(font.render("This is a simple clicker game.", True, black), (10, 30))
            screen.blit(font.render("You just need to click on the black square to get Score.", True, black), (10, 50))
            screen.blit(font.render("You can get Multiplier which increases the amount of Score you get per tap.", True, black), (10, 70))
            screen.blit(font.render("You can get a Per Second Bonus which gives you score while the game is open!", True, black), (10, 90))
            screen.blit(font.render("I hope you enjoy Clicky!", True, black), (10, 110))
            screen.blit(font.render("Clicky © 2019 Cockatoo Development Studios. See our website at https://cockatoo.dev!", True, black), (10, 130))

            screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
            clock.tick(61)
            pygame.display.flip()


        # About Screen #
        elif inAboutScreen:
            screen.fill(white)
            screen.fill(black, okBox)
            screen.blit(font.render("Ok", True, white), (335, 210))
            screen.blit(font.render("Clicky Version 1.1!", True, black), (10, 10))
            screen.blit(font.render("Written entirely in Python 3.6.5 and Pygame 1.9.4", True, black), (10, 30))
            screen.blit(font.render("Update 0.8a Changelog:", True, black), (10, 50))
            screen.blit(font.render(" - Added achievements", True, black), (10, 70))
            screen.blit(font.render("   Added minigame selector and FPS display", True, black), (10, 90))
            screen.blit(font.render("Clicky is open source. See code at https://github.com/Lumiobyte/clicker", True, black), (10, 110))
            screen.blit(font.render("Clicky © 2019 Cockatoo Development Studios. See our website at https://cockatoo.dev!", True, black), (10, 130))

            screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
            clock.tick(61)
            pygame.display.flip()

        # Files Corrupted Screen #
        elif isInErrorScreen:
            screen.fill(white)
            screen.fill(black, okBox)
            screen.blit(font.render("Ok", True, white), (335, 210))
            screen.blit(font.render("Oh no, this is embarrassing...", True, black), (10, 10))
            screen.blit(font.render("Clicky encountered an error when loading your previous save.", True, black), (10, 30))
            screen.blit(font.render("Has the file been moved or corrupted?", True, black), (10, 50))
            screen.blit(font.render("If you moved the file and you know where it is, please get it", True, black), (10, 70))
            screen.blit(font.render("and place it in the SAME DIRECTORY as this executable.", True, black), (10, 90))
            screen.blit(font.render("If you're still having issues, please contact us at https://cockatoo.dev/contact", True, black), (10, 110))
            screen.blit(font.render("You can still start your game from scratch if your save file has been corrupted.", True, black), (10, 130))
            screen.blit(font.render("If you want to, click OK below.", True, black), (10, 150))

            screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
            clock.tick(61)
            pygame.display.flip()

        elif inAchievementsScreen:
            screen.fill(white)
            screen.fill(black, okBox)
            screen.blit(font.render("Ok", True, white), (335, 210))
            screen.blit(font.render("ACHIEVEMENTS", True, black), (10, 10))

            if achievements[0]:
                screen.blit(font.render("   - Click for the first time!", True, black), (10, 30))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 30))

            if achievements[1]:
                screen.blit(font.render("   - Get your first Multiplier!", True, black), (10, 50))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 50))
            if achievements[2]:
                screen.blit(font.render("   - Get your first Per Second Bonus!", True, black), (10, 70))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 70))
            if achievements[3]:
                screen.blit(font.render("   - Get 10000 Score for the first time!", True, black), (10, 90))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 90))
            if achievements[4]:
                screen.blit(font.render("   - something  here", True, black), (10, 110))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 110))
            if achievements[5]:
                screen.blit(font.render("   - something here", True, black), (10, 130))
            else:
                screen.blit(font.render("   - Locked", True, black), (10, 130))

            screen.blit(font.render("Get Achievements to get rewards!", True, black), (10, 150))

            screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
            clock.tick(61)
            pygame.display.flip()

        else:
            # Scale the logo image #
            logoScaled = pygame.transform.scale(logo, (130, 130))

            # Draw to screen #
            screen.fill(white)
            screen.fill(black, scoreBox)
            screen.fill(black, getMultBox)
            screen.fill(black, getPerSecondBox)
            screen.fill(black, aboutBox)
            screen.fill(black, achievementsBox)
            screen.fill(black, minigamesBox)
            screen.blit(logoScaled, (10, 320))

            # Render text #
            screen.blit(font.render("You have " + str(counter) + " score.", True, black), (10, 10))
            screen.blit(font.render("You have " + str(mult) + " multiplier.", True, black), (10, 25))
            screen.blit(font.render("You get " + str(perSecond) + " score per second.", True, black), (10, 40))
            screen.blit(font.render("Click here to get score!", True, white), (325, 75))
            screen.blit(font.render("Click here to get multiplier!".format(multCost), True, white), (325, 200))
            screen.blit(font.render("Cost: {} score".format(multCost), True, white), (325, 220))
            screen.blit(font.render("Click here to get Per Second Bonus!".format(multCost), True, white), (325, 325))
            screen.blit(font.render("Cost: {} score".format(perSecondCost), True, white), (325, 345))
            screen.blit(font.render("About".format(perSecondCost), True, white), (55, 460))
            screen.blit(font.render("Achievements".format(perSecondCost), True, white), (48, 215))
            screen.blit(font.render("Play Minigames".format(perSecondCost), True, white), (46, 140))

            if achievementGet:

                print(str(achGetBox[1]) + " " + str(achGetText[1]) + " " + str(waitCounter))
                if achGetBox[1] >= 440 and not waitCounter >= 450:
                    achGetBox[1] -= 1
                    achGetText[1] -= 1
                elif achGetBox[1] <= 500 and waitCounter >= 450:
                    achGetBox[1] += 1
                    achGetText[1] += 1
                else:
                    waitCounter += 1

                screen.fill(green, (achGetBox[0], achGetBox[1], achGetBox[2], achGetBox[3]))
                screen.blit(font.render("Achievement Get!".format(perSecondCost), True, black), (achGetText[0], achGetText[1]))

                if achGetBox[1] == 499 and waitCounter >= 450:
                    waitCounter = 0
                    achievementGet = False

            # Get FPS & Render it #
            screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))

            # Make stuff work? #
            clock.tick(61)
            pygame.display.flip()


    # Minigame Select Screen #
    while whatScreen == "minigameSelect":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                gameRunning = False
                exitScreen()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if clickCount == 1:
                    pygame.mixer.music.play()
                    achievementGet = True
                    achievements[0] = True

                clickCount += 1

                if check_click(event.pos, okBox):
                    whatScreen = "main"

                elif check_click(event.pos, minigameSelectBox1):
                    if minigamesUnlocked[0] and counter >= 550:
                        counter -= 550
                        whatScreen = "minigame1"
                    elif not minigamesUnlocked[0] and counter >= 2800:
                        counter -= 2800
                        minigamesUnlocked[0] = True
                
                elif check_click(event.pos, minigameSelectBox2):
                    if minigamesUnlocked[1] and counter >= 2250:
                        counter -= 2250
                        #whatScreen = "minigame2"
                    elif not minigamesUnlocked[1] and counter >= 16500:
                        counter -= 16500
                        minigamesUnlocked[1] = True

                elif check_click(event.pos, minigameSelectBox3):
                    if minigamesUnlocked[2] and counter >= 6750:
                        counter -= 6750
                        #whatScreen = "minigame3"
                    elif not minigamesUnlocked[2] and counter >= 25000:
                        counter -= 25000
                        minigamesUnlocked[2] = True

        screen.fill(white)
        screen.fill(black, okBox)
        screen.blit(font.render("Back", True, white), (331, 210))
        screen.blit(font.render("Which minigame would you like to play?", True, black), (10, 10))
        screen.blit(font.render("Each minigame costs score to play.", True, black), (10, 30))
        screen.blit(font.render("You will need to unlock it before you can play it.", True, black), (10, 50))
        screen.blit(font.render("Minigames available: [gamehere]", True, black), (10, 90))
        screen.blit(font.render("If it is locked, click to unlock if you have enough Score.", True, black), (10, 110))
        screen.blit(font.render("If the game you want to play is unlocked, click to play if you have enough Score.", True, black), (10, 130))
        screen.blit(font.render("Choose a minigame to play:", True, black), (10, 170))

        if minigamesUnlocked[0]:
            screen.fill(green, minigameSelectBox1)
            screen.blit(font.render("Cost to play: 550 Score", True, black), (16, 235))
        elif not minigamesUnlocked[0]:
            screen.fill(red, minigameSelectBox1)
            screen.blit(font.render("Cost to unlock: 2800 Score", True, black), (16, 235))

        if minigamesUnlocked[1]:
            screen.fill(green, minigameSelectBox2)
            screen.blit(font.render("Cost to play: 2250 Score", True, black), (16, 305))
        elif not minigamesUnlocked[1]:
            screen.fill(red, minigameSelectBox2)
            screen.blit(font.render("Cost to unlock: 16500 Score", True, black), (16, 305))

        if minigamesUnlocked[2]:
            screen.fill(green, minigameSelectBox3)
            screen.blit(font.render("Cost to play: 6750 Score", True, black), (16, 375))
        elif not minigamesUnlocked[2]:
            screen.fill(red, minigameSelectBox3)
            screen.blit(font.render("Cost to unlock: 25000 Score", True, black), (16, 375))

        screen.blit(font.render("Asteroids", True, black), (16, 215))
        screen.blit(font.render("Coming Soon", True, black), (16, 285))
        screen.blit(font.render("Coming Soon", True, black), (16, 355))

        # We need to tell the player how much score they have of course #
        screen.blit(font.render("You have " + str(counter) + " score.", True, black), (600, 10))

        screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
        clock.tick(61)
        pygame.display.flip()


    # MINIGAME 1 #
    while whatScreen == "minigame1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if asteroidsScore > asteroidsHighScore:
                    asteroidsHighScore = asteroidsScore
                save()
                gameRunning = False
                exitScreen()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if asteroidsScore > asteroidsHighScore:
                        asteroidsHighScore = asteroidsScore
                    asteroidsScore = 0
                    whatScreen = "minigameSelect"
                if event.key == pygame.K_LEFT:
                    if not asteroidsSpaceshipPos[0] < 25:
                        asteroidsSpaceshipPos[0] -= 7
                if event.key == pygame.K_RIGHT:
                    if not asteroidsSpaceshipPos[0] > 700:
                        asteroidsSpaceshipPos[0] += 7
                if event.key == pygame.K_SPACE:
                    if canShoot:
                        name = str(random.randint(0, 10000))
                        #missiles[name] = [asteroidsSpaceshipPos[0] + 25, asteroidsSpaceshipPos[1] + 20]
                        missiles[name] = [pygame.Rect(asteroidsSpaceshipPos[0] + 25, asteroidsSpaceshipPos[1] + 20, 20, 20)]
                        canShoot = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if not canShoot:
                        canShoot = True

        if not destroyed:
            if random.randint(0, 60) == 27:
                name = str(random.randint(0, 10000))
                if random.randint(0, 11) <= 7:
                    #asteroids[name] = [random.randint(30, 750), -35, asteroidsAsteroid]
                    asteroids[name] = [pygame.Rect(random.randint(30, 750), -35, 70, 70), asteroidsAsteroid]
                else:
                    #asteroids[name] = [random.randint(30, 750), -35, asteroidsAlien]
                    asteroids[name] = [pygame.Rect(random.randint(30, 750), -35, 70, 70), asteroidsAlien]

            screen.blit(asteroidsBG, (-300, 0))
            screen.blit(asteroidsSpaceship, (asteroidsSpaceshipPos[0], asteroidsSpaceshipPos[1]))

            for asteroid in list(asteroids):
                asteroids[asteroid][0].top += 4
                screen.blit(asteroids[asteroid][1], (asteroids[asteroid][0].left, asteroids[asteroid][0].top))
                if asteroids[asteroid][0].top >= 550:
                    asteroids.pop(asteroid)

            for missile in list(missiles):
                missiles[missile][0].top -= 7
                screen.blit(asteroidsBullet, (missiles[missile][0].left, missiles[missile][0].top))
                if missiles[missile][0].top <= -50:
                    missiles.pop(missile)

            # COLLISION CHECKS #

            # missiles/asteroids
            for missile in list(missiles):
                for asteroid in list(asteroids):
                    if missiles[missile][0].colliderect(asteroids[asteroid][0]):
                        missiles.pop(missile)
                        asteroids.pop(asteroid)
                        asteroidsScore += random.randint(1, 4)
                        break

            #asteroids/ship

        screen.blit(font.render("Minigame Score: {}".format(asteroidsScore), True, white), (10, 10))
        screen.blit(font.render("Minigame Highscore: {}".format(asteroidsHighScore), True, white), (10, 30))
        screen.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, black), (700, 470))
        clock.tick(61)
        asteroidsFrameUpdate = True
        pygame.display.flip()

