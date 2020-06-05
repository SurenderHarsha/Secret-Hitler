# Secret Hitler
Authors:
- Wester Coenraads (s2983928)
- Battu Surender Harsha (s4120310)
- Dirk Jelle Schaap (s2745135)

## Introduction
**Secret Hitler** is a social deduction card game that came to life via a very successful Kickstarter project. Around 5-10 people have to succeed in finding and stopping the Secret Hitler. Players are secretly divided into two teams: the liberals, who have a majority, and the fascists, who are hidden to everyone but each other. If the liberals can learn to trust each other, they have enough votes to control the elections and save the day. However, the fascists will say whatever it takes to get elected, advance their agenda, and win the game. The essence of the game is this: the fascists are in the minority, and will pretend to be liberals. The liberals don’t know who the fascists are, and it is crucial for them to figure this out in order to win. Every round, a policy (either liberal or fascist) is passed by two of the players. The passed policy is public information, and can be used by players to deduce likely fascists. In this way, the players have no direct information of who are fascists, but have indirect information. For example, if players A and B passed a fascist policy, they are likely to be fascists.

In this project we aim to create a multi-agent simulation of the Secret Hitler game. To model the original game in all of its glory is too much to take on, so we will be implementing a simplified variant that is still representative of the original, but has shed some of its complicating details. In this simulation, the players of the game will be represented by the agents. Their tasks are still to figure out who the fascists are if you're a liberal, and to pass fascist policies if you're a fascist. In this way, each agent is tasked to match their internal beliefs the best as they can to the objective truth in the world they're in.
### Game Rules
If you wish to get more familiar with the game in its original form, please refer to the rules [here](https://cdn.vapid.site/sites/a67e0c72-4902-4365-a899-3386df73c2c4/assets/Secret_Hitler_Rules-023bc755617986cb2276a3b6920e43e0.pdf).

## Setup
### Program
Secret Hitler is a complex game, so we construct a somewhat simplified rule set that will allow for easier modelling.
- Executive actions are removed from the rules, as they are complex and varied conditional effects.
- Rather than drawing policy cards, the president and chancellor each secretly choose ’fascist’ or ’liberal’. If both choose liberal, a liberal policy is passed. Otherwise, a fascist policy is passed. This removes the uncertainty of the deck and the work associated with it (modelling how many cards are left in the deck, et cetera).
- Votes on the president and chancellor are done secretly, rather than publicly. This removes complex situations where player votes are used in combination with previously passed policies to determine that someone is a fascist/liberal – which would lead to highly complex models. It is now purely a way to influence the chances of passing a fascist/liberal policy, and not another situation with many different higher-order deductions and decisions.
- Hitler is no longer a part of the game and is simplified to another fascist. This is probably the most significant simplification and removes the very character that the game's name is based on. If time allows, we may keep Hitler in – but only the fact that Hitler does not know who the other fascists are. The instant win condition when electing Hitler will be removed regardless.
- The liberals or fascists win when a certain amount of their respective policies are passed. Our changes may unbalance the game, making too easy for one side to win – so we have to change the number of policies required for one side to accommodate for that. This is done manually and by trial and error.

The multi-agent simulation's progression through a game is round-based. Agents are placed around a table and each agent is assigned to either be liberal or fascist. Roughly a third of the participating agents will be assigned to be fascist. The fascists know who the other fascists are, but the liberals don't know anything about the other agents' political stances. At the start of a game one of the agents is chosen randomly as the president for that round. In the following round, a clockwise motion will determine that the agent sitting next to the previous president will now become the president. The president picks a chancelor it feels comfortable passing policies with. The chancelor cannot be the same agent for two consecutive rounds. Both the president and chancelor secretly vote to either pass a fascist or liberal policy. The result of their votes on the policy is shown in the table below. Only the result of this vote is publicly announced (i.e. the nature of the passed policy). This information is crucial for all players, since everyone is trying to figure out what player belongs to which of the two parties. Moreover, the president and chancelor get the additional information regarding the voting process. They know their own vote, and can in some cases deduct what the other's vote must have been. This round-based multi-agent simulation continues until enough policies have been passed for either the liberal or fascist party, granting that respective party the win.

|                              | Chancelor votes Liberal | Chancelor votes Facist |
|------------------------------|-------------------------|------------------------|
| **President votes Liberal**  |         Liberal         |         Facist         |
| **President votes Facist**   |          Facist         |         Facist         |

### Epistemic Model
We assume and model the players to play optimally to reduce complication i.e liberals always vote for liberal policies etc.
#### Model Variables
Each state 'S' has 'n' atoms where 'n' is the number of players in the game, each atom represents the faction of the players with '1' being a player is a 'Fascist' and '0' being a player is a 'Liberal'. 

The model initially is created with <img src="https://render.githubusercontent.com/render/math?math=2^n"> states. The number of liberals is always greater than number of fascists. When the game begins, the fascists get to know each other and all the fascist relations except reflexive relations are eliminated. Relation set for a player consists of all the possible parties of other players, as the game progresses, these relations are eliminated.

#### Public Announcements
There are a total of 3 public announcements in the game.

1.  President announcing/selecting the chancellor. (If a president is known to be a fascist, then automatically his chancellor is a fascist)
2. Voting results announcement to know if the government(President and chancellor) can select policies or not. Voting is only as yes/no, and only the number of votes for yes/no is shown, but each player's vote is kept anonymous. (Players will remember this)
3.Public announcement of Policy chosen.(As of now there is no strategy where a fascist will choose a liberal policy).






## Results
To do.


## Discussion
To do.
