%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Graph representation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Create all possible transitions
%
% (X,Y)     - From position
% (O)       - From orientation
% (X',Y')   - To position
% (O')      - To orientation
poss_trans((X,Y),O,(X',Y'),D) :-    cell((X,Y),O,D), 
                                    cell((X',Y'),_,_), 
                                    delta(D, (DX,DY)), 
                                    X'=X+DX, 
                                    Y'=Y+DY.

%%% Count number of choices in each cell and direction,
%%% this is used to differentiate forward-only and actual 
%%% decision cells
%
% (P)   - Position
% (O)   - Orientation
% (C)   - Number of choices
count(P,O,C) :-             C = #count{D:cell(P,O,D)},cell(P,O,_).

%%% Create vertices
% (P)   - Position
vertex(P) :-                schedule(_,P,_,O,_).
vertex(P) :-                schedule(_,_,P,O,_).
vertex(P) :-                cell(P,O,D), count(P,O,C), C>1.
vertex(P) :-                cell(P,0,_), count(P,0,1),
                            cell(P,1,_), count(P,1,1),
                            cell(P,2,_), count(P,2,1),
                            cell(P,3,_), count(P,3,1).
%%% Connect vertices by paths that only require 
%%% moving forward
%
% (O)   - Orientation of the agent at the start of path
% (D)   - Direction in which the agent enters the path
% (P)   - From position
% (P')  - To position
% (D')  - Direction in which the agent exits the path
% (L)   - Length of the path
path(P,O,D,P',D,1) :-       vertex(P),
                            poss_trans(P,O,P',D).

path(P,O,D,P'',D',L+1) :-   path(P,O,D,P',O',L), 
                            poss_trans(P',O',P'',D'),
                            not vertex(P').

%%% Create edges as path between vertices
%
% (P)   - From vertex position
% (O)   - Orientation of the agent at the start of path
% (D)   - Direction in which the agent enters the path
% (P')  - To vertex position
% (D')   - Direction in which the agent exits the path
% (L)   - Length of the edge
edge(P,O,D,P',D',L) :-      vertex(P), vertex(P'), path(P,O,D,P',D',L).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Agent setup, choices and impact of choice
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Starting position
% Since the train in Flatland spawns, it just "arrived"
%
% (ID)  - Identifier of the agent
% (P)   - Arrival position
% (O)   - Arrival Orientation
% (T)   - Arrival Time
arrival(ID,P,O,E) :-        schedule(ID,P,_,O,E).

%%% An agent occupies a position if they have arrived 
%%% but not departed yet
%
% (ID)  - Agent occupying the position
% (P)   - Occupied position
% (D)   - Orientation of the agent
% (T)   - Time step at which the position is occupied
occupied(ID,P,O,T) :-       arrival(ID,P,O,T).

%%% Choose to depart in a direction at some timestep
%%% or keep the position occupied
%
% (ID)  - Identifier of the agent
% (P)   - Departure position
% (D)   - Departure Direction
% (T)   - Departure Time
1{departure(ID,P,D,T):cell(P,O,D);occupied(ID,P,O,T+1)}1:-    vertex(P),
                                                            occupied(ID,P,O,T),
                                                            limit(L),
                                                            T<L/2, 
                                                            not done(ID,T).

%%% Entering an edge blocks it
%%% for at least the minimum travel time
%
% (P)   - From position
% (P')  - To position
% (B)   - Blocked time steps duration
blocked(ID,P,P',B) :-       departure(ID,P,D,T), edge(P,_,D,P',D',L), B=T..T+L-1.


%%% Arrival at a new vertex
arrival(ID,P',D',T+1) :-    departure(ID,P,D,T), edge(P,_,D,P',D',1).

1{arrive(ID,P',D',B);wait(ID,P,P',B)}1 :-     departure(ID,P,D,T),
                                                edge(P,_,_,P',D',L),
                                                L>1,
                                                B>=(T+L-1),
                                                blocked(ID,P,P',B),
                                                limit(L'),
                                                B<L'/2.

blocked(ID,P,P',T+1) :- wait(ID,P,P',T).
arrival(ID,P',D,T+1) :- arrive(ID,P',D,T).

%%% An agent reached their target
%
% (ID)  - Identifier of the agent
% (T)   - Time of arrival at destination
done(ID,T) :-               arrival(ID,P,_,T),schedule(ID,_,P,_,_).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Translation into Flatland actions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%
% Halt
%%%%%%%%%%%%%%%%%%%%%%

%%% If an agent occupied a position but didn't depart from it,
%%% then the agent must have performed a halt
% (ID)  - Identifier of the agent
% (A)   - Action taken (1 = Left Turn, 2 = Forward, 3 = Right Turn, 4 = Halt)
% (T)   - Time the action was taken
agent_action(ID,4,T) :-     occupied(ID,P,_,T), not departure(ID,P,_,T), not done(ID,T).

%%% If an agent decided to wait (only possible in last path-segment)
%%% then the agent must have performed a halt
agent_action(ID,4,T) :-     wait(ID,_,_,T).

%%%%%%%%%%%%%%%%%%%%%%
% Forward
%%%%%%%%%%%%%%%%%%%%%%

%%% If an agent occupied a position and departed from it
%%% having had only one choice, the agent must've moved forward
agent_action(ID,2,T) :-     occupied(ID,P,O,T), departure(ID,P,_,T), count(P,O,1).

%%% If an agent occupied a position and departed in the same direction
%%% the agent must've moved forward
agent_action(ID,2,T) :-     occupied(ID,P,O,T), departure(ID,P,O,T).

%%% If the agent moved onto an edge, then forward is the only
%%% possible action until the other vertex of the edge is reached
agent_action(ID,2,F) :-     departure(ID,P,D,T),
                            edge(P,_,D,P',D',L),
                            F=(T+1)..T+L-2,
                            L>1,
                            not done(ID,F).

%%% If an agent decided to arrive (only possible in last path-segment)
%%% then the action must have been a forward move
agent_action(ID,2,T) :-     arrive(ID,_,_,T).

%%%%%%%%%%%%%%%%%%%%%%
% Turns
%%%%%%%%%%%%%%%%%%%%%%

%%% If an agent occupied a position and departed from it
%%% while having to decide a direction and the direction
%%% change was a counter clockwise rotation, the agent must've
%%% chosen to turn left
agent_action(ID, 1, T) :-   occupied(ID,P,O,T),
                            departure(ID,P,D,T),
                            D=(O+3)\4,
                            count(P,O,C),
                            C>1.
%%% If an agent occupied a position and departed from it
%%% while having to decide a direction and the direction
%%% change was a clockwise rotation, the agent must've
%%% chosen to turn right
agent_action(ID, 3, T) :-   occupied(ID,P,O,T),
                            departure(ID,P,D,T),
                            D=(O+1)\4,
                            count(P,O,C),
                            C>1.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Constraints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Every agent (ID) has to reach their target
:- not done(ID,_), schedule(ID,_,_,_,_).

% An agent can not arrive at an occupied position
:- arrival(ID,P,_,T), occupied(ID',P,_,T), ID!=ID'.

% Two agents can not take opposing paths at the same time
:- blocked(ID,P',P,B), blocked(ID',P,P',B), ID!=ID'.
% Two agents can not take the same path at the same time
:- blocked(ID,P,P',B), blocked(ID',P,P',B), ID!=ID'.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Optimization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#minimize {T:done(_,T)}.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%#show vertex/1.
%#show path/6.
%#show poss_trans/4.
#show edge/6.
#show departure/4.
#show arrival/4.
#show done/2.
#show occupied/4.
#show blocked/4.
#show agent_action/3.
#show arrive/4.
#show wait/4.