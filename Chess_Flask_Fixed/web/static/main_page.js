const Player_button = document.getElementById("local_button");
const Bot_button = document.getElementById("bot_button");

Player_button.addEventListener("mousedown", async () => {
    await Change_to_main_board();
});

Bot_button.addEventListener("mousedown", async () => {
    await Switch_to_bot();
    await Change_to_main_board();
});

async function Change_to_main_board() {
    window.location.href = "http://127.0.0.1:5000/play";
}

async function Switch_to_bot() {
    await fetch("http://127.0.0.1:5000/play_bot")
}
