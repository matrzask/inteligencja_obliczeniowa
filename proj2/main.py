from aipython.stripsProblem import Strips, STRIPS_domain, Planning_problem

def move(p, l1, l2):
    return 'move_'+p+'_from_'+l1+'_to_'+l2

def at(c, l1):
    return c+'_at_'+l1

def border(l1,l2):
    return l1+'_border_'+l2

def guarded(l1):
    return l1+'_guarded'

def attack(p, m, l1, l2):
    return 'attack_'+p+'_on_'+m+'_from_'+l1+'_to_'+l2

def open(p, c, l1):
    return 'open_'+p+'_chest_'+c+'_at_'+l1

def opened(c):
    return c+'_opened'

def create_magicworld(players, monsters, locations, chests, elements):
    stmap = {Strips(move(p, l1, l2), {at(p,l1):True, border(l1,l2):True, guarded(l2):False}, {at(p,l1):False, at(p,l2):True})
                for p in players
                for l1 in locations
                for l2 in locations
                if l1 != l2} #move player from l1 to l2
    
    stmap.update({Strips(attack(p, m, l1, l2), {at(p,l1):True, at(m,l2):True, border(l1,l2):True, guarded(l2):True}, {at(m,l2):False, guarded(l2):False})
                    for p in players
                    for m in monsters
                    for l1 in locations
                    for l2 in locations
                    if l1 != l2}) #player p at l1 attacks monster m at l2
    
    stmap.update({Strips(open(p, c, l1), {at(p,l1):True, at(c,l1):True, opened(c):False}, {opened(c):True})
                    for p in players
                    for c in chests
                    for l1 in locations}) #player p opens chest c at l1