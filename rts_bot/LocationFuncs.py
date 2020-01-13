#remove this when running bot. made to prevent copying.

from elf_kingdom import *

DANGER_THRESHOLD = 0.3
DANGER_RADIUS = 1000 #CHANGE THIS IN MAIN FILE TOO.


def getClosestIceTroll(game, mapObject):
    if len(game.get_enemy_ice_trolls()) == 0:
        returnportal

    closestEnemyTroll = game.get_enemy_ice_trolls()[0] #gets the closest enemy and prints range from it.
    for enemy in game.get_enemy_ice_trolls():
        if mapObject.distance(enemy) < mapObject.distance(closestEnemyTroll):
            closestEnemyTroll = enemy
    return closestEnemyTroll

def getClosestEnemyElf(game,mapObject):
    if len(game.get_enemy_living_elves()) == 0:
        return

    closestEnemyElf = game.get_enemy_living_elves()[0] #gets the closest enemy and prints range from it.
    for enemy in game.get_enemy_living_elves():
        if mapObject.distance(enemy) < mapObject.distance(closestEnemyElf):
            closestEnemyElf = enemy
    return closestEnemyElf
        
def getClosestEnemyPortal(game, mapObject):
    if len(game.get_enemy_portals()) > 0:
        closestEnemyPortal = game.get_enemy_portals()[0] #gets the closest enemy and prints range from it.
        for portal in game.get_enemy_portals():
            if mapObject.distance(portal) < mapObject.distance(closestEnemyPortal):
                closestEnemyPortal = portal
        return closestEnemyPortal

def getClosestEnemyFountain(game, mapObject):
    if len(game.get_enemy_mana_fountains()) > 0:
        closestEnemyPortal = game.get_enemy_mana_fountains()[0] #gets the closest enemy and prints range from it.
        for portal in game.get_enemy_mana_fountains():
            if mapObject.distance(portal) < mapObject.distance(closestEnemyPortal):
                closestEnemyPortal = portal
        return closestEnemyPortal
        
def getCenterPortalLocation(game):
    center = Location(1900,3250) # get center with both castle locations
    if getSideOfMap(game) == 'left': #if we are on left side possible to check the castle locations and check ==.
        return center.add(Location(row=100, col=-450))
    else:
        return center.add(Location(row=-100, col=450))


def getMyClosestPortals(game,mapObject, num): #closest portal to enemy base
    if not len(game.get_my_portals()) > num-1:
        print("There are no enemy portals for func getAttackPortal.")
        return
    portals = game.get_my_portals()
    closestPortals = []
    for i in range(num):
        closest = portals[0]
        k = 0
        for j in range(len(portals)):
            if portals[j].distance(mapObject) < closest.distance(mapObject):
                closest = portals[j]
                k = j
        del portals[k]
        closestPortals.append(closest)
    return closestPortals
    
def getMyClosestElf(game, mapObject):
    if game.get_my_living_elves == 1:
        return game.get_my_living_elves()[0]
    if game.get_my_living_elves == 2:
        if game.get_my_living_elves()[0].distance(mapObject) < game.get_my_living_elves[1].distance(mapObject):
            return game.get_my_living_elves()[0]
        else:
            return game.get_my_living_elves()[1]
    else:
        return None
    
            
def getSideOfMap(game):
    l = Location(0,0)
    if l.distance(game.get_my_castle()) < l.distance(game.get_enemy_castle()): #our castle is at the bottom-left corner
        return 'left'
    return 'right'
    
def getPortalLocations(game): #add pair portal, maybe with checkForVicinityPortal
    side = getSideOfMap(game)
    locArr = []
    
    #mid portals
    enemyCastle = game.get_enemy_castle().location
    myCastle = game.get_my_castle().location
    
    if side == 'left':
        rightN = enemyCastle.subtract(myCastle)
        defenseLoc = myCastle + rightN.multiply(float(1)/3)
        offenseLoc = myCastle + rightN.multiply(float(2)/3)
    
    if side == 'right':
        rightN = myCastle.subtract(enemyCastle)
        defenseLoc = enemyCastle + rightN.multiply(float(2)/3)
        offenseLoc = enemyCastle + rightN.multiply(float(1)/3)
    
    if checkForVicinityPortal(game, defenseLoc) < 2:
        counter = checkForVicinityPortal(game,defenseLoc) #need to make sure 2 locs wont be added incase theres one built
        if game.can_build_portal_at(defenseLoc): #defense portal CHECK PORTALS IN AREA BEFORE EACH CHUNK OF SPECIFIC PORTAL CODE.
            locArr.append(defenseLoc)
            counter += 1
        elif checkForPortal(game, defenseLoc) == 'enemy':
            if len(getVicinityPortalLocations(game, defenseLoc)) is not 0:
                locArr.append(getVicinityPortalLocations(game, defenseLoc)[0])
                counter += 1
        if counter < 2:
            if checkForPortal(game, defenseLoc) == 'enemy':
                if len(getVicinityPortalLocations(game, defenseLoc)) > 1:
                    locArr.append(getVicinityPortalLocations(game, defenseLoc)[1])
            else:
                if len(getVicinityPortalLocations(game, defenseLoc)) > 0:
                    locArr.append(getVicinityPortalLocations(game, defenseLoc)[0])
                
    if game.can_build_portal_at(offenseLoc): #offense portal add counter here too.
        locArr.append(offenseLoc)
    elif checkForPortal(game, offenseLoc) == 'enemy':
        if len(getVicinityPortalLocations(game, offenseLoc)) is not 0:
            locArr.append(getVicinityPortalLocations(game, offenseLoc)[0])
    if checkForVicinityPortal(game, offenseLoc) < 2: #if there is no friendly portal in vicinity make one.
        if checkForPortal(game, offenseLoc) == 'enemy':
            if len(getVicinityPortalLocations(game, offenseLoc)) > 1:
                locArr.append(getVicinityPortalLocations(game, offenseLoc)[1])
        else:
            if len(getVicinityPortalLocations(game, offenseLoc)) > 0:
                locArr.append(getVicinityPortalLocations(game, offenseLoc)[0])


    #attackPortals
    attackLocs = [enemyCastle.add(Location(game.portal_size + game.castle_size + 2, 0)),
                    enemyCastle.add(Location(0, game.portal_size + game.castle_size + 2)),
                    enemyCastle.add(Location(game.portal_size + game.castle_size + 2, game.portal_size + game.castle_size + 2)),
                    enemyCastle.add(Location(0 - game.portal_size - game.castle_size - 2, 0)),
                    enemyCastle.add(Location(0, 0 - game.portal_size - game.castle_size - 2)),
                    enemyCastle.add(Location(0 - game.portal_size - game.castle_size - 2, 0 - game.portal_size - game.castle_size - 2)),
                    enemyCastle.add(Location(game.portal_size + game.castle_size + 2, 0 - game.portal_size - game.castle_size - 2)),
                    enemyCastle.add(Location(0 - game.portal_size - game.castle_size - 2, game.portal_size + game.castle_size + 2))]
    
    for tempLoc in attackLocs:
        if game.can_build_portal_at(tempLoc):
            locArr.append(tempLoc)
            break
            

    if len(locArr) == 0:
            return []
    return locArr
    
def getManaFountainLocations(game): #might make code too slow
    locArr = []
    myCastle = game.get_my_castle().location
    for i in range(game.castle_size + game.mana_fountain_size + 1, 2000, 2 * game.mana_fountain_size + 1):
        locs = [myCastle.add(Location(i, 0)),
                    myCastle.add(Location(0, i)),
                    myCastle.add(Location(i/2, i/2)),
                    myCastle.add(Location(0 - i, 0)),
                    myCastle.add(Location(0, 0 - i)),
                    myCastle.add(Location(0 - i/2, 0 - i/2)),
                    myCastle.add(Location(i/2, 0 - i/2)),
                    myCastle.add(Location(0 - i/2, i/2))]
        
        for loc in locs:
            if game.can_build_mana_fountain_at(loc):
                locArr.append(loc)
    return locArr
        
def getVicinityPortalLocations(game, loc):
    y = loc.row 
    x = loc.col
    locArr = []
    
    if getSideOfMap(game) == 'left':
        if game.can_build_portal_at(Location(y, x - 2 * game.portal_size - 5)): #case left
            locArr.append(Location(y, x - 2 * game.portal_size - 5))
    elif getSideOfMap(game) == 'right':
        if game.can_build_portal_at(Location(y, x + 2 * game.portal_size + 5)): #case right
            locArr.append(Location(y, x + 2 * game.portal_size + 5))
        
    towardsLoc = loc.towards(game.get_my_castle().location, 2 * game.portal_size + 5)
    if game.can_build_portal_at(towardsLoc): #case towards my castle
        locArr.append(towardsLoc)
    if game.can_build_portal_at(Location(y + 2 * game.portal_size + 5, x)): #case down
        locArr.append(Location( y + 2 * game.portal_size + 5, x))
    if game.can_build_portal_at(Location(y - 2 * game.portal_size - 5, x)): #case up
        locArr.append(Location(y - 2 * game.portal_size - 5, x))
    return locArr


   
def checkForPortal(game, loc): #p.location doesnt have to be loc for a portal to exist there, since portals have a radius.
    if len(game.get_my_portals()) == 0 and len(game.get_enemy_portals()) == 0:
        return 'none'

    if not len(game.get_my_portals()) == 0:
        myPortals = game.get_my_portals()
        for p in myPortals:
            if loc.distance(p.location) <= game.portal_size:
                return 'friend'

    if not len(game.get_enemy_portals()) == 0:
        enemyPortals = game.get_enemy_portals()
        for p in enemyPortals:
            #if p.location == loc:
            if loc.distance(p.location) <= game.portal_size:
                return 'enemy'
    return 'none'

def checkForVicinityPortal(game, loc):
    if len(game.get_my_portals()) == 0:
        return 0
    
    counter = 0
    for portal in game.get_my_portals():
        if loc.distance(portal) <= 2 * game.portal_size + 5:
            counter += 1
            
    return counter

def getEnemyPortalsInArea(game, loc, radius):
    #checks for enemy portals in radius of location.
    portals = game.get_enemy_portals()
    portalsInRange = []
    for portal in myPortals:
        if portal.distance(loc) <= radius:
            portalsInRange.append(portal)
    
    return portalsInRange

def getMyPortalsInArea(game, loc, radius):
    #checks for my portals in radius of location.
    portals = game.get_my_portals()
    portalsInRange = []
    for portal in portals:
        if portal.distance(loc) <= radius:
            portalsInRange.append(portal)
    
    return portalsInRange

def getIceTrollEffectiveHP(game, troll, loc):
    time = (troll.distance(game.get_my_castle()) - game.ice_troll_attack_range) / game.ice_troll_max_speed
    effectiveHP = troll.current_health - time * game.ice_troll_suffocation_per_turn
    return effectiveHP

def getIsDangerous(game, loc):
    #enemy elfs, my elfs, enemy ice trolls, my ice torlls, and their range from the location. get
    #getDistanceScore(dist, 1000)
    danger = 0
    for enemyElf in game.get_enemy_living_elves():
        distanceScore = getDistanceScore(loc.distance(enemyElf), DANGER_RADIUS, game.elf_attack_range)
        distanceScore = max(distanceScore, 0)
        danger += distanceScore * float(0.25) * game.elf_attack_multiplier
    '''
    for myElf in game.get_my_living_elves():
        distanceScore = getDistanceScore(loc.distance(myElf), DANGER_RADIUS)
        distanceScore = max(distanceScore, 0)
        danger -= distanceScore * float(0.25) * game.elf_attack_multiplier
    ''' 
    for enemyIceTroll in game.get_enemy_ice_trolls():
        distanceScore = getDistanceScore(loc.distance(enemyIceTroll), DANGER_RADIUS, game.ice_troll_attack_range)
        distanceScore = max(distanceScore, 0)
        danger += distanceScore * float(0.25) * game.ice_troll_attack_multiplier
    
    for myIceTroll in game.get_my_ice_trolls():
        distanceScore = getDistanceScore(loc.distance(myIceTroll), DANGER_RADIUS)
        distanceScore = max(distanceScore, 0)
        danger -= distanceScore * float(0.25) * game.ice_troll_attack_multiplier
        
    
    
    danger = max(danger, 0)
    #print("Location %s Danger: %s" %(loc, danger))
    return danger >= DANGER_THRESHOLD
    
def getDistanceScore(currDistance, maxDistance, minDistance = 0):
    return 1 - max(0 , currDistance - minDistance) / float(maxDistance)