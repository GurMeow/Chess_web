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
    console.log((i*8 + j) % 2)
    if ((i+j+1) % 2 === 0)
    {
        return [color1, color1Dark];

    }
    else
    {
        return [color2, color2Dark];
    }
}

function mousedown(i, j) {
    const clicked_button = button_board[i][j];

    // If the same square is clicked again, reset it
    if (previous_button === clicked_button) {
        const [originalColor, _] = find_color(i, j);
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

    // Set new active square
    active_button = [i, j];
    previous_coords = [i, j];
    previous_button = clicked_button;

    clicked_button.style.backgroundColor = find_color(i, j)[1]; // Or whatever highlight color you like

    console.log("Selected:", i, j);

    console.log(get_possible_moves(i, j));
}


function mouseup(i, j)
{

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

console.log(button_board[0][0])

console.log(value_board)


async function get_possible_moves(posx, posy) {
    const formData = new FormData();
    formData.append("posx", posx);
    formData.append("posy", posy);
    await fetch("http://127.0.0.1:5000/get_move", {
        method: "POST",
        body: formData
    });
}
