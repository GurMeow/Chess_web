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

function show_winning_text(winner)
{
    winning_text.style.display = "";
    winning_text.innerHTML = `${winner} won!`;
    replay_button.style.display = "";
    replay_button.disabled = false;
}

function check_for_king(i, j)
{
    if (whites_turn && pieces_board[i][j] === "BKing")
    {
        show_winning_text("White");
        return false;
    }
    else if (pieces_board[i][j] === "WKing")
    {
        show_winning_text("Black");
        return false;
    }

    return true;
}

function bot_king_check(i, j)
{
    if (pieces_board[i][j] === "WKing")
    {
        show_winning_text("Black");
        return false;
    }

    console.log(i, j, pieces_board[i][j]);

    return true;
}

function unwrite_notation(notation)
{
    console.log(notation)
    const letter = notation[0].charCodeAt(0)-65;
    const number = 8 - Number(notation[1]);
    console.log(number, letter);
    return [number, letter];
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

function chess_piece_inverted(piece)
{
    if (!whites_turn || bot)
    {
        if (piece === "qu")
        {
            return "WQueen";
        }
        else if (piece === "ro")
        {
            return "WRook";
        }
        else if (piece === "bi")
        {
            return "WBishop";
        }
        else if (piece === "kn") {
            return "WKnight";
        }
    }
    else
    {
        if (piece === "qu")
        {
            return "BQueen";
        }
        else if (piece === "ro")
        {
            return "BRook";
        }
        else if (piece === "bi")
        {
            return "BBishop";
        }
        else if (piece === "kn") {
            return "BKnight";
        }
    }
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

function disable_promotion()
{
    promotion_board.style.display = "none";
    const promotion_btns = promotion_board.querySelectorAll("button");

    promotion_btns.forEach(button => {
        button.disabled = true;
        button.querySelector("img").src = "";
    });
}

function enable_promotion()
{
    promotion_board.style.display = "";
    const promotion_btns = promotion_board.querySelectorAll("button");

    promotion_btns.forEach(button => {
        button.disabled = false;
    });
    if (whites_turn)
    {
        promotion_btns[0].querySelector("img").src = Enter_picture("WQueen");
        promotion_btns[1].querySelector("img").src = Enter_picture("WRook");
        promotion_btns[2].querySelector("img").src = Enter_picture("WBishop");
        promotion_btns[3].querySelector("img").src = Enter_picture("WKnight");
    }
    else
    {
        promotion_btns[0].querySelector("img").src = Enter_picture("BQueen");
        promotion_btns[1].querySelector("img").src = Enter_picture("BRook");
        promotion_btns[2].querySelector("img").src = Enter_picture("BBishop");
        promotion_btns[3].querySelector("img").src = Enter_picture("BKnight");
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

function move_type(type)
{
    if (type === "o-o")
    {
        return "small";
    }
    else if (type === "o-o-o")
    {
        return "long";
    }
    else if (type.slice(-2) === "qu")
    {
        return "queen";
    }
    else if (type.slice(-2) === "ro")
    {
        return "rook";
    }
    else if (type.slice(-2) === "bi")
    {
        return "bishop";
    }
    else if (type.slice(-2) === "kn")
    {
        return "knight";
    }
    else
    {
        return "normal";
    }
}

function switch_imgs(i, j) {
    button_board[i][j].querySelector("img").src = Enter_picture(pieces_board[i][j]);
    button_board[i][j].querySelector("img").style.width = "4vw";
    button_board[i][j].querySelector("img").style.height = "4vw";
    button_board[i][j].querySelector("img").style.display = "";
}

function switch_bot_promotions_imgs(i, j, piece) {
    button_board[i][j].querySelector("img").src = Enter_picture(piece);
    button_board[i][j].querySelector("img").style.width = "4vw";
    button_board[i][j].querySelector("img").style.height = "4vw";
    button_board[i][j].querySelector("img").style.display = "";
}


function move_bot(first_position, second_position)
{
    const [prev_i, prev_j] = first_position
    const [i, j] = second_position;

    pieces_board[i][j] = pieces_board[prev_i][prev_j];
    pieces_board[prev_i][prev_j] = "-";


    // const piece_img = previous_button.querySelector("img").cloneNode(true);

    const img = button_board[prev_i][prev_j].querySelector("img");
    img.src = "";
    img.style.display = "none";
    switch_imgs(i, j)
}

async function engine_turn()
{
    console.log("e")

    can_play = false;

    let engine_move_played = await engine_move();
    console.log(engine_move_played)
    engine_move_played = engine_move_played[1];

    console.log(engine_move_played);

    const bot_move_type = move_type(engine_move_played);

    let first_position, second_position;

    if(bot_move_type !== "small" && bot_move_type !== "long")
    {
        first_position = engine_move_played.slice(0, 2);
        second_position = engine_move_played.slice(4, 6);

        const res = unwrite_notation(second_position)

        can_play = bot_king_check(res[0], res[1]);

        const second_unwritten = unwrite_notation(second_position);

        move_bot(unwrite_notation(first_position), second_unwritten);


        console.log(bot_move_type, first_position, second_position);

        console.log(unwrite_notation(first_position), unwrite_notation(second_position))


        if (bot_move_type === "queen")
        {
            pieces_board[second_unwritten[0]][second_unwritten[1]] = "BQueen";
            switch_bot_promotions_imgs(second_unwritten[0],second_unwritten[1], "BQueen");
        }
        else if (bot_move_type === "rook")
        {
            pieces_board[second_unwritten[0]][second_unwritten[1]] = "BRook";
            switch_bot_promotions_imgs(second_unwritten[0],second_unwritten[1], "BRook");
        }
        else if (bot_move_type === "bishop")
        {
            pieces_board[second_unwritten[0]][second_unwritten[1]] = "BBishop";
            switch_bot_promotions_imgs(second_unwritten[0],second_unwritten[1], "BBishop");
        }
        else if (bot_move_type === "knight")
        {
            pieces_board[second_unwritten[0]][second_unwritten[1]] = "BKnight";
            switch_bot_promotions_imgs(second_unwritten[0],second_unwritten[1], "BKnight");
        }
    }
    else if (bot_move_type === "small")
    {
        move_bot([0, 4], [0, 6]);
        move_bot([0, 7], [0, 5]);
        can_play = true;
    }
    else if (bot_move_type === "long")
    {
        move_bot([0, 4], [0, 2]);
        move_bot([0, 0], [0, 3]);
        can_play = true;
    }

    console.log(engine_move_played)
    await play_move(engine_move_played);
}


async function mousedown(i, j) {
    if (!check_if_selected_is_move(i, j) && can_play)
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
    else if (can_play)
    {
        can_play = check_for_king(i, j);

        console.log(pieces_board[previous_coords[0]][previous_coords[1]], i)

        if (i === 0 && pieces_board[previous_coords[0]][previous_coords[1]] === "WPawn" && can_play)
        {
            can_play = false;
            promotion = true;
            enable_promotion();
        }
        else if (i === 7 && pieces_board[previous_coords[0]][previous_coords[1]] === "BPawn" && can_play)
        {
            can_play = false;
            promotion = true;
            enable_promotion();
        }

        promoting_pawn_coords = [i, j];

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
        else if (!promotion)
        {
            await play_move(write_chess_notation(i, j));
        }

        console.log("e2")
        clear_all_buttons_color();

        pieces_board[i][j] = pieces_board[previous_coords[0]][previous_coords[1]];
        pieces_board[previous_coords[0]][previous_coords[1]] = "-";


        if (!bot)
        {
            whites_turn = !whites_turn;
        }

        king_castle = false;
        queen_castle = false;


        // const piece_img = previous_button.querySelector("img").cloneNode(true);

        const img = button_board[previous_coords[0]][previous_coords[1]].querySelector("img");
        img.src = "";
        img.style.display = "none";
        switch_imgs(i, j);

        if (bot && !promotion)
        {
            await engine_turn();
        }
    }
}


function mouseup(i, j)
{
    return [i, j];
}

async function play_promotion(piece)
{
    const [i, j] = promoting_pawn_coords;

    console.log(write_chess_notation(promoting_pawn_coords[0], promoting_pawn_coords[1]), promoting_pawn_coords[0], promoting_pawn_coords[1])
    if (whites_turn)
    {
        await play_move(`${write_chess_notation(i, j)}${piece}`)
    }
    else
    {
        await play_move(`${write_chess_notation(i, j)}${piece}`)
    }
    console.log(previous_coords)
    console.log(`${write_chess_notation(7, previous_coords[1])}${piece}`)

    disable_promotion();

    can_play = true;
    promotion = false;

    console.log(whites_turn)

    pieces_board[i][j] = chess_piece_inverted(piece);

    const promoted_img = button_board[previous_coords[0]][previous_coords[1]].querySelector("img");
    promoted_img.src = "";
    promoted_img.style.display = "none";
    button_board[i][j].querySelector("img").src = Enter_picture(pieces_board[i][j]);
    button_board[i][j].querySelector("img").style.width = "4vw";
    button_board[i][j].querySelector("img").style.height = "4vw";
    button_board[i][j].querySelector("img").style.display = "";

    if (bot)
    {
        await engine_turn();
    }
}

function upd_notations(notation)
{
    let row_color;

    if (!whites_notation)
    {
        row_color = "black-"
    }
    else
    {
        row_color = "white-"
    }
    notations.push(notation)

    const bold = document.createElement("b");
    const notation_paragraph = document.createElement("p");
    notation_paragraph.className = `${row_color}notation-text`;
    notation_paragraph.style.top = `${row_position}vw`
    notation_paragraph.innerHTML = notation
    bold.appendChild(notation_paragraph)
    document.getElementById("notation-box").appendChild(bold);

    if (!whites_notation)
    {
        row_position = row_position + 3;
    }
    whites_notation = !whites_notation
}


function Set_promotion_board()
{
    for (let i = 0; i < 4; i++)
    {
        const promotion_btn = document.createElement("button");
        promotion_btn.className = "square-button"
        promotion_btn.style.width = "100%";
        promotion_btn.style.height = "6vw";
        promotion_btn.style.padding = "0";
        promotion_btn.style.margin = "0";
        promotion_btn.style.border = "none";
        promotion_btn.style.display = "";
        promotion_btn.style.backgroundColor = "white";


        const promotion_btn_img = document.createElement("img");
        promotion_btn_img.src = "";
        promotion_btn_img.className = "promotion-img"
        promotion_btn_img.style.display = "";
        promotion_btn.appendChild(promotion_btn_img);

        promotion_board.appendChild(promotion_btn);
    }

    const promotion_btns = promotion_board.querySelectorAll("button");

    promotion_btns[0].addEventListener("mousedown", () => play_promotion("qu"));
    promotion_btns[1].addEventListener("mousedown", () => play_promotion("ro"));
    promotion_btns[2].addEventListener("mousedown", () => play_promotion("bi"));
    promotion_btns[3].addEventListener("mousedown", () => play_promotion("kn"));
}


async function Create_board(){
    bot = await get_bot_value();
    console.log(bot)

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
const promotion_board = document.getElementById("promotion-board");

const winning_text = document.getElementById("winning-text");
winning_text.style.display = "none";

const replay_button = document.getElementById("replay-button");
replay_button.style.display = "none";
replay_button.disabled = true;
replay_button.addEventListener("mousedown", async () => {
    await reload_page();
});

document.getElementById("return-button").addEventListener("mousedown", async () => {
    await return_home();
})

const color1 = "rgb(115, 149, 82)";
const color1Dark = "rgb(185, 202, 67)";
const color2 = "rgb(235, 236, 208)";
const color2Dark = "rgb(245,246,130)";
let color_check = true;

const notations = [];
let whites_notation = true;
let row_position = 0;

let bot;

const value_board = [];
const button_board = [];

let active_button = [];
let previous_button = null;
let previous_coords = null;

let possible_squares_to_go = [];

let whites_turn = true;

let king_castle = false;
let queen_castle = false;
let promotion = false;

let promoting_pawn_coords = [];

let can_play = true;


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

Create_board().then();
Set_promotion_board();

disable_promotion();

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
    upd_notations(notation);

    const formData = new FormData();
    formData.append("move_encoding", notation);
    await fetch("http://127.0.0.1:5000/play_move", {
        method: "POST",
        body: formData
    });
}

async function engine_move() {
    const response = await fetch("http://127.0.0.1:5000/get_engine_move")

    return await response.json();
}

async function return_home()
{
    window.location.href = "http://127.0.0.1:5000/";
}

async function reload_page()
{
    window.location.href = "http://127.0.0.1:5000/play";
}

async function get_bot_value() {
    const response = await fetch("http://127.0.0.1:5000/get_bot")

    return await response.json();
}
