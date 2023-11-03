% This is a basic variant of the naive encoding
% it is specifically for straight line maps, 
% so it only contains rules for straight tracks.
%
% All T-values have to be altered in case the map 
% differs from the default map.

% At each time step the agent has to choose one
% action from all actions possible at the location
% of the agent given its orientation and cell type.
{agent_action(I,A,T):possible_action(C,F,A)} = 1:-  agent_position(I,X,Y,T), 
                                                    agent_orientation(I,O,T), 
                                                    cell(X,Y,C,O'),
                                                    F=(4+O-O')\4, 
                                                    T<10.

% Update orientations
%
% If the halting action (3) is chosen
% keep the current orientation and advance time
agent_orientation(I,O,T+1) :- agent_action(I,3,T), agent_orientation(I,O,T).


% If forward action is chosen given a straight track
% simply keep the orientation the same and advance time
agent_orientation(I,O,T+1) :- agent_action(I,0,T), 
                            agent_position(I,X,Y,T),
                            agent_orientation(I,O,T),
                            cell(X,Y,C,_),
                            C=1.
% Update positions
%
% If the halting action (3) is chosen
% then don't change any coordinates, simply advance the time step.
agent_position(I,X,Y,T+1) :- agent_action(I,3,T), agent_position(I,X,Y,T).

% If any other action is chosen
% then move one step forward into orientation direction
% and advance time step
agent_position(I,X',Y',T+1) :-  agent_action(I,A,T),
                                agent_orientation(I,O,T), 
                                agent_position(I,X,Y,T),
                                A != 3,
                                X'=X-(O - 2)* (O \ 2), 
                                Y'=Y+(O - 1)* ((O+1) \ 2).

% At time step greater than 4 the agent can not be at
% any position which is not the position of the target.
:- agent_position(I,X,Y,T), agent_target(I,X',Y'),X-X'+Y-Y'!=0, T>4.

#show agent_action/3.
#show agent_position/4.