% This is a basic variant of the naive encoding
% it is specifically for straight line maps, 
% so it only contains rules for straight tracks.

% At each time step the agent has to choose one
% action from all actions possible at the location
% of the agent given its orientation and cell type.
{agent_action(I,A,T,OC):possible_action(C,F,A,OC)} = 1:-  agent_position(I,X,Y,T), 
                                                    agent_orientation(I,O,T), 
                                                    cell(X,Y,C,O'),
                                                    agent_state(I,0,T),
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

% As long as the agent is not at their target
% the state remains 0 (has not arrived yet), otherwise
% the state changes to 1 (has arrived).
agent_state(I,0,T) :- agent_position(I,X,Y,T), agent_target(I,X',Y'),(X-X')**2+(Y-Y')**2!=0.
agent_state(I,1,T) :- agent_position(I,X,Y,T), agent_target(I,X,Y).

% At time step greater than the step limit 
% (will be replaced by actual latest arrival in the future)
% the agent can not be at any position which is 
% not the position of the target.
:- agent_state(I,0,T),step_limit(L), T>(L-1).

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

#show agent_action/4.
#show agent_position/4.
#show agent_state/3.
#show agent_orientation/3.
#show agent_target/3.