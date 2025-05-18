function Get_Picture(i, j) {
    return button_board[i][j].querySelector("img");
}

function Enter_picture(piece_name)
{
    return `/static/resources/${piece_name}.png`;
}

function Set_Picture(i, j) {
    Get_Picture(i, j).src = Enter_picture(pieces_board[i][j]);
    Get_Picture(i, j).style.width = "4vw";
    Get_Picture(i, j).style.height = "4vw";
}


function Set_Board_Pieces() {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (pieces_board[i][j] !== "-")
            {
                Set_Picture(i, j);
            }
        }
    }
}

function find_color(i, j)
{
    if ((i+j+1) % 2 === 0)
    {
        return [color1, color1Dark];

    }
    else
    {
        return [color2, color2Dark];
    }
}

function same_piece_color_for_turn(piece)
{
    if (piece[0] === "W" && whites_turn)
    {
        return true
    }
    else if (piece[0] === "B" && !whites_turn)
    {
        return true
    }
    return false
}

function clear_all_buttons_color()
{
    king_castle = false;
    queen_castle = false;
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            button_board[i][j].style.backgroundColor = find_color(i, j)[0];
            possible_squares_to_go = [];
        }
    }
}

function check_if_selected_is_move(i, j)
{
    for (let x = 0; x < possible_squares_to_go.length; x++)
    {
        if (i === possible_squares_to_go[x][0] && j === possible_squares_to_go[x][1])
        {
            return true
        }
    }
    return false
}

function write_chess_notation(i, j) {
    console.log(`${value_board[previous_coords[0]][previous_coords[1]]}->${value_board[i][j]}`)
    return `${value_board[previous_coords[0]][previous_coords[1]]}->${value_board[i][j]}`;
}

function check_for_castles(possible_moves)
{
    for (let i = 0; i < possible_moves.length; i++)
    {
        if (possible_moves[i][0] === "o-o")
        {
            king_castle = true;
        }
        if (possible_moves[i][0] === "o-o-o")
        {
            queen_castle = true;
        }
    }
}

function switch_rook_for_castle(i, j, i2, j2)
{
    pieces_board[i][j] = "-";
    if (whites_turn)
    {
        pieces_board[i2][j2] = "WRook";
    }
    else
    {
        pieces_board[i2][j2] = "BRook";
    }
    const rook_img = button_board[i][j].querySelector("img");
    rook_img.src = "";
    rook_img.style.display = "none";
    button_board[i2][j2].querySelector("img").src = Enter_picture(pieces_board[i2][j2]);
    button_board[i2][j2].querySelector("img").style.width = "4vw";
    button_board[i2][j2].querySelector("img").style.height = "4vw";
    button_board[i2][j2].querySelector("img").style.display = "";
}


async function mousedown(i, j) {
    if (!check_if_selected_is_move(i, j))
    {
        clear_all_buttons_color();

        const clicked_button = button_board[i][j];

        // If the same square is clicked again, reset it
        if (previous_button === clicked_button) {
            const [originalColor, _] = find_color(i, j)[0];
            clicked_button.style.backgroundColor = originalColor;

            // Clear state
            previous_button = null;
            previous_coords = null;
            active_button = [];

            console.log("Deselected:", i, j);
            return;
        }

        // Reset previously selected square if it exists
        if (previous_button) {
            const [prev_i, prev_j] = previous_coords;
            const [originalColor, _] = find_color(prev_i, prev_j);
            previous_button.style.backgroundColor = originalColor;
        }

        console.log(pieces_board[i][j] !== "-" && same_piece_color_for_turn(pieces_board[i][j]))

        // Set new active square
        if (pieces_board[i][j] !== "-" && same_piece_color_for_turn(pieces_board[i][j]))
        {
            console.log("e")
            active_button = [i, j];
            previous_coords = [i, j];
            previous_button = clicked_button;

            clicked_button.style.backgroundColor = find_color(i, j)[1]; // Or whatever highlight color you like

            console.log("Selected:", i, j);

            const possible_moves = await get_possible_moves(i, j);
            check_for_castles(possible_moves);

            if (king_castle && whites_turn)
            {
                possible_squares_to_go.push([7, 6]);
                button_board[7][6].style.backgroundColor = find_color(7, 6)[1];
                console.log("r")
            }
            else if (king_castle)
            {
                possible_squares_to_go.push([0, 6]);
                button_board[0][6].style.backgroundColor = find_color(0, 6)[1];
                console.log("r")
            }

            if (queen_castle && whites_turn)
            {
                possible_squares_to_go.push([7, 2]);
                button_board[7][2].style.backgroundColor = find_color(7, 2)[1];
                console.log("r")
            }
            else if (queen_castle)
            {
                possible_squares_to_go.push([0, 2]);
                button_board[0][2].style.backgroundColor = find_color(0, 2)[1];
                console.log("r")
            }

            for (let i = 0; i < possible_moves.length; i++)
            {
                if (possible_moves[i][0] !== "o-o" && possible_moves[i][0] !== "o-o-o")
                {
                    const [possible_i, possible_j] = possible_moves[i];
                    console.log(possible_i, possible_j)
                    button_board[possible_i][possible_j].style.backgroundColor = find_color(possible_i, possible_j)[1];
                    possible_squares_to_go.push(possible_moves[i]);
                }
            }
            console.log(possible_squares_to_go)
        }
        else
        {
            active_button = null;
            previous_coords = null;
            previous_button = null;
            possible_squares_to_go = [];
        }
        console.log(possible_squares_to_go)
    }
    else
    {
        console.log(king_castle, i, j)
        if (king_castle && i === 7 && j === 6)
        {
            switch_rook_for_castle(7, 7, 7, 5);

            await play_move("o-o");
        }
        else if (king_castle && i === 0 && j === 6)
        {
            switch_rook_for_castle(0, 7, 0, 5);

            await play_move("o-o")
        }
        else if (queen_castle && i === 7 && j === 2)
        {
            switch_rook_for_castle(7, 0, 7, 3);

            await play_move("o-o-o")
        }
        else if (queen_castle && i === 0 && j === 2)
        {
            switch_rook_for_castle(0, 0, 0, 3);

            await play_move("o-o-o");
        }
        else
        {
            await play_move(write_chess_notation(i, j));
        }

        console.log("e2")
        clear_all_buttons_color();

        whites_turn = !whites_turn;
        king_castle = false;
        queen_castle = false;

        pieces_board[i][j] = pieces_board[previous_coords[0]][previous_coords[1]];
        pieces_board[previous_coords[0]][previous_coords[1]] = "-";

        // const piece_img = previous_button.querySelector("img").cloneNode(true);

        const img = button_board[previous_coords[0]][previous_coords[1]].querySelector("img");
        img.src = "";
        img.style.display = "none";
        button_board[i][j].querySelector("img").src = Enter_picture(pieces_board[i][j]);
        button_board[i][j].querySelector("img").style.width = "4vw";
        button_board[i][j].querySelector("img").style.height = "4vw";
        button_board[i][j].querySelector("img").style.display = "";
    }
}


function mouseup(i, j)
{
    return [i, j];
}


function Create_board() {


    for (let i = 0; i < 8; i++) {
        const new_row = document.createElement("tr");
        main_board.appendChild(new_row);

        const value_row = [];

        const row_of_buttons = [];

        color_check = !color_check;

        for (let j = 0; j < 8; j++) {
            const new_square = document.createElement("td");
            value_row.push(`${String.fromCharCode(65+j)}${8-i}`);
            new_square.style.width = "4.5vw"; // Use viewport width units
            new_square.style.height = "4.5vw";
            new_square.style.border = "none";
            new_square.style.padding = "0";
            new_square.style.margin = "0";
            new_row.appendChild(new_square);

            const square_btn = document.createElement("button");
            square_btn.className = "square-button"
            square_btn.style.width = "100%";
            square_btn.style.height = "100%";
            square_btn.style.padding = "0";
            square_btn.style.margin = "0";
            square_btn.style.border = "none";
            square_btn.style.display = "block";

            square_btn.addEventListener("mousedown", () => mousedown(i, j));

            square_btn.addEventListener("mouseup", () => mouseup(i, j));

            square_btn.appendChild(document.createElement("img"));

            if (color_check) {
                square_btn.style.backgroundColor = color1;
                color_check = false;
            }
            else
            {
                square_btn.style.backgroundColor = color2;
                color_check = true;
            }
            new_square.appendChild(square_btn);

            if (j === 0)
            {
                const square_number = document.createElement("p");
                square_number.textContent = `${8 - i}`;
                square_number.style.position = "absolute";
                square_number.style.bottom = "70%";
                square_number.style.left = "5%";
                square_number.style.margin = "0";
                square_number.style.fontSize = "1vw";
                square_btn.style.position = "relative";

                square_btn.appendChild(square_number);
            }

            row_of_buttons.push(square_btn);
        }

        button_board.push(row_of_buttons);
        value_board.push(value_row);
    }


    for (let i = 0; i < 8; i++) {
        const square_letter = document.createElement("p");
        square_letter.textContent = String.fromCharCode(65+i);
        square_letter.style.position = "absolute";
        square_letter.style.bottom = "-4%";
        square_letter.style.left = "80%";
        square_letter.style.margin = "0";
        square_letter.style.fontSize = "1vw";
        button_board[7][i].style.position = "relative";

        button_board[7][i].appendChild(square_letter);
    }

    Set_Board_Pieces();
}

const main_board = document.getElementById("main-board");

const color1 = "rgb(115, 149, 82)";
const color1Dark = "rgb(185, 202, 67)";
const color2 = "rgb(235, 236, 208)";
const color2Dark = "rgb(245,246,130)";
let color_check = true;

const value_board = [];
const button_board = [];

let active_button = [];
let previous_button = null;
let previous_coords = null;

let possible_squares_to_go = [];

let whites_turn = true;

let king_castle = false;
let queen_castle = false;


const pieces_board =
[
    ["BRook", "BKnight", "BBishop", "BQueen", "BKing", "BBishop", "BKnight", "BRook"],
    ["BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn"],
    ["WRook", "WKnight", "WBishop", "WQueen", "WKing", "WBishop", "WKnight", "WRook"]
];

Create_board();


async function get_possible_moves(posx, posy) {
    const formData = new FormData();
    formData.append("posx", posx);
    formData.append("posy", posy);

    const response = await fetch("http://127.0.0.1:5000/get_move", {
        method: "POST",
        body: formData
    });

    const data = await response.json(); // parse the JSON response
    console.log(data); // do something with the data
    return data;
}


async function play_move(notation) {
    const formData = new FormData();
    formData.append("move_encoding", notation);
    await fetch("http://127.0.0.1:5000/play_move", {
        method: "POST",
        body: formData
    });
}
