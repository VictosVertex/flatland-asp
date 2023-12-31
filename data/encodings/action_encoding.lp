% This is a basic variant of the naive encoding
% it is specifically for straight line maps, 
% so it only contains rules for straight tracks.

% Initial position of the agent
agent_position(I,X,Y,0):- agent(I,X,Y,_,_).
agent_orientation(I,O,0):- agent(I,_,_,O,_).

% At each time step the agent has to choose one
% action from all actions possible at the location
% of the agent given its orientation and cell type.
{agent_action(I,A,T,OC):possible_action(C,F,A,OC)} = 1:-  agent_position(I,X,Y,T), 
                                                    agent_orientation(I,O,T), 
                                                    cell(X,Y,C,O'),
                                                    not agent_done(I,T),
                                                    step_limit(L),
                                                    F=(4+O-O')\4,
                                                    T<L.

% Update orientations according to action taken and current orientation
agent_orientation(I,O,T+1) :- agent_action(I,A,T,OC), agent_orientation(I,O',T), O=(O'+OC)\4.

% Update positions
%
% If the halting action (4) is chosen
% then don't change any coordinates, simply advance the time step.
agent_position(I,X,Y,T+1) :- agent_action(I,4,T,OC), agent_position(I,X,Y,T).

% If any other action is chosen
% then move one step forward into orientation direction
% and advance time step
agent_position(I,X',Y',T+1) :-  agent_action(I,A,T,OC),
                                agent_orientation(I,O,T+1), 
                                agent_position(I,X,Y,T),
                                A != 4,
                                X'=X-(O - 2)* (O \ 2), 
                                Y'=Y+(O - 1)* ((O+1) \ 2).

% The agent is done as soon as they arrive at their target
agent_done(I,T) :- agent_position(I,X,Y,T), agent_target(I,X,Y).

% Every agent must be done.
:- not agent_done(I,_), agent(I,_,_,_,_). 

% Two different agents can not be at the same position
% at the same time
:-  agent_position(I,X,Y,T), 
    agent_position(I',X,Y,T), 
    I!=I', 
    agent_position(I,X',Y',0),
    (X-X')**2+(Y-Y')**2!=0.

% Two agents can not swap places
:-  agent_position(I,X,Y,T), 
    agent_position(I',X',Y',T), 
    agent_position(I,X',Y',T+1), 
    agent_position(I',X,Y,T+1),
    I != I'.

all_done(T):- T = #sum{T',I:agent_done(I,T')}.

#minimize {T:all_done(T)}.

#show agent_action/4.
#show agent_position/4.
#show agent_orientation/3.
#show agent_target/3.
#show agent_done/2.
#show all_done/1.