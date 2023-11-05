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

% Update orientations
%
% If the halting action (4) is chosen
% keep the current orientation and advance time
% Update orientations according to action taken and current orientation
agent_orientation(I,O,T+1) :- agent_action(I,4,T,OC), agent_orientation(I,O,T).


% If forward action is chosen given a straight track
% simply keep the orientation the same and advance time
agent_orientation(I,O,T+1) :- agent_action(I,2,T,OC), 
                            agent_position(I,X,Y,T),
                            agent_orientation(I,O,T),
                            cell(X,Y,1,_).
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
agent_state(I,0,T) :- agent_position(I,X,Y,T), agent_target(I,X',Y'),X-X'+Y-Y'!=0.
agent_state(I,1,T) :- agent_position(I,X,Y,T), agent_target(I,X',Y'),X-X'+Y-Y'==0.

% At time step greater than 4 the agent can not be at
% any position which is not the position of the target.
:- agent_state(I,0,T),step_limit(L), T>(L-1).

#show agent_action/4.
#show agent_position/4.