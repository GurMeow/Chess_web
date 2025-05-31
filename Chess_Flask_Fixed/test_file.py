import copy
import main
import eval_board

# def make_move(board, from_sq, to_sq):
#     """
#     Mutate board in place:
#       - Move the piece at from_sq to to_sq
#       - Return a snapshot of what was at to_sq and any metadata you need to restore.
#     from_sq/to_sq are (row, col) tuples.
#     """
#     fr, fc = from_sq
#     tr, tc = to_sq
#
#     moved = board[fr][fc]
#     captured = board[tr][tc]
#     prev_times_moved = moved.get("times_moved", None)
#
#     # Do the move:
#     board[tr][tc] = moved
#     board[fr][fc] = {"color": "-1", "piece": "-1"}
#     if prev_times_moved is not None:
#         board[tr][tc]["times_moved"] = prev_times_moved + 1
#
#     # Return snapshot for undo
#     return {
#         "from_sq": (fr, fc), "to_sq": (tr, tc),
#         "moved_piece": moved, "captured_piece": captured,
#         "prev_times_moved": prev_times_moved
#     }
#
#
# def undo_move(board, snapshot):
#     """
#     Restore the board exactly as it was before make_move.
#     """
#     fr, fc = snapshot["from_sq"]
#     tr, tc = snapshot["to_sq"]
#
#     board[fr][fc] = snapshot["moved_piece"]
#     board[tr][tc] = snapshot["captured_piece"]
#
#     if snapshot["prev_times_moved"] is not None:
#         board[fr][fc]["times_moved"] = snapshot["prev_times_moved"]
#
#
# def generate_moves(board, turn):
#     moves = []
#     for i, row in enumerate(board):
#         for j, pos in enumerate(row):
#             if pos["color"] == turn:
#                 for possibility in pos["possible_moves"]:
#                     moves.append((i, j, possibility[0], possibility[1], f"{chr(65+j)}{8-i}->{chr(65+possibility[1])}{8-possibility[0]}"))
#     return moves
#
#
# def minimax_move_undo(depth, board, turn, current_depth, alpha=float('-inf'), beta=float('inf')):
#     main.update_possible_moves(board)
#     current_score = eval_board.evaluate_current_board(board)
#
#     if current_depth == 2 * depth or abs(current_score) > 1000:
#         return [current_score, ""]
#
#     is_maximizing = (turn == "white")
#     best_move = [float('-inf') if is_maximizing else float('inf'), ""]
#
#     moves = generate_moves(board, turn)
#
#     for (fr, fc, tr, tc, notation) in moves:
#         snapshot = make_move(board, (fr, fc), (tr, tc))
#         next_turn = "black" if turn == "white" else "white"
#
#         eval_result = minimax_move_undo(depth, board, next_turn, current_depth + 1, alpha, beta)
#         undo_move(board, snapshot)
#
#         value = eval_result[0]
#
#         if is_maximizing:
#             if value > best_move[0]:
#                 best_move = [value, notation]
#             alpha = max(alpha, value)
#         else:
#             if value < best_move[0]:
#                 best_move = [value, notation]
#             beta = min(beta, value)
#
#         if beta <= alpha:
#             break
#
#     return best_move


def make_move(board, from_sq, to_sq):
    """
    Mutate board in place for a normal move:
      - Move piece from from_sq to to_sq
      - Increment times_moved if present
    Returns snapshot for undo.
    """
    fr, fc = from_sq
    tr, tc = to_sq

    moved = board[fr][fc]
    captured = board[tr][tc]
    prev_times_moved = moved.get("times_moved", None)

    # Execute move
    board[tr][tc] = moved
    board[fr][fc] = {"color": "-1", "piece": "-1"}
    if prev_times_moved is not None:
        board[tr][tc]["times_moved"] = prev_times_moved + 1

    # Snapshot for undo
    return {"from_sq": (fr, fc), "to_sq": (tr, tc),
            "moved_piece": moved, "captured_piece": captured,
            "prev_times_moved": prev_times_moved}


def undo_move(board, snapshot):
    """
    Restore a normal move using snapshot.
    """
    fr, fc = snapshot["from_sq"]
    tr, tc = snapshot["to_sq"]

    board[fr][fc] = snapshot["moved_piece"]
    board[tr][tc] = snapshot["captured_piece"]
    if snapshot["prev_times_moved"] is not None:
        board[fr][fc]["times_moved"] = snapshot["prev_times_moved"]


def generate_moves(board, turn, order_moves):
    """
    Returns a list of move entries:
    - Normal: ("normal", fr, fc, tr, tc, notation)
    - Special (castling/promotion): ("special", new_board, notation)
    """
    moves = []

    for i, row in enumerate(board):
        for j, pos in enumerate(row):
            if pos["color"] != turn:
                continue
            for possibility in pos["possible_moves"]:
                # Castling
                if possibility in (["o-o"], ["o-o-o"]):
                    new_board = copy.deepcopy(board)
                    notation = possibility[0]
                    if turn == "white":
                        row0 = 7
                    else:
                        row0 = 0
                    # king from col4 to col6 or col2
                    if notation == "o-o":
                        # kingside
                        new_board[row0][4]["hasCastled"] = True
                        new_board[row0][6] = new_board[row0][4]
                        new_board[row0][5] = new_board[row0][7]
                        new_board[row0][4] = {"color": "-1", "piece": "-1"}
                        new_board[row0][7] = {"color": "-1", "piece": "-1"}
                    else:
                        # queenside
                        new_board[row0][4]["hasCastled"] = True
                        new_board[row0][2] = new_board[row0][4]
                        new_board[row0][3] = new_board[row0][0]
                        new_board[row0][4] = {"color": "-1", "piece": "-1"}
                        new_board[row0][0] = {"color": "-1", "piece": "-1"}
                    moves.append(("special", new_board, notation))
                    continue

                # Promotion
                try:
                    if len(possibility) >= 3 and possibility[2] == "P":
                        for promo in ["rook","bishop","queen","knight"]:
                            new_board = copy.deepcopy(board)
                            fr, fc = i, j
                            tr, tc = possibility[0], possibility[1]
                            new_board[tr][tc] = new_board[fr][fc]
                            new_board[fr][fc] = {"color": "-1", "piece": "-1"}
                            new_board[tr][tc]["piece"] = promo
                            notation = f"{chr(65+fc)}{8-fr}->{chr(65+tc)}{8-tr}{promo[:2]}"
                            moves.append(("special", new_board, notation))
                        continue
                except Exception:
                    pass

                # Normal move
                fr, fc = i, j
                tr, tc = possibility[0], possibility[1]
                notation = f"{chr(65+fc)}{8-fr}->{chr(65+tc)}{8-tr}"
                moves.append(("normal", fr, fc, tr, tc, notation))
    if order_moves:
        move_order = move_ordering(moves, turn, board)
        # print(moves, end = "\n\n")
        # print(move_order)
        return move_order
    return moves


def minimax_move_undo(depth, board, turn, current_depth=0,
                      alpha=float('-inf'), beta=float('inf'), previous_eval=None):
    """
    Alpha-beta minimax using in-place move/undo for normals,
    deepcopy for specials.
    Returns [best_score, best_notation].
    """
    main.update_possible_moves(board)
    score = eval_board.evaluate_current_board(board)
    continue_flag = False
    if previous_eval:
        pass
    # Terminal or max depth
    if current_depth == depth * 2 + 6:
        return [score,""]
    if current_depth >= 2 * depth and previous_eval and abs(previous_eval - score) > 3:
        continue_flag = True
        # print(previous_eval - score)
        print(f"deepsearched with {current_depth} / {depth *2} overflow!")
    if abs(score) > 1000 or (current_depth >= 2 * depth and not continue_flag):
        return [score, ""]

    is_max = (turn == "white")
    best = [float('-inf') if is_max else float('inf'), ""]
    next_turn = "black" if turn == "white" else "white"
    if current_depth < depth * 2 - 1:
        possible_moves = generate_moves(board, turn, True)
    else:
        possible_moves = generate_moves(board, turn, False)
    if not possible_moves:
        for i in range(8):
            for j in range(8):
                if not main.is_king(board[i][j]):
                    continue
                if not board[i][j]["color"] == turn:
                    continue
                if board[i][j]["checked"]:
                    return [float('-inf') if turn == "black" else float('inf'),""]
                return [0, ""]
    for mv in possible_moves:
        kind = mv[0]
        if kind == "normal":
            _, fr, fc, tr, tc, notation = mv
            snap = make_move(board, (fr, fc), (tr, tc))
            res = minimax_move_undo(depth, board, next_turn,
                                    current_depth+1, alpha, beta, previous_eval=score)
            undo_move(board, snap)
        else:
            _, new_b, notation = mv
            res = minimax_move_undo(depth, new_b, next_turn,
                                    current_depth+1, alpha, beta, previous_eval=score)
        val = res[0]

        if is_max:
            if val > best[0]:
                best = [val, notation]
            alpha = max(alpha, val)
            if val > 1000:
                return best
        else:
            if val < best[0]:
                best = [val, notation]
            beta = min(beta, val)
            if val < -1000:
                return best
        if beta <= alpha:
            break

    return best


def move_ordering(moves, turn, board):
    move_order = []
    if turn == "white":
        next_turn = "black"
    else:
        next_turn = "white"
    for mv in moves:
        kind = mv[0]
        if kind == "normal":
            _, fr, fc, tr, tc, notation = mv
            snap = make_move(board, (fr, fc), (tr, tc))
            res = minimax_move_undo(0, board, next_turn)
            undo_move(board, snap)
        else:
            _, new_b, notation = mv
            res = minimax_move_undo(0, new_b, next_turn)
        move_order.append([mv, res[0]])
    #Sorting
    for i in range(len(move_order)):
        did_swap = False
        for j in range(len(move_order)-i-1):
            if turn == "white":
                if move_order[j][1] < move_order[j+1][1]:
                    #OO me found shiny new way to switch values!
                    move_order[j], move_order[j + 1] = move_order[j + 1], move_order[j]
                    did_swap = True
            else:
                if move_order[j][1] > move_order[j+1][1]:
                    #OO me found shiny new way to switch values!
                    move_order[j], move_order[j + 1] = move_order[j + 1], move_order[j]
                    did_swap = True
        if not did_swap:
            break
    for i ,element in enumerate(move_order):
        element.pop()
        move_order[i] = element[0]
    return move_order


def decode_move(move):
    if move == "o-o" or move == "o-o-o":
        return [move]
    return [8 - int(move[5]), ord(move[4])-65]


def merge_sort_merger(arr, left_pos, middle_pos, right_pos):
    len1 = middle_pos - left_pos + 1
    len2 = right_pos - middle_pos
    arr1 = [0] * len1
    arr2 = [0] * len2
#   Turns out you can create long empty lists like that.
    for i in range(len1):
        arr1[i] = arr[left_pos + i]
    for j in range(len2):
        arr2[j] = arr[middle_pos + j + 1]
    #intilaizing thingies
    i = 0
    j = 0
    k = left_pos

    while i < len1 and j < len2:
        if arr1[i] <= arr2[j]:
            arr[k] = arr1[i]
            i += 1
        else:
            arr[k] = arr2[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = arr1[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = arr2[j]
        j += 1
        k += 1


def merge_sort(arr, left_pos, right_pos):
    if left_pos < right_pos:
        middle_pos = (left_pos + right_pos) // 2
        merge_sort(arr, left_pos, middle_pos)
        merge_sort(arr, middle_pos + 1, right_pos)
        merge_sort_merger(arr, left_pos, middle_pos, right_pos)
