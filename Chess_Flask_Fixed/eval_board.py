import copy
import time
import main



def evaluate_current_board(board):
    points = 0
    for i, row in enumerate(board):
        for j, pos in enumerate(row):
            points_this_round = 0
            if pos["piece"] == "-1":
                continue
            if pos["piece"] == "pawn":
                points_this_round += eval_pawn(board, pos, pos["color"], i, j)
            if pos["piece"] == "bishop":
                points_this_round += eval_bishop(board, pos, pos["color"], i, j)
            if pos["piece"] == "knight":
                points_this_round += 3
            if pos["piece"] == "rook":
                points_this_round += 5
            if pos["piece"] == "queen":
                points_this_round += 9
            if pos["piece"] == "king":
                points_this_round += eval_king(board, pos, pos["color"], i, j)
            if pos["color"] == "black":
                points_this_round *= -1
            points += points_this_round
    points = round(points, 3)
    return points



def has_check(board):
    for i in range(8):
        for j in range(8):
            if board[i][j]["checks"]:
                return True
    return False


def all_possible_boards(board, turn):
    boards = [[], []]
    for i, row in enumerate(board):
        for j, pos in enumerate(row):
            if pos["color"] == turn:
                for possibility in pos["possible_moves"]:
                    if possibility == ["o-o-o"] or possibility == ["o-o"]:
                        new_board = copy.deepcopy(board)
                        if turn == "white" and (main.contains_possible_move(board[7][4], ["o-o"]) or main.contains_possible_move(board[7][4], ["o-o-o"])):
                            if possibility == ["o-o"]:
                                new_board[7][6] = new_board[7][4]
                                new_board[7][4] = new_board[7][5]
                                new_board[7][5] = new_board[7][7]
                                new_board[7][7] = new_board[7][4]
                                boards[1].append("o-o")
                            if possibility == ["o-o-o"]:
                                new_board[7][2] = new_board[7][4]
                                new_board[7][4] = {"color": "-1", "piece": "-1"}
                                new_board[7][3] = new_board[7][0]
                                new_board[7][0] = {"color": "-1", "piece": "-1"}
                                boards[1].append("o-o-o")
                            new_board[7][6]["times_moved"] += 1
                            new_board[7][5]["times_moved"] += 1
                        if turn == "black" and (main.contains_possible_move(board[0][4], ["o-o"]) or main.contains_possible_move(board[4][0], ["o-o-o"])):
                            if possibility == ["o-o"]:
                                new_board[0][6] = new_board[0][4]
                                new_board[0][4] = new_board[0][5]
                                new_board[0][5] = new_board[0][7]
                                new_board[0][7] = new_board[0][4]
                                boards[1].append("o-o")
                            if possibility == ["o-o-o"]:
                                new_board[7][2] = new_board[7][4]
                                new_board[7][4] = {"color": "-1", "piece": "-1"}
                                new_board[7][3] = new_board[7][0]
                                new_board[7][0] = {"color": "-1", "piece": "-1"}
                                boards[1].append("o-o-o")
                            new_board[0][6]["times_moved"] += 1
                            new_board[0][5]["times_moved"] += 1
                        boards[0].append(new_board)
                        continue
                    try:
                        if possibility[2] == "P":
                            potential_promotions = ["rook","bishop","queen","knight"]
                            for piece_type in potential_promotions:
                                moved_piece = copy.deepcopy(board[i][j])
                                new_board = copy.deepcopy(board)
                                new_board[possibility[0]][possibility[1]] = moved_piece
                                new_board[i][j] = {"color": "-1", "piece": "-1"}
                                new_board[possibility[0]][possibility[1]]["piece"] = piece_type
                                boards[0].append(new_board)
                                boards[1].append(f"{chr(65+j)}{8-i}->{chr(65 + possibility[1])}{8-possibility[0]}{piece_type[:2]}")
                            continue
                    except:
                        pass
                    moved_piece = copy.deepcopy(board[i][j])
                    new_board = copy.deepcopy(board)
                    new_board[possibility[0]][possibility[1]] = moved_piece
                    new_board[i][j] = {"color": "-1", "piece": "-1"}
                    boards[0].append(new_board)
                    boards[1].append(f"{chr(65+j)}{8-i}->{chr(65 + possibility[1])}{8-possibility[0]}")
    return boards


def eval_pawn(board, pos, color, row, column):
    points = 1
    if (column == 3 or column == 4) and (row == 3 or row == 4):
        points += 0.25
    if pos["defenders"] > 1 and pos["attackers"] > 1:
        points += pos["defenders"] * 0.1
    points -= pos["attackers"] * 0.1
    points += 0.5 * (2/(abs(column-4)+1))
    if color == "white":
        points += (6 - row) * 0.05
        if row < 2:
            points += (3 - row) * 0.1
        if row > 0 and board[row-1][column]["color"] == "white" and board[row-1][column]["piece"] == "pawn":
            points -= 0.1
    if color == "black":
        points += (row - 1) * 0.05
        if row > 5:
            points += (row - 4) * 0.1
        if row < 7 and board[row+1][column]["color"] == "white" and board[row+1][column]["piece"] == "pawn":
            points -= 0.1
    board[row][column]["value"] = points
    return points


def eval_bishop(board, pos, color, row, column):
    points = 3
    if pos["attackers"] > 1:
        points += pos["defenders"] * 0.1
    points -= pos["attackers"] * 0.1
    points += len(pos["possible_moves"]) * 0.01
    board[row][column]["value"] = points
    return points


def eval_king(board, pos, color, row, column):
    points = 10000
    if pos["hasCastled"]:
        points += 1
    if pos["times_moved"] != 0 and not pos["hasCastled"]:
        points -= 0.2
    points += 0.05 * pos["defenders"]
    board[row][column]["value"] = points
    return points


def get_all_possible_boards_after_n_moves(depth, board, turn, current_depth):
    boards = all_possible_boards(board, turn)
    if current_depth < depth:
        for i in range(len(boards[0])):
            if turn == "white":
                opp_turn = "black"
            else:
                opp_turn = "white"
            used_board = copy.deepcopy(boards[0][i])
            boards[0][i] = {boards[1][i]: []}
            main.print_board(used_board)
            boards[0][i][f"{boards[1][i]}"] = get_all_possible_boards_after_n_moves(depth, used_board, opp_turn, current_depth + 1)
    return boards



def print_board_after_move(chess_board, command):
    parts = command.split("->")
    piece_column = ord(parts[0][0]) - 65
    piece_row = 7 - int(parts[0][1]) + 1
    target_column = ord(parts[1][0]) - 65
    target_row = 7 - int(parts[1][1]) + 1

    if main.contains_possible_move(chess_board[piece_row][piece_column], [target_row, target_column]):
        chess_board[target_row][target_column] = chess_board[piece_row][piece_column]
        chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
    main.print_board(chess_board)


def get_best_board_after_n_moves(depth, board, turn, current_depth, alpha=float('-inf'), beta=float('inf')):
    main.update_possible_moves(board)
    current_board = evaluate_current_board(board)

    if current_board < -1000 or current_board > 1000 or current_depth == 2 * depth:
        return [current_board, ""]

    is_maximizing = (turn == "white")
    best_move = [float('-inf') if is_maximizing else float('inf'),""]

    boards = all_possible_boards(board, turn)

    for i, new_board in enumerate(boards[0]):
        next_turn = "black" if turn == "white" else "white"
        eval_result = get_best_board_after_n_moves(depth, new_board, next_turn, current_depth + 1, alpha, beta)
        value = eval_result[0]

        if is_maximizing:
            if value > best_move[0]:
                best_move = [value,boards[1][i]]
            alpha = max(alpha, value)
        else:
            if value < best_move[0]:
                best_move = [value, boards[1][i]]
            beta = min(beta, value)

        if beta <= alpha:
            break

    return best_move
