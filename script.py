import sys, pygame, math, json, os, threading, time

pygame.init()
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption('Clicky')
icon = pygame.image.load(os.path.join(sys.path[0], "images/icon.png"))
pygame.display.set_icon(icon)

# Initialize variables and load files #
font = pygame.font.Font(None, 25)

logo = pygame.image.load(os.path.join(sys.path[0], "images/logo.png"))

white = [255, 255, 255]
black = [0, 0, 0]

counter = 0
mult = 1
multCost = 100
perSecond = 0
perSecondCost = 1000
saves = {}
gameRunning = True
errorLoading = False

# Menu variables #
firstTimeOpening = True
inAboutScreen = False
isInErrorScreen = False
splashScreen = True

scoreBox = (325, 75, 300, 100)
getMultBox = (325, 200, 300, 100)
getPerSecondBox = (325, 325, 300, 100)
okBox = (325, 200, 50, 50)
aboutBox = (40, 445, 80, 50)

# FUNCTIONS #

def secondLoop():
    global counter
    while gameRunning:
        counter += perSecond
        time.sleep(1)

def load():
    with open(os.path.join(sys.path[0], "save.json"), "r") as file:
        global counter
        global mult
        global multCost
        global saves
        global perSecond
        global firstTimeOpening
        global perSecondCost
        saves = json.load(file)
        counter = int(saves["score"])
        mult = int(saves["multi"])
        multCost = int(saves["multCost"])
        perSecond = int(saves["perSecond"])
        firstTimeOpening = saves["firstTimeOpening"]
        perSecondCost = int(saves["perSecondCost"])

# Load scores #
try:
    load()
except Exception as e:
    errorLoading = True
    isInErrorScreen = True
    print("Can't load scores. Is the file corrupted or has it been moved? Error screen opened in application.")
    print("Error: {}".format(str(e)))

def save():
    saves["score"] = counter
    saves["multi"] = mult
    saves["multCost"] = multCost
    saves["perSecond"] = perSecond
    saves["firstTimeOpening"] = firstTimeOpening
    saves["perSecond"] = perSecond
    saves["perSecondCost"] = perSecondCost

    with open(os.path.join(sys.path[0], "save.json"), "w") as file:
        json.dump(saves, file)

def check_click(position, target):
    print("x " + str(position[0]))
    print("y " + str(position[1]))
    print("target 1 " + str(target[0]))
    print("target 2 " + str(target[1]))
    print("target 3 " + str(target[2]))
    print("target 4 " + str(target[3]))
    if ((position[0] > target[0] and position[0] < target[0] + target[2]) and (position[1] > target[1] and position[1] < target[1] + target[3])):
        print("Good!")
    return ((position[0] > target[0] and position[0] < target[0] + target[2]) and (position[1] > target[1] and position[1] < target[1] + target[3]))

# Start the loop #
secondLoopThread = threading.Thread(target=secondLoop)
secondLoopThread.start()

# Main event handler and game process #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            gameRunning = False
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if check_click(event.pos, okBox):
                if firstTimeOpening:
                    firstTimeOpening = False
                elif isInErrorScreen:
                    isInErrorScreen = False
                elif inAboutScreen:
                    inAboutScreen = False
            
            elif check_click(event.pos, aboutBox):
                if not inAboutScreen:
                    inAboutScreen = True

            elif check_click(event.pos, scoreBox):
                if not firstTimeOpening and not isInErrorScreen and not inAboutScreen:
                    print(counter)
                    counter += 1 * mult
                    print(counter)

            elif check_click(event.pos, getMultBox):
                if not firstTimeOpening and not isInErrorScreen and not inAboutScreen:
                    if counter >= multCost:
                        counter -= multCost
                        mult += 1
                        multCost += 100

            elif check_click(event.pos, getPerSecondBox):
                if not firstTimeOpening and not isInErrorScreen and not inAboutScreen:
                    if counter >= perSecondCost:
                        counter -= perSecondCost
                        perSecond += 1
                        perSecondCost+= 500

    # If it is the first time the user has opened the game or the database has been reset, show information #
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
        pygame.display.flip()

    # About Screen #
    elif inAboutScreen:
        screen.fill(white)
        screen.fill(black, okBox)
        screen.blit(font.render("Ok", True, white), (335, 210))
        screen.blit(font.render("Clicky Version 1.0!", True, black), (10, 10))
        screen.blit(font.render("Written entirely in Python 3.6.5 and Pygame 1.9.4", True, black), (10, 30))
        screen.blit(font.render("Update 1.0 Changelog:", True, black), (10, 50))
        screen.blit(font.render(" - Added splash screen, main game mechanics,", True, black), (10, 70))
        screen.blit(font.render("   Game icon, and did some backend work.", True, black), (10, 90))
        screen.blit(font.render("Clicky is open source. See code at https://github.com/Lumiobyte/clicker", True, black), (10, 110))
        screen.blit(font.render("Clicky © 2019 Cockatoo Development Studios. See our website at https://cockatoo.dev!", True, black), (10, 130))
        pygame.display.flip()

    # About Screen #
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


        # Make stuff work? #
        pygame.display.flip()