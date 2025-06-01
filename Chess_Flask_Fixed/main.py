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
import random
import os
from collections import defaultdict


def encoding_to_move(command):
    global turn, zobrist_table
    update_possible_moves(chess_board)
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
            if command == "o-o-o":
                chess_board[7][2] = chess_board[7][4]
                chess_board[7][4] = {"color": "-1", "piece": "-1"}
                chess_board[7][3] = chess_board[7][0]
                chess_board[7][0] = {"color": "-1", "piece": "-1"}
                chess_board[7][2]["times_moved"] += 1
                chess_board[7][3]["times_moved"] += 1
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
            if command == "o-o-o":
                chess_board[0][2] = chess_board[7][4]
                chess_board[0][4] = {"color": "-1", "piece": "-1"}
                chess_board[0][3] = chess_board[7][0]
                chess_board[0][0] = {"color": "-1", "piece": "-1"}
                chess_board[0][2]["times_moved"] += 1
                chess_board[0][3]["times_moved"] += 1
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
            if chess_board[piece_row][piece_column]["color"] != turn:
                return "Illegal move"
            if contains_possible_move(chess_board[piece_row][piece_column],
                                      [target_row, target_column, 'P']):
                if parts[1][2:] == "ro":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "rook", "times_moved": 1}
                if parts[1][2:] == "bi":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "bishop",
                                                              "times_moved": 1}
                if parts[1][2:] == "qu":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "queen", "times_moved": 1}
                if parts[1][2:] == "kn":
                    chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
                    chess_board[target_row][target_column] = {"color": turn, "piece": "knight",
                                                              "times_moved": 1}
            elif contains_possible_move(chess_board[piece_row][piece_column], [target_row, target_column]):
                chess_board[piece_row][piece_column]["times_moved"] += 1
                chess_board[target_row][target_column] = chess_board[piece_row][piece_column]
                chess_board[piece_row][piece_column] = {"color": "-1", "piece": "-1"}
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


def update_possible_moves(board):
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
            if is_king(board[i][j]):
                king_positions.append([i, j])
                continue
            if board[i][j]["color"] != "-1":
                board[i][j]["possible_moves"], board[i][j]["checks"] = possible_moves(i, j, board)
    for pos in king_positions:
        board[pos[0]][pos[1]]["possible_moves"], _ = possible_moves(pos[0], pos[1], board)
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
chess_board = update_possible_moves(chess_board)
move_dict = defaultdict(int)
move_dict[get_zobrist_hash(chess_board, zobrist_table)] = 1

if __name__ == '__main__':
    autoplay = False
    run = True
    print_board(chess_board)
    start = time.time()
    command = test_file.minimax_move_undo(depth,chess_board,turn,1)[1]
    print(command)
    print(f"calculation took {time.time() - start} seconds to finish")
    while run:
        if not autoplay:
            command = input("Enter command: ")
        if command == "exit":
            break
        elif command == "all possible boards":
            for i in eval_board.all_possible_boards(chess_board, turn)[0]:
                print_board(i)
                print("\n\n\n")
        elif command == "eval board":
            print(f"evalualtion: {eval_board.evaluate_current_board(chess_board)}")
        elif command == "apbi":
            depth = input("please enter the depth you want: ")
            for i in eval_board.get_all_possible_boards_after_n_moves(int(depth), chess_board, turn, 1)[0]:
                print(i, end="\n\n\n")
            # for i in eval_board.get_all_possible_boards_after_n_moves(int(depth), chess_board, turn, 1):
            #     for j in i:
            #         print(j)
            #         print_board(j)
            #         print("\n\n\n")
        elif command == "get best move":
            depth = input("please enter the depth you want: ")
            print(eval_board.get_best_board_after_n_moves(depth, chess_board, turn, 1))
        elif command[0].isupper() or command == "o-o" or command == "o-o-o":
            if encoding_to_move(command) == "Illegal move":
                print("Illegal move")
                continue
            update_possible_moves(chess_board)
            print_board(chess_board)
            print(chess_board)
            if turn == "white":
                turn = "black"
            else:
                turn = "white"
            start = time.time()
            result = test_file.minimax_move_undo(depth,chess_board,turn,1)
            command = result[1]
            print(command)
            print(f"calculation took {time.time()-start} to finish. with a position score of {result[0]}")
        else:
            print(eval(command))


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
    global turn, depth, chess_board, move_dict
    turn = "white"
    chess_board, zobrist_table = init_game_board()
    chess_board = update_possible_moves(chess_board)
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
    chess_board = update_possible_moves(chess_board)
    return jsonify(chess_board)


@app.route("/get_engine_move")
def get_engine_move():
    global turn, depth, chess_board
    start = time.time()
    z_table = copy.deepcopy(zobrist_table)
    z_hash = copy.deepcopy(get_zobrist_hash(chess_board, zobrist_table))
    mov_dict = copy.deepcopy(move_dict)
    thingy = test_file.minimax_move_undo(depth, chess_board, turn, zobrist_table = z_table, zobirst_hash= z_hash, move_dict = mov_dict)
    res = jsonify (thingy)
    print(f"took {time.time() - start} seconds")
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
