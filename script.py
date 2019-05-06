import sys, pygame, math, json, os, threading, time

pygame.init()
screen = pygame.display.set_mode([550, 500])
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
saves = {}

scoreBox = (200, 75, 300, 200)
getMultBox = (200, 300, 300, 200)

# FUNCTIONS #

def secondLoop():
    global counter
    while True:
        counter += perSecond
        time.sleep(1)

def load():
    with open(os.path.join(sys.path[0], "save.json"), "r") as file:
        global counter
        global mult
        global multCost
        global saves
        global perSecond
        saves = json.load(file)
        counter = int(saves["score"])
        mult = int(saves["mult"])
        multCost = int(saves["multCost"])
        perSecond = int(saves["perSecond"])

# Load scores #
load()

def save():
    saves["score"] = counter
    saves["multi"] = mult
    saves["multCost"] = multCost
    saves["perSecond"] = perSecond

    with open(os.path.join(sys.path[0], "save.json"), "w") as file:
        json.dump(saves, file)

def check_click(loc, area):
    return ((loc[0] > area[0] and loc[0] < area[0] + area[2]) and (loc[1] > area[1] and loc[1] < area[1] + area[3]))

# Start the loop #
secondLoopThread = threading.Thread(target=secondLoop)
secondLoopThread.start()

# Main event handler and game process #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if check_click(event.pos, scoreBox):
                counter += 1 * mult

            elif check_click(event.pos, getMultBox):
                if counter >= multCost:
                    counter -= multCost
                    mult += 1
                    multCost += 100

    # Scale the logo image #
    logoScaled = pygame.transform.scale(logo, (175, 175))

    # Draw to screen #
    screen.fill(white)
    screen.fill(black, scoreBox)
    screen.fill(black, getMultBox)
    screen.blit(logoScaled, (10, 320))


    # Render text #
    screen.blit(font.render("You have " + str(counter) + " score.", True, black), (10, 10))
    screen.blit(font.render("You have " + str(mult) + " multiplier.", True, black), (10, 25))
    screen.blit(font.render("You get " + str(perSecond) + " score per second.", True, black), (10, 40))
    screen.blit(font.render("Click here to get score!", True, white), (200, 75))
    screen.blit(font.render("Click here to get multiplier!".format(multCost), True, white), (200, 300))
    screen.blit(font.render("Cost: {} score".format(multCost), True, white), (200, 320))


    # Make stuff work? #
    pygame.display.flip()