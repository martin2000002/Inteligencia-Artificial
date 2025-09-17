% mc_solver.pl - Misioneros y Caníbales con Backtracking (SWI-Prolog)
% Estado: state(M_left, C_left, Boat) con Boat en {l,r}

:- initialization(run, main).

% Estado inicial y objetivo
start(state(3,3,l)).
goal(state(0,0,r)).

% Lados opuestos
opp(l, r).
opp(r, l).

% Cargas posibles del bote (Misioneros, Caníbales)
boat_load(2,0).
boat_load(1,0).
boat_load(0,2).
boat_load(0,1).
boat_load(1,1).

% Un estado es seguro si ambas orillas respetan la regla
safe_counts(Ml, Cl) :-
    Ml >= 0, Ml =< 3, Cl >= 0, Cl =< 3,
    ( Ml =:= 0 ; Cl =< Ml ),             % izquierda
    Mr is 3 - Ml,
    Cr is 3 - Cl,
    ( Mr =:= 0 ; Cr =< Mr ).             % derecha

safe(state(Ml, Cl, _)) :- safe_counts(Ml, Cl).

% Movimiento: el bote siempre se mueve y lleva una carga válida
move(state(Ml, Cl, l), state(Ml2, Cl2, r), move(M,C)) :-
    boat_load(M, C),
    Ml >= M, Cl >= C,
    Ml2 is Ml - M, Cl2 is Cl - C,
    safe_counts(Ml2, Cl2).

move(state(Ml, Cl, r), state(Ml2, Cl2, l), move(M,C)) :-
    boat_load(M, C),
    Ml2 is Ml + M, Cl2 is Cl + C,
    Ml2 =< 3, Cl2 =< 3,
    safe_counts(Ml2, Cl2).

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

% --- Salida ---

bank_str(0,0, '-') :- !.
bank_str(M, C, Str) :- format(string(Str), '~dM, ~dC', [M, C]).

print_state(state(Ml, Cl, _B)) :-
    Mr is 3 - Ml, Cr is 3 - Cl,
    bank_str(Ml, Cl, LStr),
    bank_str(Mr, Cr, RStr),
    format('IZQ: ~w | DER: ~w~n', [LStr, RStr]).

print_move(state(Ml1, Cl1, B1), state(Ml2, Cl2, _)) :-
    ( B1 == l -> Dir = 'izquierda -> derecha', M is Ml1 - Ml2, C is Cl1 - Cl2
    ;             Dir = 'izquierda <- derecha', M is Ml2 - Ml1, C is Cl2 - Cl1
    ),
    parts_str(M, C, Who),
    ( Who = '' -> format('El bote cruza vacio? (no permitido) (~w)~n', [Dir])
    ; format('El bote lleva ~w (~w)~n', [Who, Dir])
    ).

parts_str(M, C, Str) :-
    ( M =:= 0 -> MStr = '' ; format(string(MStr), '~d misionero(s)', [M]) ),
    ( C =:= 0 -> CStr = '' ; format(string(CStr), '~d canibal(es)', [C]) ),
    join_parts(MStr, CStr, Str).

join_parts('', '', '').
join_parts(A, '', A).
join_parts('', B, B).
join_parts(A, B, Str) :- format(string(Str), '~w y ~w', [A, B]).

print_solution([First|Rest]) :-
    writeln('Solucion (backtracking):'),
    writeln('Paso 0: Estado inicial'),
    print_state(First),
    print_steps(1, [First|Rest]).

print_steps(_, [_]).
print_steps(N, [Prev,Next|Rest]) :-
    format('~nPaso ~d: ', [N]),
    print_move(Prev, Next),
    print_state(Next),
    N1 is N+1,
    print_steps(N1, [Next|Rest]).

run :-
    ( solve(Path) ->
        print_solution(Path),
        length(Path, L), Steps is L-1,
        format('~nTotal de pasos: ~d~n', [Steps])
    ; writeln('No se encontró solución.')
    ).
