import copy
import main
import eval_board

def make_move(board, from_sq, to_sq, zobrist_hash, zobrist_table):
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

    zobrist_hash = update_zobrist_hash(zobrist_hash, from_sq, to_sq, moved, zobrist_table, captured)

    # Execute move
    board[tr][tc] = moved
    board[fr][fc] = {"color": "-1", "piece": "-1"}
    if prev_times_moved is not None:
        board[tr][tc]["times_moved"] = prev_times_moved + 1

    # Snapshot for undo
    return {"from_sq": (fr, fc), "to_sq": (tr, tc),
            "moved_piece": moved, "captured_piece": captured,
            "prev_times_moved": prev_times_moved, "prev_hash": zobrist_hash}, zobrist_hash


def undo_move(board, snapshot, zobrist_hash, zobrist_table):
    """
    Restore a normal move using snapshot.
    """
    fr, fc = snapshot["from_sq"]
    tr, tc = snapshot["to_sq"]

    board[fr][fc] = snapshot["moved_piece"]
    board[tr][tc] = snapshot["captured_piece"]
    if snapshot["prev_times_moved"] is not None:
        board[fr][fc]["times_moved"] = snapshot["prev_times_moved"]
    zobrist_hash = update_zobrist_hash(zobrist_hash, (fr, fc), (tr, tc),
                                       snapshot["moved_piece"], zobrist_table, snapshot["captured_piece"])
    return zobrist_hash


def generate_moves(board, turn, zobrist_table, z_hash, move_dict, order_moves):
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
                    moves.append(("castling", new_board, notation))
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
                            moves.append(("promotion", new_board, notation))
                        continue
                except Exception:
                    pass
                # Normal move
                fr, fc = i, j
                tr, tc = possibility[0], possibility[1]
                notation = f"{chr(65+fc)}{8-fr}->{chr(65+tc)}{8-tr}"
                moves.append(("normal", fr, fc, tr, tc, notation))
    if order_moves:
        move_order = move_ordering(moves, turn, board, z_hash, zobrist_table, move_dict)
        # print(moves, end = "\n\n")
        # print(move_order)
        return move_order
    return moves


def minimax_move_undo(depth, board, turn, zobrist_table, zobirst_hash, move_dict, current_depth=0,
                      alpha=float('-inf'), beta=float('inf'), previous_eval=None):
    """
    Alpha-beta minimax using in-place move/undo for normals,
    deepcopy for specials.
    Returns [best_score, best_notation].
    """
    main.update_possible_moves(board)
    score = eval_board.evaluate_current_board(board)
    continue_flag = False
    forceful_continue_flag = False
    if move_dict[zobirst_hash] >= 3:
        return [0, ""]

    if eval_board.has_check(board) and current_depth <= 2*depth + 12 and depth >= current_depth * 2:
        forceful_continue_flag = True
        print(f"forceful deep-searched with {current_depth} / {depth *2} overflow!")
    # Terminal or max depth
    if current_depth == depth * 2 + 6 and not forceful_continue_flag:
        return [score,""]
    if current_depth >= 2 * depth and previous_eval and abs(previous_eval - score) >= 3:
        continue_flag = True
        # print(previous_eval - score)
        print(f"deep-searched with {current_depth} / {depth *2} overflow!")
    if abs(score) > 1000 or (current_depth >= 2 * depth and not continue_flag):
        return [score, ""]

    is_max = (turn == "white")
    best = [float('-inf') if is_max else float('inf'), ""]
    next_turn = "black" if turn == "white" else "white"
    if current_depth < depth * 2 - 1:
        possible_moves = generate_moves(board, turn, zobrist_table, zobirst_hash, move_dict, True)
    else:
        possible_moves = generate_moves(board, turn, zobrist_table, zobirst_hash, move_dict, False)
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
            snap, z_hash = make_move(board, (fr, fc), (tr, tc), zobirst_hash, zobrist_table)
            move_dict[z_hash] += 1
            res = minimax_move_undo(depth, board, next_turn, zobrist_table, z_hash, move_dict,
                                    current_depth+1, alpha, beta, previous_eval=score)
            move_dict[z_hash] -= 1
            undo_move(board, snap, zobirst_hash, zobrist_table)
        else:
            _, new_b, notation = mv
            z_hash = main.get_zobrist_hash(new_b, zobrist_table)
            move_dict[z_hash] += 1
            res = minimax_move_undo(depth, new_b, next_turn, zobrist_table, z_hash, move_dict,
                                    current_depth+1, alpha, beta, previous_eval=score)
            move_dict[z_hash] -= 1
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


def move_ordering(moves, turn, board, zobrist_hash, zobrist_table, move_dict):
    move_order = []
    if turn == "white":
        next_turn = "black"
    else:
        next_turn = "white"
    for mv in moves:
        kind = mv[0]
        if kind == "normal":
            _, fr, fc, tr, tc, notation = mv
            snap, z_hash = make_move(board, (fr, fc), (tr, tc), zobrist_hash, zobrist_table)
            res = minimax_move_undo(-20, board, next_turn, zobrist_table, z_hash, move_dict)
            undo_move(board, snap, z_hash, zobrist_table)
        else:
            _, new_b, notation = mv
            z_hash = main.get_zobrist_hash(new_b, zobrist_table)
            res = minimax_move_undo(-20, new_b, next_turn, zobrist_table, z_hash, move_dict)
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


def update_zobrist_hash(zobrist_hash, from_sq, to_sq, moved_piece, zobrist_table, captured_piece=None):
    fr, fc = from_sq
    tr, tc = to_sq
    from_index = fr * 8 + fc
    to_index = tr * 8 + tc

    color = moved_piece["color"]
    piece = moved_piece["piece"]
    # print(zobrist_table[(from_index, piece, color)])
    # Remove piece from original square
    zobrist_hash ^= zobrist_table[(from_index, piece, color)]

    # Remove captured piece if any
    if captured_piece and captured_piece["piece"] != "-1":
        zobrist_hash ^= zobrist_table[(to_index, captured_piece["piece"], captured_piece["color"])]

    # Add moved piece to new square
    zobrist_hash ^= zobrist_table[(to_index, piece, color)]

    return zobrist_hash
