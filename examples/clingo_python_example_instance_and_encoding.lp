% This is a basic example of Answer Set Programming

% Definitions:
%   These statements are facts about the instance, they are always given.
%
% Define a 2X2 grid of cells with coordinates X in [1,2] and Y in [1,2]
cell(1..2,1..2).

% Generators:
%   With the help of generators the facts can be dynamically expanded
%
% For each cell generate exactly one number consistion of the position X,Y (same as the cell)
% and a value Z in [1,9]
{number(X,Y,Z):Z=1..9} = 1  :- cell(X,Y).

% Integrity Constraints:
%   Rules that must not be satisfied
%
% The body shows that two numbers exist with differing Y coordinate
% so they are in the same row of the 2D-grid.
% It also states that the sum of their respective Z values can not be 5.
%
% Since this rule - must not - be satisfied, it basically states:
%   There can not be two numbers in the same row whose Z values do not sum up to 5.
%
% In other words the Z values of each row - must - sum to 5.
:- number(1,1,Z), number(1,2,Z'), Z+Z'!=5.
:- number(2,1,Z), number(2,2,Z'), Z+Z'!=5.

% Similarly in the first column of the grid the sum of Z values must be 6
% and in the second row the sum must be 4
:- number(1,1,Z), number(2,1,Z'), Z+Z'!=6.
:- number(1,2,Z), number(2,2,Z'), Z+Z'!=4.

% Only show the number predicate
#show number/3.

% If this example is run with clingo_python_example.py
% one possible solution would look like:
% number(2,2,1) number(1,1,2) number(1,2,3) number(2,1,4)
%
% Displaying the generated solution in grid form
% number(1,1,2) number(1,2,3)
% number(2,1,4) number(2,2,1)
%
% Z values of rows:
%   2 + 3 = 5
%   4 + 1 = 5
%
% Z values of columns:
%   2 + 4 = 6
%   3 + 1 = 4
%
% Thus all constraints are fulfilled and the solution candidate, 
% the answer set, satisfies our encoding