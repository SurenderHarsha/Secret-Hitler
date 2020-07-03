# -*- coding: utf-8 -*-



import mlsolver
from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import *
from itertools import combinations
from random import randrange, choice, sample
import threading
import time
import copy
import numpy as np

fascist_dist = {
        5:2,
        6:2,
        7:3,
        8:3,
        9:4
        }


class Zero_Order(object):
    def __init__(self, n_players, simulation = True,n_f_wins = 5,n_l_wins = 5):
        self.n_players = n_players
        self.n_fascists = fascist_dist[self.n_players]
        self.fascist_wins_needed = n_f_wins
        self.liberal_wins_needed = n_l_wins
        self.president=-1
        self.chancellor=-1
        self.liberal_wins=0
        self.fascist_wins=0
        self.game_state='Start'
        self.winner = 0
        self.done = False
        self.lock = 0
        self.simulation = simulation
        self.votes = { n: False for n in range(n_players) }
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

        self.fascists = sample(list(range(self.n_players)), self.n_fascists)
        
        t1 = threading.Thread(target=self.run_game)
        t1.start()
    
    def is_fascist(self,player_number):
        return player_number in self.fascists

    def is_liberal(self,player_number):
        return not self.is_fascist(player_number)
    
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
            time.sleep(2)
        self.liberal_wins = 0
        self.fascist_wins = 0
        vote_threshold = self.n_players // 2 + 1
        self.chancellor = -1
        self.president = randrange(0, self.n_players)
        if self.simulation:
            print("Game Running")
        
        while self.liberal_wins < self.liberal_wins_needed and self.fascist_wins < self.fascist_wins_needed:
            while self.lock:
                continue
            self.game_state = "Selecting President"
            if self.simulation:
                time.sleep(2.5)
            self.president = (self.president + 1) % self.n_players
            
            self.game_state = "Selecting Chancellor"
            
            if self.simulation:
                time.sleep(2.5)
            if self.is_liberal(self.president):
                self.chancellor = choice(list(range(self.president)) + list(range(self.president + 1, self.n_players)))
            else:
                # Potential issue: this crashes if there is only 1 fascist in the game
                self.chancellor = choice(list(range(self.president)) + list(range(self.president + 1, self.n_fascists)))
            self.votes = { n: False for n in range(self.n_players) } 
            if self.simulation:
                time.sleep(2.5)
                self.game_state = "Voting"
                time.sleep(2.5)
            while self.lock:
                continue
            votes_for = 0
            for player in range(self.n_players):
                while self.lock:
                    continue
                if self.simulation:
                    time.sleep(0.5)
                if player == self.president or player == self.chancellor:
                    self.votes[player] = True
                    votes_for += 1
                elif self.is_liberal(player):
                    vote = choice([True, False])
                    self.votes[player] = vote
                    votes_for += 1 if vote else 0
                else:
                    vote = self.is_fascist(self.president) or self.is_fascist(self.chancellor)
                    self.votes[player] = vote
                    votes_for += 1 if vote else 0
            if self.simulation:
                time.sleep(2)
            while self.lock:
                continue
            #votes_for = randrange(0, self.n_players - self.n_fascists + 1) + (self.n_fascists if self.is_fascist(self.chancellor) else 0)
            if votes_for >= vote_threshold:
                self.game_state = "Government wins by "+str(votes_for-(self.n_players-votes_for))+" votes"
                if self.simulation:
                    time.sleep(3.5)
                if self.is_liberal(self.president) and self.is_liberal(self.chancellor):
                    while self.lock:
                        continue
                    self.liberal_wins += 1
                    self.game_state = "Liberal policy passed"
                else:
                    self.fascist_wins += 1
                    self.game_state = "Fascist Policy passed"
            else:
                if self.simulation:
                    self.game_state = "Vote Failed"
                    time.sleep(1.5)
                    self.game_state = "Choose new Government"
            if self.simulation:
                time.sleep(3.5)
            self.chancellor = -1
        if self.liberal_wins>=5:
            self.game_state = "Liberals Win"
            self.winner = 0
        else:
            self.game_state = "Fascists Win"
            self.winner = 1
        if self.simulation:
            print('The liberals win!' if self.liberal_wins >= 5 else 'The fascists win!')
            time.sleep(2)
        self.done = True
    def communicate(self):
        #Pass on game state here to UI
        
        
        pass
        
        
class First_Order(object):
    def __init__(self,n_players,simulation = True,n_f_wins = 5,n_l_wins = 5):
        self.n_players = n_players
        self.n_fascists = fascist_dist[self.n_players]
        self.fascists = sample(list(range(self.n_players)), self.n_fascists)
        self.fascist_wins_needed = n_f_wins
        self.liberal_wins_needed = n_l_wins
        self.president = 0
        self.chancellor = 0
        self.liberal_wins = 0
        self.fascist_wins = 0
        self.game_state = 'Start'
        self.simulation = simulation
        self.votes = { n: False for n in range(n_players) }
        self.done=False
        self.lock = 0
        t2 = threading.Thread(target = self.preprocess)
        t2.start()
            
    def is_fascist(self,player_number):
        return player_number in self.fascists

    def is_liberal(self,player_number):
        return not self.is_fascist(player_number)
    
    def add_reflexive_edges(self, worlds, relations):
        result = set()
        for world in worlds:
            result.add((world.name, world.name))
        return result
    
    def add_symmetric_edges(self,relations):
        result = set()
        for r in relations:
            x, y = r[1], r[0]
            result.add((x, y))
        return result
    
    def preprocess(self):
        combination_numbers = combinations(range(self.n_players), self.n_fascists)
        self.possible_combinations = []
        for combo in combination_numbers:
            atoms = ["{}=fascist".format(p) for p in combo] + ["{}=liberal".format(p) for p in range(self.n_players) if p not in combo]
            self.possible_combinations.append(atoms)
            
        self.worlds = [World("{}".format(idx), { atom: True for atom in atoms}) for idx, atoms in enumerate(self.possible_combinations)]
        self.n_worlds = len(self.worlds)
        
        self.models = []
        for player in range(self.n_players):
            worlds = copy.deepcopy(self.worlds)
            relations = {
                # Just the liberal relations
                (str(x), str(y)) for x, y in list(combinations((range(self.n_worlds)), 2))
            } if self.is_liberal(player) else set()

            relations.update(self.add_reflexive_edges(worlds, relations))
            relations.update(self.add_symmetric_edges(relations))
            model = KripkeStructure(worlds, relations)
            atom = Atom('{}=fascist'.format(player)) if self.is_fascist(player) else Atom('{}=liberal'.format(player))
            model = model.solve(atom)
            self.models.append(model)
        for player in range(self.n_players):
            if self.is_fascist(player):
                for p in range(self.n_players):
                    if self.is_liberal(p):
                        a = Atom('{}=liberal'.format(p))
                        self.models[player] = self.models[player].solve(a)
        
        t1 = threading.Thread(target=self.run_game)
        t1.start()
    def run_game(self):
        self.liberal_wins = 0
        self.fascist_wins = 0
        self.game_state = "Starting.."
        if self.simulation:
                time.sleep(2.5)
        vote_threshold = self.n_players // 2 + 1
        self.chancellor = -1
        self.president = randrange(0, self.n_players)

        while self.liberal_wins < self.liberal_wins_needed and self.fascist_wins < self.fascist_wins_needed:
            
            self.game_state = "Selecting President"
            if self.simulation:
                time.sleep(2.5)
            while self.lock:
                continue
            self.president = (self.president + 1) % self.n_players
            if self.simulation:
                time.sleep(2.5)
            self.game_state = "Selecting Chancellor"
            if self.simulation:
                time.sleep(2.5)
            # Choosing a chancellor
            while self.lock:
                continue
            if self.is_fascist(self.president):
                self.chancellor = choice(list(range(self.president)) + list(range(self.president + 1, self.n_players)))
            else:
                model = self.models[self.president]
                # Choose the 'most liberal' candidate
                counts = []
                for player in range(self.n_players):
                    while self.lock:
                        continue
                    counts.append(sum(map(lambda w: 1 if w.assignment.get('{}=liberal'.format(player), False) else 0, model.worlds)))
                counts[self.president] = -1
                self.chancellor = np.argmax(counts)
            if self.simulation:
                time.sleep(2.5)
            while self.lock:
                continue
            self.votes = { n: False for n in range(self.n_players) }
            self.game_state = "Voting"
            if self.simulation:
                time.sleep(2.5)
            # Voting on the government
            votes_for = 0
            for player in range(self.n_players):
                if self.simulation:
                    time.sleep(0.5)
                while self.lock:
                    continue
                
                if player == self.president or (player == self.chancellor and self.is_fascist(player)):
                    self.votes[player] = True
                    votes_for += 1
                elif self.is_liberal(player):
                    f = Box(Or(Atom('{}=fascist'.format(self.president)), Atom('{}=fascist'.format(self.chancellor))))
                    a_fascist = self.fascists[0]
                    real_world = self.models[a_fascist].worlds[0].name
                    
                    one_is_fascist = f.semantic(self.models[player],real_world)
                    #one_is_fascist = copy.deepcopy(self.models[player]).solve(f) == self.models[player]
                    vote = not one_is_fascist
                    self.votes[player] = vote
                    votes_for += 1 if vote else 0
                else:
                    vote = self.is_fascist(self.president) or self.is_fascist(self.chancellor)
                    self.votes[player] = vote
                    votes_for += 1 if vote else 0
                    
            if self.simulation:
                time.sleep(2.5)
            while self.lock:
                    continue
            # The government chooses a policy
            # and the kripke models are updated
            # based on the policy chosen
            if votes_for >= vote_threshold:
                self.game_state = "Government wins!"
                if self.simulation:
                    time.sleep(2.5)
                while self.lock:
                    continue
                if self.is_liberal(self.president) and self.is_liberal(self.chancellor):
                    self.game_state = "Liberal Policy Passed"
                    if self.simulation:
                        time.sleep(2.5)
                    while self.lock:
                        continue
                    self.liberal_wins += 1
                    updater = Box(And(Atom('{}=liberal'.format(self.president)), Atom('{}=liberal'.format(self.chancellor))))
                    for n in range(self.n_players):
                        self.models[n] = self.models[n].solve(updater)
                else:
                    self.game_state = "Fascist Policy Passed"
                    if self.simulation:
                        time.sleep(2.5)
                    while self.lock:
                        continue
                    self.fascist_wins += 1
                    updater = Box(Or(Atom('{}=fascist'.format(self.president)), Atom('{}=fascist'.format(self.chancellor))))
                    for n in range(self.n_players):
                        self.models[n] = self.models[n].solve(updater)
                    
                    if self.is_liberal(self.president):
                        self.models[self.president] = self.models[self.president].solve(Atom('{}=fascist'.format(self.chancellor)))
                    if self.is_liberal(self.chancellor):
                        self.models[self.chancellor] = self.models[self.chancellor].solve(Atom('{}=fascist'.format(self.president)))
                    
            if self.simulation:
                time.sleep(2.5)
            while self.lock:
                    continue
        if self.liberal_wins >= 5:
            self.game_state = "Liberals Win"
            self.winner = 0
        else:
            self.game_state = "Fascists Win"
            self.winner = 1
        #print('The liberals win!' if self.liberal_wins >= 5 else 'The fascists win!')
        self.done = True
        
        
if __name__ == '__main__':
    print('NOTE: this runs the model without the UI')
    game = First_Order(5)
    #game.run_game()
    print('Finished running...')