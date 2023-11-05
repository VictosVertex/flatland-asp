% This is a basic variant of the naive encoding
% it is specifically for straight line maps, 
% so it only contains rules for straight tracks.

% At each time step the agent has to choose one
% action from all actions possible at the location
% of the agent given its orientation and cell type.
{agent_action(I,A,T):possible_action(C,F,A)} = 1:-  agent_position(I,X,Y,T), 
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
agent_orientation(I,O,T+1) :- agent_action(I,4,T), agent_orientation(I,O,T).


% If forward action is chosen given a straight track
% simply keep the orientation the same and advance time
agent_orientation(I,O,T+1) :- agent_action(I,2,T), 
                            agent_position(I,X,Y,T),
                            agent_orientation(I,O,T),
                            cell(X,Y,1,_).

% If turn left action is chosen, reduce agent orientation by 1 
% (which is the same as adding 3 considering modulo 4).
agent_orientation(I,O,T+1) :- agent_action(I,1,T), agent_orientation(I,O',T),O=(O'+3)\4.

% If turn right action is chosen, increase agent orientation by 1.
agent_orientation(I,O,T+1) :- agent_action(I,3,T), agent_orientation(I,O',T),O=(O'+1)\4.

% If forward action is chosen on simple switch
% and orientations of agent and cell are parallel
% then keep orientation
agent_orientation(I,Oa,T+1) :-  agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,2,Oc),
                                (4+Oa-Oc)\2=0. % Check if parallel

% If forward action is chosen on simple switch
% with different orientation then turn right
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,2,Oc),
                                (4+Oa-Oc)\2=1,  % Check if crossed
                                O=(Oa+1)\4.     % Turn right

% If forward action is chosen on mirrored simple switch
% and orientations of agent and cell are parallel
% then keep orientation
agent_orientation(I,Oa,T+1) :-  agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,10,Oc),
                                (4+Oa-Oc)\2=0.  % Check if parallel

% If forward action is chosen on mirrored simple switch
% with different orientation then turn left
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,10,Oc),
                                (4+Oa-Oc)\2=1,  % Check if crossed
                                O=(Oa+3)\4.     % Turn left

% If forward action is chosen on right turn
% with same orientation, turn right
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,8,Oa),
                                O=(Oa+1)\4.     % Turn right

% If forward action is chosen on right turn
% with different orientation, turn left
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,8,Oc),
                                O=(Oa+3)\4,     % Turn left
                                Oa!=Oc.

% If forward action is chosen on left turn 
% with same orientation, turn left
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,9,Oa),
                                O=(Oa+3)\4.     % Turn left

% If forward action is chosen on left turn 
% with different orientation, turn right
agent_orientation(I,O,T+1) :-   agent_action(I,2,T), 
                                agent_position(I,X,Y,T),
                                agent_orientation(I,Oa,T),
                                cell(X,Y,9,Oc),
                                O=(Oa+1)\4,     % Turn right
                                Oa!=Oc.


% Update positions
%
% If the halting action (4) is chosen
% then don't change any coordinates, simply advance the time step.
agent_position(I,X,Y,T+1) :- agent_action(I,4,T), agent_position(I,X,Y,T).

% If any other action is chosen
% then move one step forward into orientation direction
% and advance time step
agent_position(I,X',Y',T+1) :-  agent_action(I,A,T),
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

% At time step greater than the step limit, the agent can not be at
% any position which is not the position of the target.
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

%:- agent_position(I,X,Y,T), agent_position(I',X,Y,T+1), I!=I',agent_position(I,X',Y',0),
%    (X-X')**2+(Y-Y')**2!=0.

%:-  agent_position(I,X,Y,T), agent_position(I',X+1,Y,T), 
%    agent_orientation(I,O,T), agent_orientation(I',O',T),O=(O'+2)\4, I!=I'.

%:-  agent_position(I,X,Y,T), agent_position(I',X,Y+1,T),
%    agent_orientation(I,O,T), agent_orientation(I',O',T),O=(O'+2)\4, I!=I'.

#show agent_action/3.
#show agent_position/4.
#show agent_state/3.
#show agent_orientation/3.
#show agent_target/3.