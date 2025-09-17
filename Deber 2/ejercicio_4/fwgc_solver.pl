% fwgc_solver.pl - Solver del problema Farmer, Wolf, Goat, Cabbage en SWI-Prolog
% Representación del estado: state(F, W, G, C) con lados l (izquierda) y r (derecha)

:- initialization(run, main).

% Estado inicial y objetivo
start(state(l,l,l,l)).
goal(state(r,r,r,r)).

% Lados opuestos
opp(l, r).
opp(r, l).

% Un estado es seguro si no se deja Lobo con Cabra sin el Granjero,
% ni Cabra con Col sin el Granjero
safe(state(F,W,G,C)) :-
    \+ (W = G, F \= W),
    \+ (G = C, F \= G).

% Movimientos posibles (el granjero siempre cruza):
% - Solo
move(state(F,W,G,C), state(F1,W,G,C), farmer) :-
    opp(F, F1),
    safe(state(F1,W,G,C)).
% - Con el lobo
move(state(F,W,G,C), state(F1,W1,G,C), farmer_wolf) :-
    F = W, opp(F, F1), opp(W, W1),
    safe(state(F1,W1,G,C)).
% - Con la cabra
move(state(F,W,G,C), state(F1,W,G1,C), farmer_goat) :-
    F = G, opp(F, F1), opp(G, G1),
    safe(state(F1,W,G1,C)).
% - Con la col
move(state(F,W,G,C), state(F1,W,G,C1), farmer_cabbage) :-
    F = C, opp(F, F1), opp(C, C1),
    safe(state(F1,W,G,C1)).

% Envoltura sin acción para facilitar el uso con dfs/bfs
move(State, Next) :- move(State, Next, _).

% --- Backtracking (DFS) ---
% Encuentra una ruta cualquiera desde start a goal (no garantiza mínimos pasos)
solve(Path) :-
    start(S), goal(G),
    dfs(S, G, [S], Path).

dfs(State, Goal, _, [State]) :-
    State = Goal, !.
dfs(State, Goal, Visited, [State|Path]) :-
    move(State, Next),
    \+ member(Next, Visited),
    dfs(Next, Goal, [Next|Visited], Path).

% Extrae las cabezas de una lista de listas
heads([], []).
heads([[H|_]|T], [H|HT]) :- heads(T, HT).

% Descripción legible de un estado
print_state(State) :-
    State = state(F,W,G,C),
    left_list(state(F,W,G,C), L),
    right_list(state(F,W,G,C), R),
    write('IZQ: '), show_list(L), write(' | DER: '), show_list(R), nl.

left_list(state(F,W,G,C), L4) :-
    L0 = [],
    (F==l -> L1=['Granjero'|L0]; L1=L0),
    (W==l -> L2=['Lobo'|L1]; L2=L1),
    (G==l -> L3=['Cabra'|L2]; L3=L2),
    (C==l -> L4=['Col'|L3]; L4=L3).

right_list(state(F,W,G,C), R4) :-
    R0 = [],
    (F==r -> R1=['Granjero'|R0]; R1=R0),
    (W==r -> R2=['Lobo'|R1]; R2=R1),
    (G==r -> R3=['Cabra'|R2]; R3=R2),
    (C==r -> R4=['Col'|R3]; R4=R3).

show_list([]) :- write('-').
show_list([X]) :- write(X).
show_list([X|Xs]) :- write(X), write(', '), show_list(Xs).

% Describe el movimiento entre dos estados
print_move(state(F,W1,G1,C1), state(_,W2,G2,C2)) :-
    (F==l -> Dir = 'izquierda -> derecha' ; Dir = 'izquierda <- derecha'),
    ( W1 \= W2 -> Name = 'Lobo'
    ; G1 \= G2 -> Name = 'Cabra'
    ; C1 \= C2 -> Name = 'Col'
    ; Name = none
    ),
    ( Name == none -> format('El Granjero cruza solo (~w)~n', [Dir])
    ; format('El Granjero lleva la ~w (~w)~n', [Name, Dir])
    ).

% Imprime la solución paso a paso
print_solution(Path) :-
    Path = [First|_],
    writeln('Solucion (backtracking):'),
    writeln('Paso 0: Estado inicial'),
    print_state(First),
    print_steps(1, Path).

print_steps(_, [_]).
print_steps(N, [Prev,Next|Rest]) :-
    format('~nPaso ~d: ', [N]),
    print_move(Prev, Next),
    print_state(Next),
    N1 is N+1,
    print_steps(N1, [Next|Rest]).

% Punto de entrada (se ejecuta al cargar con swipl -q -s fwgc_solver.pl)
run :-
    ( solve(Path) ->
        print_solution(Path),
        length(Path, L), Steps is L-1,
        format('~nTotal de pasos: ~d~n', [Steps])
    ; writeln('No se encontró solución.')
    ).
