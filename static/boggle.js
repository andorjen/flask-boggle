"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $boardBody = $("#board-body")

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  // console.log(response)
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  for (let row of board) {
    const $boardRow = $("<tr>")
    for (let letter of row) {
      const $boardCell = $("<td>")
      $boardCell.text(letter)
      $boardRow.append($boardCell)
    }

    $boardBody.append($boardRow)
  }
  // $table.empty();
  // loop over board and create the DOM tr/td structure
}

$form.on("submit", handleFormSubmit)

async function handleFormSubmit() {
  const inputWord = $("#wordInput").val();
  console.log(inputWord, gameId)
  const response = await axios(
    {
      method: "post",
      url: "/api/score-word",
      data: {
        word: inputWord,
        game_id: gameId
      }
    }
  )
  console.log(response)

}

start();