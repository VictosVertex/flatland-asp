% This is a basic variant of the naive encoding
% it is specifically for straight line maps, 
% so it only contains rules for straight tracks

% At each time step the agent has to choose one
% action from all actions possible at the location
% of the agent given its orientation and cell type
{agent_action(I,A,T):possible_action(C,F,A)} = 1:- agent(I,X,Y,O,T), cell(X,Y,C,O'),F=(4+O-O')\4, T<10.

% If the halting action (3) is chosen
% then don't change any coordinates or orientation
% simply advance the time step
agent(I,X,Y,O,T+1) :- agent_action(I,3,T), agent(I,X,Y,O,T).

% This part is only applicable to straight lines!
%
% If the forward move action (0) is chosen
% then change coordinates based on orientation,
% keep orientation and advance time step by one
agent(I,X',Y',O,T+1) :- agent_action(I,0,T), agent(I,X,Y,O,T), cell(X,Y,C,_), C=1, X'=X-(O - 2)* (O \ 2), Y'=Y+(O - 1)* ((O+1) \ 2).

% At time step greater than 4 the agent can not be at
% any position which is not the position of the target
:- agent(I,X,Y,O,T), target(I,X',Y'),X-X'+Y-Y'!=0, T>4.

#show agent_action/3.
#show agent/5.