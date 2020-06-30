#!/usr/bin/env python
# coding: utf-8

# In[139]:


import mlsolver
from mlsolver.kripke import World, KripkeStructure
from itertools import combinations
from random import randrange, choice


# In[140]:


# Configuration
# The way the roles are assigned: players 0..n_fascists are fascist, the other players are liberals
n_players = 5
n_fascists = 2
fascist_wins_needed = 5
liberal_wins_needed = 5


# In[141]:


# Utility functions
def is_fascist(player_number):
    return player_number < n_fascists

def is_liberal(player_number):
    return player_number >= n_fascists

def add_reflexive_edges(worlds, relations):
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.append((world.name, world.name))
            result[agent] = result_agents
    return result

def add_symmetric_edges(relations):
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.append((x, y))
        result[agent] = result_agents
    return result


# In[142]:


# Initialize the worlds
combination_numbers = combinations(range(n_players), n_fascists)
possible_combinations = []
for combo in combination_numbers:
    atoms = ["{}=fascist".format(p) for p in combo] + ["{}=liberal".format(p) for p in range(n_players) if p not in combo]
    possible_combinations.append(atoms)
    
worlds = [World("{}".format(idx), { atom: True for atom in atoms}) for idx, atoms in enumerate(possible_combinations)]
n_worlds = len(worlds)


# In[143]:


# Initialize the relations
relations = {
    # Just the liberal relations
    n: [(str(x), str(y)) for x, y in list(combinations((range(n_worlds)), 2))] for n in range(n_fascists, n_players)
}

# Add the fascist relations
for n in range(n_fascists):
    relations.update({ n: [] })

relations.update(add_reflexive_edges(worlds, relations))
relations.update(add_symmetric_edges(relations))


# In[144]:


# Set up the game state
liberal_wins = 0
fascist_wins = 0
vote_threshold = n_players // 2 + 1
chancellor = -1
president = randrange(0, n_players)

while liberal_wins < 5 and fascist_wins < 5:
    president = (president + 1) % n_players
    if is_liberal(president):
        chancellor = choice(list(range(president)) + list(range(president + 1, n_players)))
    else:
        # Potential issue: this crashes if there is only 1 fascist in the game
        chancellor = choice(list(range(president)) + list(range(president + 1, n_fascists)))
    votes_for = randrange(0, n_players - n_fascists) + (n_fascists if is_fascist(chancellor) else 0)
    if votes_for >= vote_threshold:
        if is_liberal(president) and is_liberal(chancellor):
            liberal_wins += 1
        else:
            fascist_wins += 1

print('The liberals win!' if liberal_wins >= 5 else 'The fascists win!')


# In[ ]:




