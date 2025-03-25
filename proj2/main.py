from aipython.stripsProblem import Strips, STRIPS_domain, Planning_problem

def move(p, l1, l2):
    return 'move_'+p+'_from_'+l1+'_to_'+l2

def at(e):
    return e+'_at'

def border(l1,l2):
    (l1,l2) = (l2,l1) if l1 > l2 else (l1,l2) # to make relation symmetrical
    return l1+'_border_'+l2

def guarded(l1):
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
    
world1 = create_world({'player'}, {'spider'}, {'forest','cave','dungeon'})
problem1 = Planning_problem(world1,
                            {at('player'):'forest', at('spider'):'dungeon',
                             border('forest','cave'):True, border('cave','dungeon'):True, border('dungeon','forest'):False,
                             guarded('forest'):False, guarded('cave'):False, guarded('dungeon'):True,
                             has_stone('player'):False, has_wood('player'):False, has_pickaxe('player'):False, has_sword('player'):False}, #initial state
                             {at('player'):'dungeon'}) #goal

