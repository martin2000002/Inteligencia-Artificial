from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import heapq

from game.board import BoardArr, parse_board, board_to_lines, place, winner, hamming_to_goal, goal_consistent_moves
from heuristics.hamming import hamming


@dataclass(order=True)
class PQItem:
    priority: int
    counter: int
    board: BoardArr = field(compare=False)
    parent_key: Optional[str] = field(compare=False, default=None)
    move: Optional[Tuple[Tuple[int, int], str]] = field(compare=False, default=None)


def board_key(b: BoardArr) -> str:
    return "".join("".join(row) for row in b)


def best_first_search(start: BoardArr, goal: BoardArr):
    # Priority queue with (hamming, counter) to make ordering stable
    pq: List[PQItem] = []
    counter = 0

    start_h = hamming(start, goal)
    heapq.heappush(pq, PQItem(start_h, counter, start, None, None))

    came_from: Dict[str, Tuple[Optional[str], Optional[Tuple[Tuple[int, int], str]]]] = {}
    came_from[board_key(start)] = (None, None)

    visited: set[str] = set()
    generated = 1

    while pq:
        item = heapq.heappop(pq)
        b = item.board
        k = board_key(b)
        if k in visited:
            continue
        visited.add(k)

        if b == goal:
            # reconstruct path
            path: List[BoardArr] = []
            moves: List[Tuple[Tuple[int, int], str]] = []
            cur_key = k
            while cur_key is not None:
                parent, move = came_from[cur_key]
                # find board by key: not stored, rebuild from parent chain
                # To reconstruct boards, we'll replay moves from start
                cur_key = parent
            # Instead of reconstructing boards here, perform a second pass replaying
            # the moves collected during search in came_from.
            # Let's reconstruct moves sequence first.
            seq: List[Tuple[Tuple[int, int], str]] = []
            cur = k
            while True:
                parent, mv = came_from[cur]
                if parent is None:
                    break
                if mv is not None:
                    seq.append(mv)
                cur = parent
            seq.reverse()
            # Now rebuild boards by applying moves from start
            boards: List[BoardArr] = [start]
            curb = start
            for (pos, token) in seq:
                curb = place(curb, pos, token)
                boards.append(curb)

            return {
                "found": True,
                "generated": generated,
                "visited": len(visited),
                "moves": seq,
                "boards": boards,
            }

        # expand
        for (pos, token) in goal_consistent_moves(b, goal):
            nb = place(b, pos, token)
            nk = board_key(nb)
            if nk in visited:
                continue
            counter += 1
            generated += 1
            prio = hamming(nb, goal)
            heapq.heappush(pq, PQItem(prio, counter, nb, k, (pos, token)))
            if nk not in came_from:
                came_from[nk] = (k, (pos, token))

    return {
        "found": False,
        "generated": generated,
        "visited": len(visited),
        "moves": [],
        "boards": [],
    }
