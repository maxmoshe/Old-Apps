"""
This is an example for a bot.
"""
#
#NOTE::::::::::::::::::
#we should really find the time to organize the code into files.
#

from elf_kingdom import *
from LocationFuncs import *
import math

#PORTALS:
#DO NOT USE MOD WITH PORTALS.
DEFEND_PORTAL_MULT = 1.2
SUMMON_ATTACKERS_MULT = 1.5
SUMMON_TORANDO_MULT = 1
MANA_WASTE = 20 #if my mana/summon cost > 20: score * 5
GIANT_MANA_SCORE = 2.5

#ELFS:
CHASE_ELF_MULT = 1
ATTACK_FOUNTAIN_MULT = 4 #DO NOT ASK ME WHY THIS WORKS. it does
ATTACK_FOUNTAIN_RANGE = 2500 #as range increases, distance score gets more problematic - averge score goes up
BUILD_PORTAL_MOD = 0.3
BUILD_FOUNTAIN_MOD = 0
DANGEROUS_PORTAL_MOD = 0.2

DANGER_RADIUS = 1000 #CHANGE THIS IN LOCATION FUNCS TOO.
SOFT_MANA_MIN = 0
MAX_CASTLE_HEALTH = 151
PORTAL_RADIUS = 500
CASTLE_RADIUS = 769
QUOTES = ["MESSING WITH CONSTANTS IS UNCONSTITUTIONAL.",
            "They'll set up portals in the middle of the map, influence and infiltrate our territory and government with anti-male elf propaganda in the hopes that it'll bring down what they've labelled the 'perpetually-oppressive cis-gender hetero-normative capitalist amphibian castle'.",
            "The curse of zadoom is a synthetic completely fake with actors, in my view, manufactured. I couldn't believe it at first. I knew they had actors there, clearly, but I thought they killed some real elfiot.",
            "REJOICE TO GOD ALMIGHTY FOR THIS ANIMATING CONTEST OF LIBERTY! AAAAAAGGNNNGGHHHUUUGGHHH!",
            "The reason there are so many elfiot now is because it's a chemical warfare operation. I have the government documents.",
            "YOU'LL NEVER DEFEAT THE HUMAN SPIRIT! YOU'LL NEVER DEFEAT GOD! YOU'LL NEVER WIN! NEVER! NEVER EVER! NEVER!",
            "I don't like 'em putting chemicals in the mana that turn the freakin' trolls gay!",
            "this is not human intelligence, OK? IT'S NOT HUMAN INTELLIGENCE WE'RE FACING!",
            "Liberty is rising. Liberty is rising! Freedom will not stop! You will not stop freedom! You will not stop the Republic! Humanity is awakening! Infowars dot com!",
            "we're coming for ya we're coming straight for ya and you know it that's why you're so scared that's why you're moving so fast now, and you just better keep doing that dance",
            "I'm like a chimpanzee, in a tree, jumping up and down, warning other chimpanzees when I see a big cat coming through the woods... I'm the weirdo? Because I'm sitting in a tree going OOH OOH AAH AAH AAH OOH AAH AAH OOH OOH OOH AAH AAH AAH AAH AAH!?",
            "I'm telling you it's what zadoom said. It's what he warned of. It's what we're dealing with. They're demons. They're freaking inter dimensional invaders.",
            "YOU WANTED TO OVERRUN US, AND POISON US, AND TAKE OUR FAMILIES, AND KILL US!?!? YOOOOUUUU WILL DIE, NOT US! YOU ANTI-HUMAN CRAP!",
            "Ive been in bed with probably 300 women.",
            "I'M IN COMPETITION WITH THE DEVIL. I'M IN A DEATH BATTLE!",
            "JUST TAKE THE RED PILL PEOPLE!!!",
            "SCANNING... CONTROL... MANIPULATE SCIENTIFIC DATA... TAKE OVER. BLAST. CONTROL. WORLD GOVERNMENT... SHUTDOWN INFRASTRUCTURE... SHIP EVERYTHING TO CHINA...",
            "A young Talmid Chacham, arrived from chutz laaretz."]

class StateHistory:
    lastState = None
    currentState = None

    
class GameState:
    
    def __init__(self, game):
        self.enemyElves = game.get_all_enemy_elves()
        self.enemyGiants = game.get_enemy_lava_giants()
        self.enemyTrolls = game.get_enemy_ice_trolls()


class Action:
    def __init__(self, score, action_function, game=None, elf=None, *args):
        self.score = score
        self.action_function = action_function
        self.game = game
        self.elf = elf
        self.args = args
        
    def do_action(self):
        self.action_function(self.game, self.elf, *self.args)

    def __str__(self):
        return "Action strategy: %s score %.2f" % (self.action_function.__name__, self.score)


class Summon:
    def __init__(self, score, summon_function, cost=0, *args):
        self.score = score
        self.summon_function = summon_function
        self.cost = cost
        self.args = args
        
    def do_summon(self):
        self.summon_function(*self.args)

    def __str__(self):
        return "Summon strategy: %s score %.2f" % (self.summon_function.__name__, self.score)


def do_turn(game):
    #PRINT QUOTE
    quote = QUOTES[game.turn/45]
    print(quote)
        
    
    
    gameState = GameState(game)
    StateHistory.lastState = StateHistory.currentState
    StateHistory.currentState = gameState

    # Give orders to my elves.
    handle_elves(game)
    # Give orders to my portals.
    handle_portals(game)


portalLocations = []
manaFountainLocations = []
portalManaFlag = False
fountainManaFlag = False
def handle_elves(game):
    global portalLocations
    global manaFountainLocations
    global portalManaFlag
    global fountainManaFlag
    
    portalManaFlag = False
    fountainManaFlag = False
    
    portalLocations = getPortalLocations(game)
    manaFountainLocations = getManaFountainLocations(game)
    
    action_functions = [getElfAttackCastle, getElfAttackElf, getElfMakePortal, getElfKite, getElfAttackDangerousPortal, getElfAttackPortal, getElfMakeManaFountain, getElfAttackManaFountain, getElfInvis]

    free_elves = game.get_all_my_elves()

    while len(free_elves) > 0:
        actions = []
        #the way this loop is programmed makes assigning each elf a set number in the beginning of the game unnecessary
        for elf in free_elves:
            if not elf.is_alive():
                continue #skips current iteration
            if elf.is_building:
                continue
            
            for action in action_functions:
                actions.append(action(game, elf)) #get all of the actions
            
        if len(actions) == 0:
            break

        actions = sorted(actions, key=lambda action: action.score, reverse=True) #get the action with the highest score
        best_action = actions[0]
        #print("Elf %s:\n\t%s" % (best_action.elf.id, best_action))
        free_elves.remove(best_action.elf)
        if best_action.action_function is elfAttackManaFountain:
            action_functions.remove(getElfAttackManaFountain)
            print('GAZA GAZA GAZA!!!!!!!!!!!!!!')
        best_action.do_action()

turnsSinceBait = 50
def handle_portals(game):
    print("Portals:")
    
    #TODO this is defense bait test
    global turnsSinceBait
    turnsSinceBait += 1
    #print(turnsSinceBait)
    
    if len(game.get_my_portals()) == 0:
        return
    
    if turnsSinceBait > 50:
        attackPortal = getMyClosestPortals(game, game.get_enemy_castle(), 1)[0]
        if attackPortal.can_summon_lava_giant():
            spawnLavaGiant(game, [attackPortal])
            print("jebaited")
    
    summons = []
    #summons.append(getFaceRace(game))
    for portal in game.get_my_portals():
        portalSummons = []
        portalSummons.append(getSummonCastleDefenders(game, portal))
        portalSummons.append(getSummonPortalDefenders(game, portal))
        portalSummons.append(getSummonCastleAttackers(game, portal))
        portalSummons.append(getSummonTornado(game, portal))
        portalSummons = sorted(portalSummons, key=lambda summon: summon.score, reverse=True)
        summons.append(portalSummons[0])
        
        
    
    # Sort summons by descending score
    summons = sorted(summons, key=lambda summon: summon.score, reverse=True)
    #print("Summon options:\n\t%s" % '\n\t'.join(map(str, summons))) #PRINTOFF
    total_mana = game.get_my_mana()


    
    
    for summon in summons:
        if summon.summon_function is doNothing:
            break
        if game.get_my_mana() / summon.cost + 0.01 > MANA_WASTE:
            summon.score = summon.score * 5
        if summon.score < 0.15 or total_mana < summon.cost:
            break
        if portalManaFlag and fountainManaFlag and total_mana < summon.cost + game.portal_cost + game.mana_fountain_cost:
            break
        if portalManaFlag and total_mana < summon.cost + game.portal_cost:
            break
        if fountainManaFlag and total_mana < summon.cost + game.mana_fountain_cost:
            break
        
        summon.do_summon()
        total_mana -= summon.cost


def getElfBuildLocation(game, elf):
    "Get location in which the elf should build a portal."
    if len(game.get_my_living_elves()) == 0:
        return
    singleBestLocation = getBestPortalLocations(game, 1)
    bestPortalLocations = getBestPortalLocations(game, 2)
    
    if singleBestLocation is None:
        return
    
    if len(game.get_my_living_elves()) == 1: #maybe return closer one out of 2 getBestPortalLocations
        if bestPortalLocations is not None:
            if elf.distance(bestPortalLocations[0]) < elf.distance(bestPortalLocations[1]):
                return bestPortalLocations[0]
            return bestPortalLocations[1]
        return singleBestLocation

    elf1, elf2 = game.get_all_my_elves()
    if elf1 == elf:
        otherElf = elf2
    else:
        otherElf = elf1

    if getBestPortalLocations(game, 2) is None:
        if elf.distance(singleBestLocation) < otherElf.distance(singleBestLocation):
            return singleBestLocation
        return


    elfDistances = [elf.distance(bestPortalLocations[0]), elf.distance(bestPortalLocations[1])]
    otherElfDistances = [otherElf.distance(bestPortalLocations[0]), otherElf.distance(bestPortalLocations[1])]
    if elfDistances[0] < otherElfDistances[0]:
        # if the elf is closer than other elf to both portals
        if elfDistances[1] < otherElfDistances[1]:
            if elfDistances[0] < elfDistances[1]:
                # if first portalLoc is closer, go to it
                return bestPortalLocations[0] 
            # if second portalLoc is closer, go to it.
            return bestPortalLocations[1]
        return bestPortalLocations[0] #if elf is closer to first portal from getBestPortalLocations(), go to it.

    # Elf is further from first portal
    if elfDistances[1] > otherElfDistances[1]:
        if otherElfDistances[0] > otherElfDistances[1]:
            # if first portalLoc is closer, go to it
            return bestPortalLocations[0] 
        else:
            # if second portalLoc is closer, go to it.
            return bestPortalLocations[1]
    return bestPortalLocations[1]


def kite(game, elf):
    # Move away from corners
    print("OUT OF THE SEWER, LITERAL VAMPIRE POT BELLIED GOBLINS ARE HOBBLING AROUND COMING AFTER US!")
    if getSideOfMap(game) == 'left':
        direction = -300
    else:
        direction = 300

    if elf.location.row > game.rows - 350 or elf.location.row < 350:
        newLocation = Location(row=elf.location.row, col=elf.location.col + direction)
        elf.move_to(newLocation)
    else:
        closestElf = getClosestEnemyElf(game, elf)
        closestTroll = getClosestIceTroll(game, elf)
        if not len(game.get_enemy_ice_trolls()) == 0:
            if not len(game.get_enemy_living_elves()) == 0:
                if elf.distance(closestElf) < elf.distance(closestTroll):
                    elf.move_to(elf.location.towards(closestElf, -300))
            elf.move_to(elf.location.towards(closestTroll, -300))
        if not len(game.get_enemy_living_elves()) == 0:
            elf.move_to(elf.location.towards(closestElf, -300))
        
        
        
        
def generalAI(game, elf):
    print('Elf is running GeneralAI.')
    # GENERAL ai
    if not elf.is_alive():
        print('I am dead.')
        return

    # print ("Elf location: %d, %d, %d" % (elf.location.row, elf.location.col, game.rows))

    if len(game.get_enemy_living_elves()) > 0: #if there are enemy elves in my range, attack them.
        if elf.in_attack_range(getClosestEnemyElf(game, elf)):
            elf.attack(getClosestEnemyElf(game, elf))
            print('Elves will be crushed I can taste your weakness crushing crushing crushing.')
            return
    
    for enemyElf in game.get_enemy_living_elves(): #if enemy elf is close enough to build a dangerous portal, go kill him.
        if enemyElf.distance(game.get_my_castle()) < 2000: #what if we're dangerous? 
            if elf.distance(enemyElf) < 1300: #WHAT IF I AM?
                print('DESTROY THE CHILD')
                elf.move_to(enemyElf)
                return
    
    if len(game.get_enemy_ice_trolls()) > 0: #if there are enemy trolls in kite range, kite them.
        if elf.distance(getClosestIceTroll(game, elf)) < 500:
            kite(game, elf)
            print('Running from a troll.')
            return
    
    buildLocation = getElfBuildLocation(game, elf)
    if buildLocation is not None: #checks for orders to build portal.
        if len(game.get_my_portals()) < 6:
            elfMakePortal(game, elf, buildLocation)
            return
    
    if len(game.get_enemy_portals()) > 0: #there are portals - go attack them
        if elf.in_attack_range(getClosestEnemyPortal(game,elf)):
            print('Attacking closest enemy portal.')
            elf.attack(getClosestEnemyPortal(game,elf))
            return
        else:
            print('Let me tell all the scum and all the leftists: youre going to lose all of your portals soon.')
            elf.move_to(getClosestEnemyPortal(game,elf))
            return
        
    elif len(game.get_enemy_living_elves()) > 0:#there are elves - go attack them.
        elf.move_to(getClosestEnemyElf(game,elf))
        print("We're coming for ya we're coming straight for ya and you know it that's why you're so scared that's why you're moving so fast now, and you just better keep doing that dance")
        return
    else:
        elfAttackCastle(game, elf)
        print('Im a pioneer. Im an explorer. Im an elfit, and im coming.')
        return


            
def elfDefend(game, elf):
    if len(game.get_enemy_lava_giants()) <= 0: #if there are ice trolls, kite them.
        return

    print('Defend')
    closestEnemy = game.get_enemy_lava_giants()[0] #gets the closest enemy and prints range from it.
    for enemy in game.get_enemy_creatures():
        if elf.distance(enemy) < elf.distance(closestEnemy):
            closestEnemy = enemy
    print(elf.distance(closestEnemy))
    if elf.in_attack_range(closestEnemy):
        elf.attack(closestEnemy)
    else:
        elf.move_to(closestEnemy)
            
def elfAttackCastle(game, elf):
    if elf.in_attack_range(game.get_enemy_castle()):
        elf.attack(game.get_enemy_castle())
    else:
        elf.move_to(game.get_enemy_castle())


def getGiantEffectiveHP(game, giant):
    time = (giant.distance(game.get_my_castle()) - CASTLE_RADIUS) / game.lava_giant_max_speed
    effectiveHP = giant.current_health - time * game.lava_giant_suffocation_per_turn
    return effectiveHP

    
def getMyTotalGiantEffectiveHP(game, loc, radius):
    giants = game.get_enemy_lava_giants()
    if len(giants) == 0:
        return 0
    total = 0
    for giant in giants:
        if giant.distance(loc) <= radius:
            total += getGiantEffectiveHP(game, giant)
    return total
    
def getEnemyTotalGiantEffectiveHP(game, loc, radius):
    giants = game.get_enemy_lava_giants()
    if len(giants) == 0:
        return 0
    total = 0
    for giant in giants:
        # print ("totalGiantEffective distance: %s %s %s" %(giant, loc, giant.distance(loc)))
        if giant.distance(loc) <= radius:
            # print ("giantHp: %s %s" %(giant, getGiantEffectiveHP(game, giant)))
            total += getGiantEffectiveHP(game, giant)
    return total

def getMyHealthyIceTrolls(game, loc, radius):
    trolls = game.get_my_ice_trolls()
    if len(trolls) == 0:
        return 0
    total = 0
    
    for troll in trolls:
        if troll.current_health > game.ice_troll_max_health * 0.4:
            if troll.distance(loc) <= radius:
                total += 1
    return total

def getEnemyHealthyIceTrolls(game, loc, radius):
    trolls = game.get_enemy_ice_trolls()
    if len(trolls) == 0:
        return 0
    total = 0
    
    for troll in trolls:
        if troll.current_health > game.ice_troll_max_health * 0.4:
            if troll.distance(loc) <= radius:
                total += 1
    return total
    
def getMyHealthyTornadoes(game, loc, radius):
    trolls = game.get_my_tornadoes()
    if len(trolls) == 0:
        return 0
    total = 0
    
    for troll in trolls:
        if troll.current_health > game.tornado_max_health * 0.4:
            if troll.distance(loc) <= radius:
                total += 1
    return total
    
def getEnemyHealthyTornadoes(game, loc, radius):
    trolls = game.get_enemy_tornadoes()
    if len(trolls) == 0:
        return 0
    total = 0
    
    for troll in trolls:
        if troll.current_health > game.tornado_max_health * 0.4:
            if troll.distance(loc) <= radius:
                total += 1
    return total
    
def getAverageGiantLocation(game, loc, radius):
    locations = []
    for giant in game.get_enemy_lava_giants():
        if getGiantEffectiveHP(giant) > 1:
            if giant.distance(loc) <= radius:
                locations.append(giant.location)
                
    if len(locations) == 0:
        return
    
    totalLocation = Location(0, 0)
    for location in locations:
        totalLoc
        
    totalLocation.multiply(0.5)
    return total
                
                
            
    
def spawnIceTroll(game, portals): #check if lava giants in certain range, if they are, spawn trolls from 
    #closest portal to the closest lava giant to our castle.
    for portal in portals:
        if portal.can_summon_ice_troll():
            portal.summon_ice_troll()
            print("Portal %s: WE'RE UNDER ATTACK. EVERYBODY'S UNDER ATTACK." %(portal.id))

def spawnLavaGiant(game,portals): #for portal in portals if portal is close enough, spawn giants. if none, spawn from closest.
    global turnsSinceBait
    for portal in portals:
        if portal.can_summon_lava_giant():
            portal.summon_lava_giant()
            print("portal %s: HuAHHHHHHHH MURDER CASTLE! INVASION FORCE! RELEASE US!" % portal.id)
            turnsSinceBait = 0

def spawnTornado(game, portals):
    for portal in portals:
        if portal.can_summon_tornado():
            portal.summon_tornado()
            print("portal %s: The government can create and steer groups of tornadoes.")

def getSummonTornado(game, portal): #TODO make this depend on number and not distancce
    maxDistance = game.tornado_max_health * game.tornado_max_speed/ game.tornado_suffocation_per_turn
    
    if len(game.get_enemy_mana_fountains()) > 0:
        closestObjectDistance = portal.distance(getClosestEnemyFountain(game, portal))
        if len(game.get_enemy_portals()) > 0:
            closestObjectDistance = min(portal.distance(getClosestEnemyPortal(game, portal)), portal.distance(getClosestEnemyFountain(game, portal)))
    elif len(game.get_enemy_portals()) > 0:
        closestObjectDistance = portal.distance(getClosestEnemyPortal(game, portal))
    else:
        return Summon(0, doNothing)
        
    num = 0
    for enemyPortal in game.get_enemy_portals():
        if portal.distance(enemyPortal) < maxDistance * 0.6:
            num += 1
    for fountain in game.get_enemy_mana_fountains():
        if portal.distance(fountain) < maxDistance * 0.6:
            num += 1

    distanceScore = getDistanceScore(closestObjectDistance, maxDistance)
    
    numScore = num/float(3)
    existingToranadoes = getMyHealthyTornadoes(game, portal.location, maxDistance)
    existingToranadoesScore =  (2 - existingToranadoes)/2
    score = numScore * SUMMON_TORANDO_MULT * existingToranadoesScore * distanceScore
    #print("portal: %s \n\t distanceScore: %s \n\t score: %s" %(portal, distanceScore, score))
    
    return Summon(score, spawnTornado, game.tornado_cost, game, [portal])

def getSummonCastleDefenders(game, portal): #add defense from and elf in castle range. #TODO: FUX SCORE FOR ENTIRE FUNCTION
    #getBestSummon will always call this with 1 to 3, if enough portals exist.
    effectiveHp = getEnemyTotalGiantEffectiveHP(game, game.get_my_castle().location, 2500 + CASTLE_RADIUS)
    healthyTrolls = getMyHealthyIceTrolls(game, game.get_my_castle().location, 2500 + CASTLE_RADIUS)
    averageLoc = game.get_my_castle().location.towards(game.get_enemy_castle(), 1000) #calculate this. this is bad.
    
    multiplier = effectiveHp / 15 / (healthyTrolls + 0.1) #this should range from 0 to 1.

    
    distance = portal.distance(averageLoc)
    distanceScore = getDistanceScore(distance, 1500, game.portal_size)
    score = multiplier * distanceScore #multiplier / math.sqrt(distance) #TODO
    #print("""Summon castle defenders #PRINTOFF
   #     score: %s
   #     effectiveHp: %s
   #     multiplier %s""" %(score, effectiveHp, multiplier)
   # )
    return Summon(score, spawnIceTroll, game.ice_troll_cost, game, [portal])

def getSummonPortalDefenders(game, portal):
    if len(game.get_enemy_living_elves()) == 0:
        return Summon(0, doNothing)

    closestElfDistance = portal.distance(getClosestEnemyElf(game, portal))
    
    if closestElfDistance is None or closestElfDistance > 1500:
        return Summon(0, doNothing)

    closestElfDistance = max(closestElfDistance - PORTAL_RADIUS, 1)
    healthyTrolls = getMyHealthyIceTrolls(game, portal, 1500)
    #enemyHealthyTrolls = getEnemyHealthyIceTrolls(game, portal, 1000)
    #enemyIceTrollScore = ((3 - enemyHealthyTrolls) / float(3))
    healthyTrollsScore = (3 - healthyTrolls)/3
    score = healthyTrollsScore * getDistanceScore(closestElfDistance, 1500) * DEFEND_PORTAL_MULT

    #print("Summon portal defenders score: %s" % (score)) #PRINTOFF
    return Summon(score, spawnIceTroll, game.ice_troll_cost, game, [portal])

def doNothing(*args):
    pass
    
def getSummonCastleAttackers(game, portal):
    #should depend on available mana, enemy's castle health, distance
    mana = game.get_my_mana()
    if portalManaFlag:
        mana -= game.portal_cost
    if fountainManaFlag:
        mana-= game.mana_fountain_cost
    
    enemyCastleHealth = game.get_enemy_castle().current_health
    #closestPortal = getMyClosestPortals(game, game.get_enemy_castle(), 1)[0]
    # distance = closestPortal.distance(game.get_enemy_castle()) - CASTLE_RADIUS
    manaScore = float(mana) / game.lava_giant_cost / GIANT_MANA_SCORE #maybe make this double/float

    castleHealthScore = (MAX_CASTLE_HEALTH - enemyCastleHealth) / MAX_CASTLE_HEALTH

    portalEffectiveness = getAttackPortalEffectiveness(game, portal)
    score = manaScore * portalEffectiveness * SUMMON_ATTACKERS_MULT
    #print("Summon attackers score: %s, portal effectiveness %s, manaScore %s" % (score, portalEffectiveness, manaScore)) #PRINTOFF
    return Summon(score, spawnLavaGiant, game.lava_giant_cost, game, [portal])

def getFaceRace(game):
    if len(game.get_enemy_living_elves()) is not 2:
        return Summon(0, doNothing)
    closestPortal = getMyClosestPortals(game, game.get_enemy_castle(), 1)[0]
    closestPortalDistance = closestPortal.distance(game.get_enemy_castle())
    elfDistance = getClosestEnemyElf(game, closestPortal) #gets closest elf to attack portal
    myCastle = game.get_my_castle()

    if elfDistance > 2000 and closestPortalDistance < 2000:
        if game.get_enemy_castle().current_health < myCastle.current_health or getEnemyTotalGiantEffectiveHP(game, myCastle, 1200) < 20:
            return Summon(10, spawnLavaGiant, game.lava_giant_cost, game, [closestPortal])
    return Summon(0, doNothing)

def getAttackPortalEffectiveness(game, portal, portalOwner = 1):
    maxLivingDistance = game.lava_giant_max_health / game.lava_giant_suffocation_per_turn * game.lava_giant_max_speed / 1.5
    distance = portal.distance(game.get_enemy_castle()) - CASTLE_RADIUS
    if portalOwner == 2:
        distance = portal.distance(game.get_my_castle()) - CASTLE_RADIUS
    return  1 - float(distance) / maxLivingDistance



#-------------------------------------ELF FUNCS-------------------------------------------------    
def getElfAttackCastle(game, elf):
    #maybe this replaces doNothing
    return Action(0.08, elfAttackCastle, game, elf)
    
def getElfAttackElf(game, elf):
    #PRIOROTIZE LOWER HP ELF, IF THERE ARE 2 IN RANGE.
    enemyElf = getClosestEnemyElf(game, elf)
    if enemyElf is None:
        return Action(0, doNothing)
    if getIsDangerous(game, elf.location):
        return Action(0, doNothing)
    
    if elf.distance(enemyElf) <= elf.attack_range:
        for badElf in game.get_enemy_living_elves():
            if elf.distance(badElf) <=elf.attack_range:
                if elf.current_health < enemyElf.current_health:
                    enemyElf = badElf
        
        score = 1
        if elf.invisible:
            score -= 0.9
            
        #TO COMBAT MESSING WITH CONSTANTS.
        if game.elf_max_health / (elf.attack_multiplier + float(0.01)) > 30:
            score = 0
        return Action(score, elfAttackElf, game, elf, enemyElf)
    
    enemyTrolls = getEnemyHealthyIceTrolls(game, elf.location, 800)
    enemyElfs = 0
    for enemyElf in game.get_enemy_living_elves():
        if elf.distance(enemyElf) < 800:
            enemyElfs += 1
    if enemyTrolls == 0:
        if enemyElfs < 2:
            enemyElf = getClosestEnemyElf(game, elf)
            if elf.current_health > enemyElf.current_health:
                distance = elf.distance(enemyElf)
                score = getDistanceScore(distance, 1500, elf.attack_range) * CHASE_ELF_MULT
                
                if elf.invisible:
                    score -= 0.9
    
                return Action(score, elfAttackElf, game, elf, enemyElf)
        
    return Action(0, doNothing)

    
def getElfMakePortal(game, elf): #TODO fix time for mana to work with manaflag
    #this one is complicated since we have a total of 3 portals we can build.
    #maybe split it to 3 different scores and portals?
    #if not, perhaps we should determine the best portal to build using getbestportallocation
    #and then calculate the score in accordance to it.
    #portalLocations = getPortalLocations(game)
    if len(portalLocations) == 0:
        return Action(0, doNothing)
        
    distance = None
    for portalLoc in portalLocations:
        if getIsDangerous(game, portalLoc):
            if elf.distance(portalLoc) > DANGER_RADIUS:
                continue
        if distance is None or elf.distance(portalLoc) < distance:
            closestPortalLoc = portalLoc
            distance = elf.distance(closestPortalLoc)
            
    if distance is None:
        return Action(0, doNothing)
    
    walkTurns = distance/(elf.max_speed+0.01)
    
    mpt = game.get_myself().mana_per_turn
    mana = game.get_myself().mana
    if portalManaFlag:
        mana -= game.portal_cost
    if fountainManaFlag:
        mana -= game.mana_fountain_cost
    
    timeForMana = (game.portal_cost + SOFT_MANA_MIN - mana) / (mpt + 0.01)
    timeForMana -= walkTurns
    timeForMana = (max(float(0.01), timeForMana))
    manaNeededScore = min(1, 2/timeForMana)
    distanceScore = getDistanceScore(distance, 2500)
    score = (1 - float(BUILD_PORTAL_MOD)) * distanceScore * manaNeededScore + BUILD_PORTAL_MOD * manaNeededScore #example: 0.7 *score + 0.3
    score = min(1.1, score)
    if mana / game.portal_cost > MANA_WASTE:
        score = score * 5
    return Action(score, elfMakePortal, game, elf, closestPortalLoc)

def getElfMakeManaFountain(game, elf):
    if len(manaFountainLocations) == 0:
        return Action(0, doNothing)
    
    closestLoc = None
    for loc in manaFountainLocations:
        if getIsDangerous(game, loc):
            continue
        if closestLoc is None or elf.distance(loc) < elf.distance(closestLoc):
            closestLoc = loc
            
    if closestLoc is None:
        return Action(0, doNothing)
            
    walkTurns = elf.distance(closestLoc)/(elf.max_speed + 0.01)
            
    mpt = game.get_myself().mana_per_turn
    mana = game.get_myself().mana
    if portalManaFlag:
        mana -= game.portal_cost
    if fountainManaFlag:
        mana -= game.mana_fountain_cost
    
    timeForMana = (game.mana_fountain_cost + SOFT_MANA_MIN - mana) / (mpt + 0.01)
    timeForMana -= walkTurns
    timeForMana = (max(float(0.01), timeForMana))
    
    manaNeededScore = min(1, 2/timeForMana) #makes sure its max is 1 and min is 
    fountainMpt = game.mana_fountain_mana_per_turn
    manaFountains = len(game.get_my_mana_fountains())
    if fountainManaFlag:
        manaFountains += 1
    fountainsMul = manaFountains ** 2
    if mpt == 0:
        mptScore = 1
    else:
        mptScore = min(2 * fountainMpt / float(game.default_mana_per_turn + fountainsMul * fountainMpt), 1)
    distanceScore = getDistanceScore(elf.distance(closestLoc), 2500)
    score = mptScore * distanceScore * manaNeededScore * (1-float(BUILD_FOUNTAIN_MOD)) + BUILD_FOUNTAIN_MOD * manaNeededScore
    if manaFountains > 2 and game.turn > 25: #short term solution
        score = 0
    #print("loc %s, \n mptScore %s, \n distanceScore %s, \n manaNeededScore %s" %(closestLoc, mptScore, distanceScore,manaNeededScore))
    return Action(score, elfMakeManaFountain, game, elf, closestLoc)
    

def getElfKite(game, elf):
    #score should increase with trolls #TODO
    if len(game.get_enemy_ice_trolls()) == 0 or elf.invisible:
        return Action(0,doNothing)
    enemyElfs = 0
    for enemyElf in game.get_enemy_living_elves():
        if elf.distance(enemyElf) < 500:
            enemyElfs += 1
    if elf.distance(getClosestIceTroll(game, elf)) < 500:
        trolls = getEnemyHealthyIceTrolls(game, elf.location, 500)
        score = 0.75 + float(trolls * 0.1 + enemyElfs * 0.1)
        #if len(game.get_enemy_living_elves()) > 0 and elf.distance(getClosestEnemyElf(game, elf)) <= 500:
            #score = 0
        return Action(score, kite, game, elf)
    if enemyElfs > 1:
        score = 0.75 + float(enemyElfs *0.1)
        return Action(score, kite, game, elf)
    return Action(0,doNothing)
    
def getElfInvis(game, elf): #TODO change to work with elves and portals
    if len(game.get_enemy_ice_trolls()) == 0:
        return Action(0,doNothing)
    if elf.distance(getClosestIceTroll(game, elf)) <= (game.ice_troll_attack_range + 1):
        enemies = getEnemyHealthyIceTrolls(game, elf.location, 500)
        for enemy in game.get_enemy_living_elves():
            if elf.distance(enemy) < 500:
                enemies += 1
        if enemies >= 2:
            manaScore = game.get_my_mana() / game.invisibility_cost / 2
            score = 0.76 + float(enemies * 0.3)
            if elf.can_cast_invisibility():
                if not elf.invisible:
                    return Action(score, useInvis, game, elf)
    return Action(0,doNothing)

def getElfAttackDangerousPortal(game, elf):
    #should depend on:
    #distance to the portal, portal proximity to our castle, portal health (?), number of enemy portals near the portal(?)
    if len(game.get_enemy_portals()) == 0:
        return Action(0,doNothing)

    bestPortalScore = None
    for portal in game.get_enemy_portals():
        portalCastleDistanceScore = getAttackPortalEffectiveness(game, portal, 2)
        elfDistanceScore = getDistanceScore(elf.distance(portal), 2000, PORTAL_RADIUS)
        score = (float(elfDistanceScore) * portalCastleDistanceScore)/(1-DANGEROUS_PORTAL_MOD) + DANGEROUS_PORTAL_MOD
        if getIsDangerous(game, portal.location):
            continue
        if bestPortalScore is None or bestPortalScore < score:
            bestPortalScore = score
            bestPortal = portal
    
    if bestPortalScore is None:
        return Action(0, doNothing)
    
    timeToKill = bestPortal.current_health / (elf.attack_multiplier + float(0.01))
    damageScore = min(1, 8/timeToKill)
    score = (1 - float(DANGEROUS_PORTAL_MOD)) * elfDistanceScore * portalCastleDistanceScore * damageScore + DANGEROUS_PORTAL_MOD * damageScore
    return Action(score, elfAttackPortal, game, elf, bestPortal)

def getElfAttackPortal(game, elf):
    #distance to the portal, number of enemy portals near the portal(?)
    if len(game.get_enemy_portals()) == 0:
        return Action(0, doNothing)
    #run for all portals and get highest score.
    bestPortalScore = None
    for portal in game.get_enemy_portals():
        if getIsDangerous(game, portal.location):
            continue
        distanceScore = getDistanceScore(elf.distance(portal), 1500, PORTAL_RADIUS)
        portalsNearby = len(getMyPortalsInArea(game, portal.location, 1500))
        portalsNearbyScore = (10 - portalsNearby) / float(10)
        score = distanceScore * portalsNearbyScore #maybe add a constant multiplier.
        if bestPortalScore is None or bestPortalScore < score:
            bestPortalScore = score
            bestPortal = portal
    
    if bestPortalScore is None:
        return Action(0, doNothing)
        
    timeToKill = bestPortal.current_health / (elf.attack_multiplier + float(0.01))
    damageScore = min(1, 8/timeToKill)
    score = bestPortalScore * damageScore
    if elf.invisible:
        score -= 0.5
    
    return Action(score, elfAttackPortal, game, elf, bestPortal)
    
def getElfAttackManaFountain(game, elf):
    if len(game.get_enemy_mana_fountains()) == 0:
        return Action(0, doNothing)
    bestFScore = None
    for f in game.get_enemy_mana_fountains():
        if getIsDangerous(game, f.location):
            continue
        distanceScore = getDistanceScore(elf.distance(f), ATTACK_FOUNTAIN_RANGE, game.mana_fountain_size)
        #portalsNearby = len(getMyPortalsInArea(game, f.location, 1500))
        #portalsNearbyScore = (10 - portalsNearby) / float(10)
        score = distanceScore
        if bestFScore is None or bestFScore < score:
            bestFScore = score
            bestF = f
            
    if bestFScore is None:
        return Action(0, doNothing)      
        
    timeToKill = bestF.current_health / (elf.attack_multiplier + float(0.01))
    damageScore = min(1, 8/timeToKill)
    score = (bestFScore * damageScore) * ATTACK_FOUNTAIN_MULT
    score = min(1.25, score)
    return Action(score, elfAttackManaFountain, game, elf, bestF)

def elfMakePortal(game, elf, loc):
    global portalLocations
    global portalManaFlag
    portalLocations.remove(loc)
    if checkForVicinityPortal(game, loc) > 0:
        for portalLoc in portalLocations:
            if loc.distance(portalLoc) <= game.portal_size * 2 + 5:
                portalLocations.remove(portalLoc)
    if elf.distance(loc) > 0:
        portalManaFlag = True
        elf.move_to(loc)
        print(' ')
        return
    else:
        #if other elf is building, wait for him to finish first.
        for ELF in game.get_my_living_elves():
            if elf.id is not ELF.id:
                if ELF.is_building:
                    return
        print("WE BUILD! HATED BY THE GIANTS WE EMPOWER! HATED BY THE TROLLS WE'VE GIVEN LIFE TO! HOW DO YOU THINK GOD FEELS!?")
        elf.build_portal()
        return

def elfMakeManaFountain(game, elf, loc): #TODO
    global manaFountainLocations
    global fountainManaFlag
    
    manaFountainLocations.remove(loc)
    
    if elf.distance(loc) > 0:
        fountainManaFlag = True
        elf.move_to(loc)
        print("GO TO INFOWARS STORE RIGHT NOW AND HELP FUND THE INFO WAR!")
        return
    else:
        print("I HAVE MORE ENERGY THAN WHEN I WAS 20!")
        elf.build_mana_fountain()
        return


def elfAttackPortal(game, elf, portal):
    if len(game.get_enemy_portals()) == 0:
        return
    if elf.in_attack_range(portal):
        print('PORTAL WILL DIE.')
        elf.attack(portal)
        return
    print('Let me tell all the scum and all the leftists: youre going to lose all of your portals soon.')
    elf.move_to(portal)

def elfAttackManaFountain(game, elf, fountain):
    if len(game.get_enemy_mana_fountains()) == 0:
        return
    if elf.in_attack_range(fountain):
        print("MUDAMUDAMUDAMUDAMUDAMUDAMUDAMUDA!")
        elf.attack(fountain)
        return
    print("I don't like 'em putting chemicals in the mana that turn the freakin' trolls gay!")
    if elf.can_cast_speed_up() and elf.distance(fountain) >= elf.max_speed * game.speed_up_multiplier and getEnemyHealthyIceTrolls(game, elf.location, 500) > 0: #:)
        elf.cast_speed_up()
        return
    elf.move_to(fountain)
    
def elfAttackElf(game, elf, enemyElf):
    if len(game.get_enemy_living_elves()) == 0:
        return
    if elf.in_attack_range(enemyElf):
        elf.attack(enemyElf)
        print("Who is killing these elf victims? Not whites, and not the police, but other elfs.")
        return
    elf.move_to(enemyElf)
    print('Elves will be crushed I can taste your weakness crushing crushing crushing.')
    
def elfAttackCastle(game, elf):
    enemyCastle = game.get_enemy_castle()
    if elf.in_attack_range(enemyCastle):
        print("HAS CRITERIA")
        elf.attack(enemyCastle)
        return
    print("WE ARE COMING STRAIGHT FOR YOU.")
    elf.move_to(enemyCastle)
    
def useInvis(game, elf):
    if elf.can_cast_invisibility():
        elf.cast_invisibility()
        print("it's just a prank bro")
        
def useSpeed(game, elf):
    if elf.can_cast_speed_up():
        elf.cast_speed_up()
        print("DO YOU HAVE ANY IDEA HOW FAST I AM??")
