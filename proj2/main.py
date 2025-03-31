from stripsProblem import Strips, STRIPS_domain, Planning_problem
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
import time

def move(p, l1, l2):
    return 'move_'+p+'_from_'+l1+'_to_'+l2

def at(e): # location of player or monster
    return e+'_at'

def border(l1,l2): # defines if player can move from l1 to l2
    (l1,l2) = (l2,l1) if l1 > l2 else (l1,l2) # to make relation symmetrical
    return l1+'_border_'+l2

def guarded(l1): # defines if monster is guarding location l1
    return l1+'_guarded'

def attack(p, m, l1, l2):
    return 'attack_'+p+'_on_'+m+'_from_'+l1+'_to_'+l2

def has_stone(e): #e is either player or location
    return e+'_has_stone'

def has_wood(e):
    return e+'_has_wood'

def mine_stone(p, l1):
    return 'mine_stone_'+p+'_at_'+l1

def get_wood(p, l1):
    return 'get_wood_'+p+'_at_'+l1

def has_pickaxe(p):
    return p+'_has_pickaxe'

def craft_pickaxe(p): #pickaxe crafted with just wood
    return 'craft_pickaxe_'+p

def has_sword(p):
    return p+'_has_sword'

def craft_sword(p): #sword crafted with stone and wood
    return 'craft_sword_'+p


def create_world(players, monsters, locations):
    #move player from l1 to l2
    stmap = {Strips(move(p, l1, l2), {at(p):l1, border(l1,l2):True, guarded(l2):False}, {at(p):l2})
                for p in players
                for l1 in locations
                for l2 in locations
                if l1 != l2}

    #player p at l1 attacks monster m at l2
    stmap.update({Strips(attack(p, m, l1, l2), {at(p):l1, at(m):l2, border(l1,l2):True, guarded(l2):True, has_sword(p):True}, {at(m):None, guarded(l2):False})
                    for p in players
                    for m in monsters
                    for l1 in locations
                    for l2 in locations
                    if l1 != l2})
    
    #player p mines stone at location l1
    stmap.update({Strips(mine_stone(p, l1), {at(p):l1, has_stone(l1):True, has_stone(p):False, has_pickaxe(p):True}, {has_stone(p):True})
                    for p in players
                    for l1 in locations})

    #player p gets wood at location l1
    stmap.update({Strips(get_wood(p, l1), {at(p):l1, has_wood(l1):True, has_wood(p):False}, {has_wood(p):True})
                    for p in players
                    for l1 in locations})

    #player p crafts pickaxe
    stmap.update({Strips(craft_pickaxe(p), {has_wood(p):True}, {has_pickaxe(p):True, has_wood(p):False})
                    for p in players})
    
    #player p crafts sword
    stmap.update({Strips(craft_sword(p), {has_stone(p):True, has_wood(p):True}, {has_sword(p):True, has_stone(p):False, has_wood(p):False})
                    for p in players})
    
    players_and_monsters = players | monsters
    players_and_locations = players | locations
    locations_and_none = locations | {None}
    boolean = {False, True}

    feature_domain_dict = {at(e):locations_and_none for e in players_and_monsters}
    feature_domain_dict.update({border(l1,l2):boolean for l1 in locations for l2 in locations if l1 < l2})
    feature_domain_dict.update({guarded(l1):boolean for l1 in locations})
    feature_domain_dict.update({has_stone(e):boolean for e in players_and_locations})
    feature_domain_dict.update({has_wood(e):boolean for e in players_and_locations})
    feature_domain_dict.update({has_pickaxe(p):boolean for p in players})
    feature_domain_dict.update({has_sword(p):boolean for p in players})

    return STRIPS_domain(feature_domain_dict, stmap)

def borders_helper(locations, borders): #borders is a set of tuples, returns a dictionary with all locations pairs as keys and True if they are bordering, False otherwise
    border_dict = {}
    for l1 in locations:
        for l2 in locations:
            if l1 < l2:
                border_dict[border(l1, l2)] = (l1, l2) in borders or (l2, l1) in borders
    return border_dict

def locations_stone_helper(locations, locations_stone): #locations_stone is a set of locations, returns a dictionary with all locations as keys and True if they have stone, False otherwise
    stone_dict = {}
    for l in locations:
        stone_dict[has_stone(l)] = l in locations_stone
    return stone_dict

def locations_wood_helper(locations, locations_wood): #locations_wood is a set of locations, returns a dictionary with all locations as keys and True if they have wood, False otherwise
    wood_dict = {}
    for l in locations:
        wood_dict[has_wood(l)] = l in locations_wood
    return wood_dict

def forward_noheuristic(problem): #returns final state
    path = SearcherMPP(Forward_STRIPS(problem)).search()
    final_state = path.end().assignment
    actions = []
    while path.arc is not None:
        actions.append(path.arc.action)
        path = path.initial
    actions.reverse()
    {print(a) for a in actions}
    return final_state

def forward_heuristic(problem, heuristic):
    path = SearcherMPP(Forward_STRIPS(problem,heuristic)).search()
    final_state = path.end().assignment
    actions = []
    while path.arc is not None:
        actions.append(path.arc.action)
        path = path.initial
    actions.reverse()
    {print(a) for a in actions}
    return final_state

def dist(loc1, loc2, state):
    if loc1 == loc2:
        return 0
    
    score = 1
    if not state[border(loc1, loc2)]:
        score += 1
    if state[guarded(loc2)]:
        score += 1
    
    return score

def h1(state, goal):
    score = 0
    for g in goal:
        if g.endswith('_at'):
            score += dist(state[g], goal[g], state)
            continue
    return score

world1 = create_world({'player'}, {'spider'}, {'forest','cave','dungeon'})
problem1 = Planning_problem(world1,
                            {at('player'):'forest', at('spider'):'dungeon',
                             border('forest','cave'):True, border('cave','dungeon'):True, border('dungeon','forest'):False,
                             guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True,
                             has_stone('forest'):False, has_wood('forest'):True, has_stone('cave'):True, has_wood('cave'):False, has_stone('dungeon'):False, has_wood('dungeon'):False,
                             has_stone('player'):False, has_wood('player'):False, has_pickaxe('player'):False, has_sword('player'):False}, #initial state
                             {at('player'):'dungeon'}) #goal

locations = {'forest','cave','dungeon','field','mountain','tower','castle'}
world2 = create_world({'player1', 'player2'}, {'spider', 'zombie', 'skeleton'}, locations)
borders2 = borders_helper(locations, {('forest','cave'),('cave','dungeon'),('forest','field'),('field','mountain'),('mountain','tower'),('cave','mountain'),('castle','field')})
problem2 = Planning_problem(world2,
                            {at('player1'):'forest', at('player2'):'field', at('spider'):'dungeon', at('zombie'):'mountain', at('skeleton'):'tower',
                             **borders2,
                             guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True, guarded('field'):False, guarded('mountain'):True, guarded('tower'):True, guarded('castle'):False,
                             **locations_stone_helper(locations, {'cave','mountain'}), **locations_wood_helper(locations, {'forest'}),
                             has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False,
                             has_stone('player2'):False, has_wood('player2'):False, has_pickaxe('player2'):False, has_sword('player2'):False},
                            {at('player1'):'castle', at('player2'):'castle'})
                             
print("\n***** PROBLEM 2")
print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem2)

problem2b = Planning_problem(world2, state, {at('player1'):'dungeon', at('player2'):'forest'})
state = forward_noheuristic(problem2b)

problem2c = Planning_problem(world2, state, {at('player1'):'tower', at('player2'):'tower'})
forward_noheuristic(problem2c)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")

print("\nHeuristic")

start_time = time.time()
state = forward_heuristic(problem2, h1)

problem2b = Planning_problem(world2, state, {at('player1'):'dungeon', at('player2'):'forest'})
state = forward_heuristic(problem2b, h1)

problem2c = Planning_problem(world2, state, {at('player1'):'tower', at('player2'):'tower'})
forward_heuristic(problem2c, h1)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")