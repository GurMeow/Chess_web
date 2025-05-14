const main_board = document.getElementById("main-board");

const color1 = "rgb(115, 149, 82)";
const color2 = "rgb(235, 236, 208)";
let color_check = true;

const value_board = [];
const button_board = []

for (let i = 0; i < 8; i++) {
    const new_row = document.createElement("tr");
    main_board.appendChild(new_row);

    const value_row = [];

    const row_of_buttons = [];

    if (color_check) {
        color_check = false;
    }
    else
    {
        color_check = true;
    }

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

        if (j == 0)
        {
            const square_number = document.createElement("p");
            square_number.textContent = 8 - i;
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
    square_letter.style.bottom = "5%";
    square_letter.style.left = "70%";
    square_letter.style.margin = "0";
    square_letter.style.fontSize = "1vw";
    button_board[7][i].style.position = "relative";
      
    button_board[7][i].appendChild(square_letter);
}