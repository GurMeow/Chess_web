import main


def move_rook(row, column, board):
    moves = []
    for pin in board[row][column]["pinned_to"]:
        if pin[2] == "absolute":
            if pin[1] == [1, 0] or pin[1] == [-1, 0]:
                moves = possible_moves_in_direction(row, column, [-1, 0], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [1, 0], board[row][column], moves, board)
            if pin[1] == [0, 1] or pin[1] == [0, -1]:
                moves = possible_moves_in_direction(row, column, [0, 1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [0, -1], board[row][column], moves, board)
            return moves
    moves = possible_moves_in_direction(row, column, [1, 0], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [0, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, 0], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [0, -1], board[row][column], moves, board)
    return moves


def move_bishop(row, column, board):
    moves = []
    for pin in board[row][column]["pinned_to"]:
        if pin[2] == "absolute":
            if pin[1] == [1, 1] or pin[1] == [-1, -1]:
                moves = possible_moves_in_direction(row, column, [-1, -1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [1, 1], board[row][column], moves, board)
            if pin[1] == [1, -1] or pin[1] == [-1, 1]:
                moves = possible_moves_in_direction(row, column, [1, -1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [-1, 1], board[row][column], moves, board)
            return moves
    moves = possible_moves_in_direction(row, column, [1, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [1, -1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, -1], board[row][column], moves, board)
    return moves


def move_queen(row, column, board):
    moves = []
    for pin in board[row][column]["pinned_to"]:
        if pin[2] == "absolute":
            if pin[1] == [1, 1] or pin[1] == [-1, -1]:
                moves = possible_moves_in_direction(row, column, [-1, -1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [1, 1], board[row][column], moves, board)
            if pin[1] == [1, -1] or pin[1] == [-1, 1]:
                moves = possible_moves_in_direction(row, column, [1, -1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [-1, 1], board[row][column], moves, board)
            if pin[1] == [1, 0] or pin[1] == [-1, 0]:
                moves = possible_moves_in_direction(row, column, [-1, 0], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [1, 0], board[row][column], moves, board)
            if pin[1] == [0, 1] or pin[1] == [0, -1]:
                moves = possible_moves_in_direction(row, column, [0, 1], board[row][column], moves, board)
                moves = possible_moves_in_direction(row, column, [0, -1], board[row][column], moves, board)
            return moves
    moves = possible_moves_in_direction(row, column, [1, 0], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [0, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [1, -1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, 0], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [0, -1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [1, 1], board[row][column], moves, board)
    moves = possible_moves_in_direction(row, column, [-1, -1], board[row][column], moves, board)
    return moves


def move_pawn(row, column, board):
    moves = []
    for pin in board[row][column]["pinned_to"]:
        if pin[2] == "absolute":
            return moves
    if board[row][column]["color"] == "black":
        #IF black:
        if row < 7 and board[row+1][column]["piece"] == "-1":
            #IF space above is clear
            if row == 1 and board[row+2][column]["piece"] == "-1":
                moves.append([row+2, column])
            moves.append([row+1, column])
        if row < 7 and column < 7 and board[row+1][column+1]["color"] == "white":
            moves.append([row+1, column+1])
        if row < 7 and column > 0 and board[row+1][column-1]["color"] == "white":
            moves.append([row+1, column-1])
        for i, move in enumerate(moves):
            if move[0] == 7:
                moves[i].append("P")
    if board[row][column]["color"] == "white":
        #IF white:
        if row > 0 and board[row-1][column]["piece"] == "-1":
            #IF space above is clear
            if row == 6 and board[row-2][column]["piece"] == "-1":
                moves.append([row-2, column])
            moves.append([row-1, column])
        if row > 0 and column < 7 and board[row-1][column+1]["color"] == "black":
            moves.append([row-1, column+1])
        if row > 0 and column > 0 and board[row-1][column-1]["color"] == "black":
            moves.append([row-1, column-1])
        for i, move in enumerate(moves):
            if move[0] == 0:
                moves[i].append("P")
    return moves


def move_knight(row, column, board):
    piece = board[row][column]
    moves = []
    for pin in board[row][column]["pinned_to"]:
        if pin[2] == "absolute":
            return moves
    possible_move_basic(piece, row + 2, column - 1, board, moves)
    possible_move_basic(piece, row + 2, column + 1, board, moves)
    possible_move_basic(piece, row + 1, column + 2, board, moves)
    possible_move_basic(piece, row - 1, column + 2, board, moves)
    possible_move_basic(piece, row - 2, column + 1, board, moves)
    possible_move_basic(piece, row - 2, column - 1, board, moves)
    possible_move_basic(piece, row + 1, column - 2, board, moves)
    possible_move_basic(piece, row - 1, column - 2, board, moves)
    return moves


def move_king(row, column, board):
    piece = board[row][column]
    moves = []
    if main.is_in_attacked_points([row, column], piece["color"], board):
        piece["checked"] = True
    if not main.is_in_attacked_points([row+1,column+1], piece["color"], board):
        possible_move_basic(piece, row + 1, column + 1, board, moves)
    if not main.is_in_attacked_points([row,column+1], piece["color"], board):
        possible_move_basic(piece, row, column + 1, board, moves)
    if not main.is_in_attacked_points([row-1,column+1], piece["color"], board):
        possible_move_basic(piece, row - 1, column + 1, board, moves)
    if not main.is_in_attacked_points([row-1,column-1], piece["color"], board):
        possible_move_basic(piece, row - 1, column - 1, board, moves)
    if not main.is_in_attacked_points([row+1,column-1], piece["color"], board):
        possible_move_basic(piece, row + 1, column - 1, board, moves)
    if not main.is_in_attacked_points([row+1,column], piece["color"], board):
        possible_move_basic(piece, row + 1, column, board, moves)
    if not main.is_in_attacked_points([row-1,column], piece["color"], board):
        possible_move_basic(piece, row - 1, column, board, moves)
    if not main.is_in_attacked_points([row,column-1], piece["color"], board):
        possible_move_basic(piece, row, column - 1, board, moves)
    if piece["times_moved"] == 0 and piece["attackers"] == 0:
        pot_rook1 = board[row][7]
        pot_rook2 = board[row][0]
        pot_rook1["possible_moves"] = main.possible_moves(row,7,board)
        pot_rook2["possible_moves"] = main.possible_moves(row,0,board)
        if pot_rook1["piece"] == "rook" and pot_rook1["times_moved"] == 0:
            # if pot_rook1["possible_moves"]:
            if main.contains_possible_move(pot_rook1,[row, 5]):
                if not main.is_attack_points_in_range([row,7],[row,4],board,piece["color"]):
                    moves.append(["o-o"])
        if pot_rook2["piece"] == "rook" and pot_rook2["times_moved"] == 0:
            if main.contains_possible_move(pot_rook2,[row, 3]):
                if not main.is_attack_points_in_range([row,7],[row,4],board,piece["color"]):
                    moves.append(["o-o-o"])
    return moves


def possible_move_basic(piece, target_row, target_column, board, moves):
    if -1 < target_row < 8 and -1 < target_column < 8:
        if not main.is_same_color(piece, board[target_row][target_column]):
            board[target_row][target_column]["attackers"] += 1
            moves.append([target_row, target_column])
        else:
            board[target_row][target_column]["defenders"] += 1


def possible_moves_in_direction(row, column, direction, piece, moves, board):
    if row + direction[0] > 7:
        return moves
    if column + direction[1] > 7:
        return moves
    if row + direction[0] < 0:
        return moves
    if column + direction[1] < 0:
        return moves
    if main.is_same_color(piece, board[row + direction[0]][column + direction[1]]):
        board[row+direction[0]][column+direction[1]]["defenders"] += 1
        return moves
    moves.append([row + direction[0], column + direction[1]])
    if board[row+direction[0]][column+direction[1]]["piece"] != "-1":
        board[row+direction[0]][column+direction[1]]["attackers"] += 1
        pinned = pinned_to(row + direction[0], column + direction[1], direction, piece, board)
        if pinned:
            board[row+direction[0]][column + direction[1]]["pinned_to"].append(pinned)
        return moves
    return possible_moves_in_direction(row + direction[0], column + direction[1], direction,
                                            piece, moves, board
                                            )


def pinned_to(row, column, direction, piece, board):
    if row + direction[0] > 7:
        return None
    if column + direction[1] > 7:
        return None
    if row + direction[0] < 0:
        return None
    if column + direction[1] < 0:
        return None
    if main.is_same_color(piece, board[row + direction[0]][column + direction[1]]):
        return None
    if board[row+direction[0]][column+direction[1]]["piece"] != "-1":
        if main.is_king(board[row + direction[0]][column + direction[1]]):
            # main.possible_moves(row + direction[0], column + direction[1], board)
            return [board[row + direction[0]][column + direction[1]]["piece"], direction, "absolute"]
        return [board[row+direction[0]][column+direction[1]]["piece"], direction, "normal"]
    pinned_to(row + direction[0], column + direction[1], direction, piece, board)
