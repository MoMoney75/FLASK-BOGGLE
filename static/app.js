let scoreContainer = document.getElementById("score");
let score = 0;
let seconds = 60000;
let submittedWords = [];
const submitButton = document.getElementById("submit");
submitButton.addEventListener("click", handleSubmit, showMessage);

//function for when clock runs out, user is alerted
//and given final score.
async function endGame() {
  await axios.post("/end-game", { score: score });

  $("#submit").hide();
  $("#form").hide();
  $("h2").hide();
  $("#game_board").hide()

  showEndGame = document.createElement("div");
  showEndGame.innerText = `You're out of time! Your total score is ${score}`;
  showEndGame.setAttribute('id','endGameMessage')
  document.body.appendChild(showEndGame);
}

//timer set to 60 seconds, when timer runs out, endgame() is called
const initialTimer = setTimeout(() => {
  endGame();
}, seconds);

async function handleSubmit(e) {
  e.preventDefault();
  let $word = $("#word").val();

  //if no word is entered, do nothing
  if (!$word) return;

  const res = await axios.get("/answer", { params: { word: $word } });
  let response = res.data.response;
  showMessage(response);

  $("#word").val("");
}

//get the user entry and append it to the page along with
//the response from our server
function showMessage(response) {
  let $word = $("#word").val();


//returns response based on the result from boggle.py checl_word method
  if (response == "not-word") {
  alert(`${$word} - not a valid word!`);
  } else if (response == "not-on-board") {
    alert(`${$word} - that word is not on the board!`);
  } else {
    if (response === "ok") {
      if (submittedWords.includes($word)) {
      alert(`${$word} has already been used, you get no points`);
        return;
      }

      submittedWords.push($word);
    }
    //if word is in words, increment score by number of letters in word
    alert(`${$word} - good word!`);
    score += $word.length;
    scoreContainer.innerText = `your total score is ${score}`;
  }
}
