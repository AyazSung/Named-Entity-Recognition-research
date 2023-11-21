const jsonDataString = localStorage.getItem('jsonPrediction');
const jsonData = JSON.parse(jsonDataString);

console.log(jsonData);

displayMarkedText(jsonData);

function displayMarkedText(result) {
  const markedTextContainer = document.getElementById("markedText");

  const words = result.text.split(" ");

  words.forEach((word, index) => {
    const markedWord = result.marking[index];

    if (markedWord) {
      const { desc, prob } = markedWord;
      const highlightedWord = createHighlightedWord(word, prob, desc);
      markedTextContainer.appendChild(highlightedWord);
    } else {
       const span = document.createElement("div");
       span.classList.add("usual-word");
      span.textContent = word;
      markedTextContainer.appendChild(span);
    }
  });
}

function createHighlightedWord(word, probability, description) {
  const span = document.createElement("div");
  span.classList.add("word-highlight");
  span.style.backgroundColor = `rgba(255, 165, 0, ${probability})`;
  span.textContent = word;
  span.setAttribute('data-tooltip', description)

  return span;
}

function returnBack(){

}