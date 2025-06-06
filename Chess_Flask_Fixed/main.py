# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
#
import copy
import time
from flask import Flask, render_template, redirect, url_for, jsonify, request, send_file
import test_file
import chess_pieces
import eval_board
import game_state
import random
import os
from collections import defaultdict


def encoding_to_move(command):
    global turn, zobrist_table, moves
    update_possible_moves(chess_board, turn)
    if command == "o-o-o" or command == "o-o":
        nope_flag = 0
        if turn == "white" and (
                contains_possible_move(chess_board[7][4], ["o-o"]) or contains_possible_move(chess_board[7][4],
                                                                                             ["o-o-o"])):
            if command == "o-o":
                chess_board[7][6] = chess_board[7][4]
                chess_board[7][4] = chess_board[7][5]
                chess_board[7][5] = chess_board[7][7]
                chess_board[7][7] = chess_board[7][4]
                chess_board[7][6]["times_moved"] += 1
                chess_board[7][5]["times_moved"] += 1
                moves = test_file.record_moves("O-O", moves)
            if command == "o-o-o":
                chess_board[7][2] = chess_board[7][4]
                chess_board[7][4] = {"color": "-1", "piece": "-1"}
                chess_board[7][3] = chess_board[7][0]
                chess_board[7][0] = {"color": "-1", "piece": "-1"}
                chess_board[7][2]["times_moved"] += 1
                chess_board[7][3]["times_moved"] += 1
                moves = test_file.record_moves("O-O-O", moves)

        else:
            nope_flag += 1
        if turn == "black" and (
                contains_possible_move(chess_board[0][4], ["o-o"]) or contains_possible_move(chess_board[0][4],
                                                                                             ["o-o-o"])):
            if command == "o-o":
                chess_board[0][6] = chess_board[0][4]
                chess_board[0][4] = chess_board[0][5]
                chess_board[0][5] = chess_board[0][7]
                chess_board[0][7] = chess_board[0][4]
                chess_board[0][5]["times_moved"] += 1
                chess_board[0][6]["times_moved"] += 1
                moves = test_file.record_moves("O-O", moves)
            if command == "o-o-o":
                chess_board[0][2] = chess_board[7][4]
                chess_board[0][4] = {"color": "-1", "piece": "-1"}
                chess_board[0][3] = chess_board[7][0]
                chess_board[0][0] = {"color": "-1", "piece": "-1"}
                chess_board[0][2]["times_moved"] += 1
                chess_board[0][3]["times_moved"] += 1
                moves = test_file.record_moves("O-O-O", moves)

        else:
            if nope_flag == 1:
                return "Illegal move"
    else:
        try:
            parts = command.split("->")
            piece_column = ord(parts[0][0]) - 65
            piece_row = 7 - int(parts[0][1]) + 1
            target_column = ord(parts[1][0]) - 65
            target_row = 7 - int(parts[1][1]) + 1
            piece = copy.deepcopy(chess_board[piece_row][piece_column])
            prefix = ""
            if piece["piece"] == "queen":
                prefix = "Q"
            elif piece["piece"] == "rook":
                prefix = "R"
            elif piece["piece"] == "bishop":
                prefix = "B"
            elif piece["piece"] == "knight":
                prefix = "N"
            elif piece["piece"] == "king":
                prefix = "K"
            captured = copy.deepcopy(chess_board[target_row][target_column])
            if chess_board[piece_row][piece_column]["color"] != turn:
                return "Illegal move"
            if contains_possible_move(chess_board[piece_row][piece_column],
                                      [target_row, target_column, 'P']):
                if parts[1][2:] == "ro":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "rook", "times_moved": 1}
                    moves = test_file.record_moves(
                        f"{prefix}{parts[0][0].lower()}{parts[0][1]}{parts[1][0].lower()}{parts[1][1]}R", moves)
                if parts[1][2:] == "bi":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "bishop",
                                                              "times_moved": 1}
                    moves = test_file.record_moves(
                        f"{prefix}{parts[0][0].lower()}{parts[0][1]}{parts[1][0].lower()}{parts[1][1]}B", moves)
                if parts[1][2:] == "qu":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "queen", "times_moved": 1}
                    moves = test_file.record_moves(
                        f"{prefix}{parts[0][0].lower()}{parts[0][1]}{parts[1][0].lower()}{parts[1][1]}Q", moves)
                if parts[1][2:] == "kn":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "knight",
                                                              "times_moved": 1}
                    moves = test_file.record_moves(
                        f"{prefix}{parts[0][0].lower()}{parts[0][1]}{parts[1][0].lower()}{parts[1][1]}N", moves)
            elif contains_possible_move(chess_board[piece_row][piece_column], [target_row, target_column]):
                chess_board[piece_row][piece_column]["times_moved"] += 1
                chess_board[target_row][target_column] = chess_board[piece_row][piece_column]
                chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                moves = test_file.record_moves(f"{prefix}{parts[0][0].lower()}{parts[0][1]}{parts[1][0].lower()}{parts[1][1]}", moves)
            else:
                return "Illegal move"
        except Exception as e:
            print(e)
            return "Illegal move"
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    move_dict[get_zobrist_hash(chess_board, zobrist_table)] += 1
    return chess_board, move_dict[get_zobrist_hash(chess_board, zobrist_table)]


def is_attack_points_in_range(point_a,point_b,board,turn):
    for i in range(abs(point_a[0]-point_b[0])+1):
        for j in range(abs(point_a[1]-point_b[1])+1):
            if is_in_attacked_points([i+min(point_a[0],point_b[0]),j+min(point_a[1],point_b[1])], turn, board):
                return True
    return False


def is_in_attacked_points(target, turn, board):
    for point in attacked_points(turn, board):
        if point == target:
            return True
    return False


def attacked_points(turn, board):
    attacked_points = []
    # print(turn)
    # print_board(board)
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if turn == piece["color"] or piece["color"] == "-1":
                continue
            if piece["piece"] == "pawn":
                if piece["color"] == "white":
                    if i > 0 and j > 0:
                        attacked_points.append([i-1, j-1])
                    if i > 0 and j < 7:
                        attacked_points.append([i-1, j+1])
                else:
                    if i < 7 and j > 0:
                        attacked_points.append([i+1, j-1])
                    if i < 7 and j < 7:
                        attacked_points.append([i+1, j+1])
                continue
            for possibility in board[i][j]["possible_moves"]:
                if possibility == ["o-o"] or possibility == ["o-o-o"]:
                    continue
                attacked_points.append(possibility)
    return attacked_points


def contains_possible_move(piece, target):
    if piece["color"] == "-1":
        return False
    if not piece["possible_moves"]:
        return False
    for possibility in piece["possible_moves"]:
        if possibility == target:
            return True
    return False


def update_possible_moves(board, turn):
    king_positions = []
    for i in range(8):
        for j in range(8):
            board[i][j]["defenders"] = 0
            board[i][j]["attackers"] = 0
            board[i][j]["pinned_to"] = []
            board[i][j]["possible_moves"] = []
            board[i][j]["checks"] = []
    for i in range(8):
        for j in range(8):
            if board[i][j]["color"] == "-1":
                continue
            if is_king(board[i][j]):
                king_positions.append([i, j])
                continue
            board[i][j]["possible_moves"], board[i][j]["checks"] = possible_moves(i, j, board)
    for pos in king_positions:
        board[pos[0]][pos[1]]["possible_moves"], _ = possible_moves(pos[0], pos[1], board)
        game_state.white_in_check = False
        game_state.black_in_check = False
        if board[pos[0]][pos[1]]["color"] == "white" and board[pos[0]][pos[1]]["attackers"] > 0:
            game_state.white_in_check = True
        if board[pos[0]][pos[1]]["color"] == "black" and board[pos[0]][pos[1]]["attackers"] > 0:
            game_state.black_in_check = True
        game_state.any_color_in_check = game_state.white_in_check or game_state.black_in_check
    for i in range(8):
        for j in range(8):
            if not board[i][j]["pinned_to"]:
                continue
            if board[i][j]["color"] != "-1":
                board[i][j]["possible_moves"], board[i][j]["checks"] = possible_moves(i, j, board)
    return board


def possible_moves(row, column, board):
    current_square = board[row][column]
    piece = current_square["piece"]
    if piece == "rook":
        return chess_pieces.move_rook(row, column, board)
    if piece == "bishop":
        return chess_pieces.move_bishop(row, column, board)
    if piece == "knight":
        return chess_pieces.move_knight(row, column, board)
    if piece == "queen":
        return chess_pieces.move_queen(row, column, board)
    if piece == "king":
        return chess_pieces.move_king(row, column, board)
    if piece == "pawn":
        return chess_pieces.move_pawn(row, column, board)


def is_same_color(position, target):
    # print(position,target)
    return position["color"] == target["color"]


def set_color(position, color):
    position["color"] = color
    return position


def set_color_array(array, color):
    for i in range(len(array)):
        array[i] = set_color(array[i], color)
    return array


def is_white(position):
    return position["color"] == "white"


def is_king(position):
    return position["piece"] == "king"


def print_board(board):
    for i in board:
        for j in i:
            piece = j["piece"]
            color = j["color"][0]
            if piece == "-1":
                print("---", end=" ")
                continue
            print(f"{color}{piece[:2]}", end=" ")
        print("\n")


def init_game_board():
    board = [[{"color": "white", "piece": "rook"}, {"color": "white", "piece": "knight"}, {"color": "white", "piece": "bishop"}, {"color": "white", "piece": "queen"},
              {"color": "white", "piece": "king", "hasCastled": False}, {"color": "white", "piece": "bishop"}, {"color": "white", "piece": "knight"}, {"color": "white", "piece": "rook"}],
             [{"color": "white", "piece": "pawn"}, {"color": "white", "piece": "pawn"},
              {"color": "white", "piece": "pawn"}, {"color": "white", "piece": "pawn"},
              {"color": "white", "piece": "pawn"}, {"color": "white", "piece": "pawn"},
              {"color": "white", "piece": "pawn"}, {"color": "white", "piece": "pawn"}]
    ]
    for i in range(4):
        board.append([])
        for j in range(8):
            board[i+2].append({"color": "-1", "piece": "-1"})
    board.append(copy.deepcopy(board[1]))
    board.append(copy.deepcopy(board[0]))
    set_color_array(board[1], "black")
    set_color_array(board[0], "black")
    for i in range(8):
        for j in range(8):
            board[i][j]["times_moved"] = 0
    piece_types = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    colors = ["white", "black"]

    zobrist_table = {
        (sq, piece, color): random.getrandbits(64)
        for sq in range(64)
        for piece in piece_types
        for color in colors
    }
    return board, zobrist_table


def get_zobrist_hash(board, zobrist_table):
    h = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece["piece"] != "-1":
                piece_type = piece["piece"]
                color = piece["color"]
                sq = row * 8 + col
                h ^= zobrist_table[(sq, piece_type, color)]
    return h


turn = "white"
depth = 2
chess_board, zobrist_table = init_game_board()
chess_board = update_possible_moves(chess_board, turn)
move_dict = defaultdict(int)
move_dict[get_zobrist_hash(chess_board, zobrist_table)] = 1
moves = []
bot = False
player_time = 600
player_timer = False
app = Flask(__name__)
app.run(debug=True)
template_dir = os.path.abspath('web/templates')
app.template_folder = template_dir
static_dir = os.path.abspath('web/static')
app.static_folder = static_dir

bot = False

@app.route("/")
def load_home_page():
    global bot
    bot = False
    return render_template("main.html", title="Home | Chess App")

@app.route("/play")
def play():
    global turn, depth, chess_board, move_dict, moves
    turn = "white"
    moves = []
    game_state.init()
    chess_board, zobrist_table = init_game_board()
    chess_board = update_possible_moves(chess_board, turn)
    move_dict = defaultdict(int)
    move_dict[get_zobrist_hash(chess_board, zobrist_table)] = 1
    return render_template("index.html", title="Main Game | Chess App")


@app.route("/play_bot")
def change_bot():
    global bot
    bot = True


@app.route("/get_bot")
def get_bot():
    global bot
    return jsonify(bot)


@app.route("/get_move", methods=['POST'])
def get_possible_moves():
    posx = request.form.get('posx')
    posy = request.form.get('posy')
    return jsonify(chess_board[int(posx)][int(posy)]["possible_moves"])


@app.route("/play_move", methods=['POST'])
def play_move():
    global turn, chess_board
    move_encoding = request.form.get("move_encoding")
    chess_board, times_position_happend = encoding_to_move(move_encoding)
    chess_board = update_possible_moves(chess_board, turn)
    return jsonify(chess_board)


@app.route("/get_engine_move")
def get_engine_move():
    global turn, depth, chess_board
    start = time.time()
    z_table = copy.deepcopy(zobrist_table)
    z_hash = copy.deepcopy(get_zobrist_hash(chess_board, zobrist_table))
    mov_dict = copy.deepcopy(move_dict)
    thingy = test_file.minimax_move_undo(depth, chess_board, turn, zobrist_table = z_table, zobirst_hash= z_hash, move_dict = mov_dict)
    res = jsonify(thingy)
    print(f"searched {game_state.moves_calculated} moves in {time.time() - start} seconds ({game_state.moves_calculated/(time.time()-start)} moves per second)")
    print(f"got a score of {thingy[0]}")
    game_state.moves_calculated = 0
    return res


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/set_depth", methods = ["POST"])
def set_depth():
    global depth
    depth = float(request.form.get("depth"))
    # print(depth)
    return "true"


@app.route("/get_depth")
def get_depth():
    return jsonify(depth)


@app.route("/get_pgn")
def get_pgn():
    global moves
    res = test_file.create_full_pgn(moves)
    print(res)
    return res


@app.route("/change_time", methods=["POST"])
def change_time():
    global player_time
    player_time = int(request.form.get("player_time"))
    return jsonify(player_time)


@app.route("/change_timer", methods=["POST"])
def change_timer():
    global player_timer
    player_timer = request.form.get("player_timer")
    player_timer = player_timer.lower() == "true"
    return jsonify(player_timer)


@app.route("/get_time")
def get_time():
    global player_time, player_timer
    return jsonify(player_time, player_timer)
