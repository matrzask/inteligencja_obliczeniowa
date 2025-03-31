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


### SIMPLE PROBLEMS ###
print("***** SIMPLE PROBLEMS *****")
print("\n***** PROBLEM 1")
locations1 = {'forest','cave','dungeon'}
world1 = create_world({'player1'}, {'spider'}, locations1)
borders1 = borders_helper(locations1, {('forest','cave'),('cave','dungeon')})
problem1 = Planning_problem(world1,
                            {at('player1'):'forest', at('spider'):'dungeon',
                                **borders1,
                                guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True,
                                **locations_stone_helper(locations1, {'cave'}), **locations_wood_helper(locations1, {'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'dungeon'})
                            

print("\nNo Heuristic")
start_time = time.time()
forward_noheuristic(problem1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
forward_heuristic(problem1, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\n***** PROBLEM 2")
locations2 = {'village', 'river', 'hill', 'forest', 'quarry'}
world2 = create_world({'player1'}, {'wolf'}, locations2)
borders2 = borders_helper(locations2, {('village', 'river'), ('river', 'hill'), ('village', 'forest'), ('forest', 'quarry')})
problem2 = Planning_problem(world2,
                            {at('player1'):'village', at('wolf'):'hill',
                                **borders2,
                                guarded('village'):False, guarded('river'):False, guarded('hill'):True, guarded('forest'):False, guarded('quarry'):False,
                                **locations_stone_helper(locations2, {'hill', 'quarry'}), **locations_wood_helper(locations2, {'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'hill'})

print("\nNo Heuristic")
start_time = time.time()
forward_noheuristic(problem2)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
forward_heuristic(problem2, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")


print("\n***** PROBLEM 3")
locations3 = {'beach', 'jungle', 'cave', 'temple', 'lake', 'village', 'stone quarry', 'forest', 'mountain', 'river'}
world3 = create_world({'player1'}, set(), locations3)
borders3 = borders_helper(locations3, {('beach', 'jungle'), ('jungle', 'forest'), ('forest', 'cave'), ('jungle', 'lake'), ('village', 'stone quarry'), ('village', 'river'), ('lake', 'river'), ('river', 'mountain'), ('mountain', 'temple')})
problem3 = Planning_problem(world3,
                            {at('player1'):'beach',
                                **borders3,
                                guarded('beach'):False, guarded('jungle'):False, guarded('cave'):False, guarded('temple'):False, guarded('lake'):False, guarded('village'):False, guarded('stone quarry'):False, guarded('forest'):False, guarded('mountain'):False, guarded('river'):False,
                                **locations_stone_helper(locations3, {'cave', 'stone quarry'}), **locations_wood_helper(locations3, {'jungle', 'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'temple', has_sword('player1'):True})

print("\nNo Heuristic")
start_time = time.time()
forward_noheuristic(problem3)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
forward_heuristic(problem3, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

### PROBLEMS WITH SUBGOALS ###
print("\n\n***** PROBLEMS WITH SUBGOALS *****")
print("\n***** PROBLEM 1")
locations1 = {'forest','cave','dungeon'}
world1 = create_world({'player1'}, {'spider'}, locations1)
borders1 = borders_helper(locations1, {('forest','cave'),('cave','dungeon')})
problem1 = Planning_problem(world1,
                            {at('player1'):'forest', at('spider'):'dungeon',
                                **borders1,
                                guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True,
                                **locations_stone_helper(locations1, {'cave'}), **locations_wood_helper(locations1, {'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'cave'})
                            

print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem1)

problem1b = Planning_problem(world1, state, {has_stone('player1'):True, has_sword('player1'):True})
state = forward_noheuristic(problem1b)

problem1c = Planning_problem(world1, state, {at('player1'):'dungeon'})
forward_noheuristic(problem1c)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")

start_time = time.time()
state = forward_heuristic(problem1, h1)

problem1b = Planning_problem(world1, state, {has_stone('player1'):True, has_sword('player1'):True})
state = forward_heuristic(problem1b, h1)

problem1c = Planning_problem(world1, state, {at('player1'):'dungeon'})
forward_heuristic(problem1c, h1)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\n***** PROBLEM 2")
locations2 = {'village', 'river', 'hill', 'forest', 'quarry'}
world2 = create_world({'player1'}, {'wolf'}, locations2)
borders2 = borders_helper(locations2, {('village', 'river'), ('river', 'hill'), ('village', 'forest'), ('forest', 'quarry')})
problem2 = Planning_problem(world2,
                            {at('player1'):'village', at('wolf'):'hill',
                                **borders2,
                                guarded('village'):False, guarded('river'):False, guarded('hill'):True, guarded('forest'):False, guarded('quarry'):False,
                                **locations_stone_helper(locations2, {'hill', 'quarry'}), **locations_wood_helper(locations2, {'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'river'})

print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem2)

problem2b = Planning_problem(world2, state, {at('player1'):'village', has_sword('player1'):True})
state = forward_noheuristic(problem2b)

problem2c = Planning_problem(world2, state, {at('player1'):'hill'})
forward_noheuristic(problem2c)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
state = forward_heuristic(problem2, h1)

problem2b = Planning_problem(world2, state, {at('player1'):'village', has_sword('player1'):True})
state = forward_heuristic(problem2b, h1)

problem2c = Planning_problem(world2, state, {at('player1'):'hill'})
forward_heuristic(problem2c, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")


print("\n***** PROBLEM 3")
locations3 = {'beach', 'jungle', 'cave', 'temple', 'lake', 'village', 'stone quarry', 'forest', 'mountain', 'river'}
world3 = create_world({'player1'}, set(), locations3)
borders3 = borders_helper(locations3, {('beach', 'jungle'), ('jungle', 'forest'), ('forest', 'cave'), ('jungle', 'lake'), ('village', 'stone quarry'), ('village', 'river'), ('lake', 'river'), ('river', 'mountain'), ('mountain', 'temple')})
problem3 = Planning_problem(world3,
                            {at('player1'):'beach',
                                **borders3,
                                guarded('beach'):False, guarded('jungle'):False, guarded('cave'):False, guarded('temple'):False, guarded('lake'):False, guarded('village'):False, guarded('stone quarry'):False, guarded('forest'):False, guarded('mountain'):False, guarded('river'):False,
                                **locations_stone_helper(locations3, {'cave', 'stone quarry'}), **locations_wood_helper(locations3, {'jungle', 'forest'}),
                                has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False},
                            {at('player1'):'forest'})

print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem3)

problem3b = Planning_problem(world3, state, {at('player1'):'village'})
state = forward_noheuristic(problem3b)

problem3c = Planning_problem(world3, state, {at('player1'):'temple', has_sword('player1'):True})
forward_noheuristic(problem3c)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
state = forward_heuristic(problem3, h1)

problem3b = Planning_problem(world3, state, {at('player1'):'village'})
state = forward_heuristic(problem3b, h1)

problem3c = Planning_problem(world3, state, {at('player1'):'temple', has_sword('player1'):True})
forward_heuristic(problem3c, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

### BIGGER PROBLEMS ###
print("\n\n***** BIGGER PROBLEMS *****")
print("\n***** PROBLEM 1")
locations1 = {'forest','cave','dungeon','field','mountain','tower','castle'}
world1 = create_world({'player1', 'player2'}, {'spider', 'zombie', 'skeleton'}, locations1)
borders1 = borders_helper(locations1, {('forest','cave'),('cave','dungeon'),('forest','field'),('field','mountain'),('mountain','tower'),('cave','mountain'),('castle','field')})
problem1 = Planning_problem(world1,
                            {at('player1'):'forest', at('player2'):'field', at('spider'):'dungeon', at('zombie'):'mountain', at('skeleton'):'tower',
                             **borders1,
                             guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True, guarded('field'):False, guarded('mountain'):True, guarded('tower'):True, guarded('castle'):False,
                             **locations_stone_helper(locations1, {'cave','mountain'}), **locations_wood_helper(locations1, {'forest'}),
                             has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False,
                             has_stone('player2'):False, has_wood('player2'):False, has_pickaxe('player2'):False, has_sword('player2'):False},
                            {at('player1'):'castle', at('player2'):'castle'})
                             
print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem1)

problem1b = Planning_problem(world1, state, {at('player1'):'dungeon', at('player2'):'forest'})
state = forward_noheuristic(problem1b)

problem1c = Planning_problem(world1, state, {at('player1'):'tower', at('player2'):'tower'})
forward_noheuristic(problem1c)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")

start_time = time.time()
state = forward_heuristic(problem1, h1)

problem1b = Planning_problem(world1, state, {at('player1'):'dungeon', at('player2'):'forest'})
state = forward_heuristic(problem1b, h1)

problem1c = Planning_problem(world1, state, {at('player1'):'tower', at('player2'):'tower'})
forward_heuristic(problem1c, h1)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")


print("\n***** PROBLEM 2")
locations2 = {'village', 'river', 'bridge', 'hill', 'forest', 'deep forest', 'cave', 'castle'}
world2 = create_world({'player1', 'player2'}, {'wolf', 'bear', 'goblin'}, locations2)
borders2 = borders_helper(locations2, {('village', 'river'), ('river', 'bridge'), ('bridge', 'forest'), ('hill', 'forest'), ('forest', 'cave'), ('cave', 'castle'), ('forest', 'deep forest')})
problem2 = Planning_problem(world2,
                            {at('player1'):'village', at('player2'):'river', at('wolf'):'deep forest', at('bear'):'hill', at('goblin'):'castle',
                             **borders2,
                             guarded('village'):False, guarded('river'):False, guarded('bridge'):False, guarded('hill'):True, guarded('forest'):False, guarded('cave'):False, guarded('castle'):True, guarded('deep forest'):True,
                             **locations_stone_helper(locations2, {'hill', 'cave'}), **locations_wood_helper(locations2, {'forest'}),
                             has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False,
                             has_stone('player2'):False, has_wood('player2'):False, has_pickaxe('player2'):False, has_sword('player2'):False},
                            {at('player1'):'castle', at('player2'):'castle'})

print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem2)

problem2b = Planning_problem(world2, state, {at('player1'):'forest', at('player2'):'hill'})
state = forward_noheuristic(problem2b)

problem2c = Planning_problem(world2, state, {at('player1'):'cave', at('player2'):'cave'})
forward_noheuristic(problem2c)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
state = forward_heuristic(problem2, h1)

problem2b = Planning_problem(world2, state, {at('player1'):'forest', at('player2'):'hill'})
state = forward_heuristic(problem2b, h1)

problem2c = Planning_problem(world2, state, {at('player1'):'cave', at('player2'):'cave'})
forward_heuristic(problem2c, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")


print("\n***** PROBLEM 3")
locations3 = {'beach', 'cliff', 'jungle', 'temple', 'lake', 'volcano', 'village', 'plains'}
world3 = create_world({'player1', 'player2'}, {'tiger', 'eagle', 'serpent'}, locations3)
borders3 = borders_helper(locations3, {('beach', 'plains'), ('beach', 'cliff'), ('cliff', 'jungle'), ('jungle', 'temple'), ('temple', 'lake'), ('lake', 'volcano'), ('volcano', 'village')})
problem3 = Planning_problem(world3,
                            {at('player1'):'beach', at('player2'):'cliff', at('tiger'):'jungle', at('eagle'):'temple', at('serpent'):'volcano',
                             **borders3,
                             guarded('beach'):False, guarded('cliff'):False, guarded('jungle'):True, guarded('temple'):True, guarded('lake'):False, guarded('volcano'):True, guarded('village'):False, guarded('plains'):False,
                             **locations_stone_helper(locations3, {'cliff', 'volcano'}), **locations_wood_helper(locations3, {'jungle', 'plains'}),
                             has_stone('player1'):False, has_wood('player1'):False, has_pickaxe('player1'):False, has_sword('player1'):False,
                             has_stone('player2'):False, has_wood('player2'):False, has_pickaxe('player2'):False, has_sword('player2'):False},
                            {at('player1'):'village', at('player2'):'village'})

print("\nNo Heuristic")
start_time = time.time()
state = forward_noheuristic(problem3)

problem3b = Planning_problem(world3, state, {at('player1'):'temple', at('player2'):'lake'})
state = forward_noheuristic(problem3b)

problem3c = Planning_problem(world3, state, {at('player1'):'volcano', at('player2'):'volcano'})
forward_noheuristic(problem3c)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print("\nHeuristic")
start_time = time.time()
state = forward_heuristic(problem3, h1)

problem3b = Planning_problem(world3, state, {at('player1'):'temple', at('player2'):'lake'})
state = forward_heuristic(problem3b, h1)

problem3c = Planning_problem(world3, state, {at('player1'):'volcano', at('player2'):'volcano'})
forward_heuristic(problem3c, h1)
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")