import sys, pygame, math, json, os, threading, time

pygame.init()
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption('Clicky')

# Initialize variables and load files #
font = pygame.font.Font(None, 25)

logo = pygame.image.load(os.path.join(sys.path[0], "images/logo.png"))

white = [255, 255, 255]
black = [0, 0, 0]

counter = 88888
mult = 1
multCost = 100
perSecond = 0
perSecondCost = 1000
saves = {}
gameRunning = True

# Menu variables #
firstTimeOpening = True
inAboutScreen = False

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
        mult = int(saves["mult"])
        multCost = int(saves["multCost"])
        perSecond = int(saves["perSecond"])
        firstTimeOpening = saves["firstTimeOpening"]
        perSecondCost = int(saves["perSecondCost"])

# Load scores #
load()

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
                elif inAboutScreen:
                    inAboutScreen = False
            
            elif check_click(event.pos, aboutBox):
                if not inAboutScreen:
                    inAboutScreen = True

            elif check_click(event.pos, scoreBox):
                print(counter)
                counter += 1 * mult
                print(counter)

            elif check_click(event.pos, getMultBox):
                if counter >= multCost:
                    counter -= multCost
                    mult += 1
                    multCost += 100

            elif check_click(event.pos, getPerSecondBox):
                if counter >= perSecondCost:
                    counter -= perSecondCost
                    perSecond += 1
                    perSecondCost+= 500

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
        screen.blit(font.render("Clicky Version 1.1!", True, black), (10, 10))
        screen.blit(font.render("Written entirely in Python 3.6.5 and Pygame 1.9.4", True, black), (10, 30))
        screen.blit(font.render("Update 1.1 Changelog:", True, black), (10, 50))
        screen.blit(font.render(" - Added per second bonus, first time opening screen,", True, black), (10, 70))
        screen.blit(font.render("   About screen, and did some backend work.", True, black), (10, 90))
        screen.blit(font.render("Clicky is open source. See code at https://github.com/Lumiobyte/clicker", True, black), (10, 110))
        screen.blit(font.render("Clicky © 2019 Cockatoo Development Studios. See our website at https://cockatoo.dev!", True, black), (10, 130))
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