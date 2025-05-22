#main-headline {
    color: black;
    position: absolute;
    left: 50%;
    white-space: nowrap;
    transform: translate(-50%, -50%);
    font-size: 4vw;
}

#main-board {
    border: 2px solid rgb(130, 130, 130); /* Change the border color and width as per your preference */
    border-collapse: collapse;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

#follow-img {
    position: absolute;
    pointer-events: none; /* So it doesn't block clicks */
    width: 50px;          /* Adjust size */
    height: 50px;
    transition: transform 0.05s ease; /* Smooth following */
}

#promotion-board {
    position: absolute;
    top: 50%;
    left: 25%;
    transform: translate(-50%, -50%);
    width: 6vw;          /* Adjust size */
    height: 30vw;
}

#return-button {
    background-color: #ffffff;
    color: #006400; /* Dark green text */
    border: 2px solid #ffffff;
    padding: 0.75em 2em;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    position: absolute;
    top: 5%;
    left: 7%;
}

#return-button:hover {
    color: #004d00;
    transform: scale(1.05);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.promotion-img {
    width: 4vw;
    height: 4vw;
}

.square-button:active {
    filter: brightness(80%);
}

body {
    background-color: rgb(0, 160, 0);
}
