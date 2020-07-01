# -*- coding: utf-8 -*-



import mlsolver
from mlsolver.kripke import World, KripkeStructure
from itertools import combinations
from random import randrange, choice
import threading
import time

fascist_dist = {
        5:2,
        6:2,
        7:3,
        8:3,
        9:4
        }


class Zero_Order(object):
    def __init__(self,n_players,simulation = True):
        self.n_players = n_players
        self.n_fascists = fascist_dist[self.n_players]
        self.fascist_wins_needed = 5
        self.liberal_wins_needed = 5
        self.president=0
        self.chancellor=0
        self.liberal_wins=0
        self.fascist_wins=0
        self.game_state='Start'
        self.winner = 0
        self.done = False
        self.simulation = simulation
        combination_numbers = combinations(range(self.n_players), self.n_fascists)
        self.possible_combinations = []
        for combo in combination_numbers:
            atoms = ["{}=fascist".format(p) for p in combo] + ["{}=liberal".format(p) for p in range(self.n_players) if p not in combo]
            self.possible_combinations.append(atoms)
            
        self.worlds = [World("{}".format(idx), { atom: True for atom in atoms}) for idx, atoms in enumerate(self.possible_combinations)]
        self.n_worlds = len(self.worlds)
        
        
        self.relations = {
        # Just the liberal relations
            n: [(str(x), str(y)) for x, y in list(combinations((range(self.n_worlds)), 2))] for n in range(self.n_fascists, self.n_players)
        }
        
        # Add the fascist relations
        for n in range(self.n_fascists):
            self.relations.update({ n: [] })
        
        self.relations.update(self.add_reflexive_edges(self.worlds, self.relations))
        self.relations.update(self.add_symmetric_edges(self.relations))
        
        
        t1 = threading.Thread(target=self.run_game)
        t1.start()
            
    def is_fascist(self,player_number):
        return player_number < self.n_fascists

    def is_liberal(self,player_number):
        return player_number >= self.n_fascists
    
    def add_reflexive_edges(self,worlds, relations):
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for world in worlds:
                result_agents.append((world.name, world.name))
                result[agent] = result_agents
        return result
    
    def add_symmetric_edges(self,relations):
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for r in agents_relations:
                x, y = r[1], r[0]
                result_agents.append((x, y))
            result[agent] = result_agents
        return result
    
    def run_game(self):
        if self.simulation:
            time.sleep(4)
        self.liberal_wins = 0
        self.fascist_wins = 0
        vote_threshold = self.n_players // 2 + 1
        self.chancellor = -1
        self.president = randrange(0, self.n_players)
        if self.simulation:
            print("Game Running")
        while self.liberal_wins < self.liberal_wins_needed and self.fascist_wins < self.fascist_wins_needed:
            self.game_state = "Choosing Government"
            if self.simulation:
                time.sleep(1)
            self.president = (self.president + 1) % self.n_players
            if self.is_liberal(self.president):
                self.chancellor = choice(list(range(self.president)) + list(range(self.president + 1, self.n_players)))
            else:
                # Potential issue: this crashes if there is only 1 fascist in the game
                self.chancellor = choice(list(range(self.president)) + list(range(self.president + 1, self.n_fascists)))
            if self.simulation:
                time.sleep(1.5)
                self.game_state ="Voting"
                time.sleep(1)
                
            votes_for = randrange(0, self.n_players - self.n_fascists + 1) + (self.n_fascists if self.is_fascist(self.chancellor) else 0)
            if votes_for >= vote_threshold:
                if self.is_liberal(self.president) and self.is_liberal(self.chancellor):
                    self.liberal_wins += 1
                else:
                    self.fascist_wins += 1
            if self.simulation:
                time.sleep(1.5)
        if self.liberal_wins>=5:
            self.winner = 0
        else:
            self.winner = 1
        if self.simulation:
            print('The liberals win!' if self.liberal_wins >= 5 else 'The fascists win!')
        self.done = True
    def communicate(self):
        #Pass on game state here to UI
        
        
        pass
        
        
class First_Order(object):
    
    def __init__(self,n_players):
        self.n_players = n_players
        self.n_fascists = fascist_dist[self.n_players]
        self.fascist_wins_needed = 5
        self.liberal_wins_needed = 5
        self.president=0
        self.chancellor=0
        self.liberal_wins=0
        self.fascist_wins=0
        self.game_state='Start'
        
        combination_numbers = combinations(range(self.n_players), self.n_fascists)
        self.possible_combinations = []
        for combo in combination_numbers:
            atoms = ["{}=fascist".format(p) for p in combo] + ["{}=liberal".format(p) for p in range(self.n_players) if p not in combo]
            self.possible_combinations.append(atoms)
            
        self.worlds = [World("{}".format(idx), { atom: True for atom in atoms}) for idx, atoms in enumerate(self.possible_combinations)]
        self.n_worlds = len(self.worlds)
        
        
        self.relations = {
        # Just the liberal relations
            n: [(str(x), str(y)) for x, y in list(combinations((range(self.n_worlds)), 2))] for n in range(self.n_fascists, self.n_players)
        }
        
        # Add the fascist relations
        for n in range(self.n_fascists):
            self.relations.update({ n: [] })
        
        self.relations.update(self.add_reflexive_edges(self.worlds, self.relations))
        self.relations.update(self.add_symmetric_edges(self.relations))
        
        
        t1 = threading.Thread(target=self.run_game)
        t1.start()
            
    def is_fascist(self,player_number):
        return player_number < self.n_fascists

    def is_liberal(self,player_number):
        return player_number >= self.n_fascists
    
    def add_reflexive_edges(self,worlds, relations):
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for world in worlds:
                result_agents.append((world.name, world.name))
                result[agent] = result_agents
        return result
    
    def add_symmetric_edges(self,relations):
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for r in agents_relations:
                x, y = r[1], r[0]
                result_agents.append((x, y))
            result[agent] = result_agents
        return result
    
    
    
