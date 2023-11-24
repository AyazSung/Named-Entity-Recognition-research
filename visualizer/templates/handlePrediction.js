const jsonDataString = localStorage.getItem('jsonPrediction');
const jsonData = JSON.parse(jsonDataString);

console.log(jsonData);

displayMarkedText(jsonData);

function displayMarkedText(result) {
  const markedTextContainer = document.getElementById("markedText");

  result.text_blocks.forEach((text_block) => {

    if (text_block.length === 3) {
      const [text, prob, desc] = text_block;
      const highlightedText= createHighlightedText(text, prob, desc);
      markedTextContainer.appendChild(highlightedText);
    } else {
       const div = document.createElement("div");
       div.classList.add("usual-word");
       div.textContent = text_block[0];
       markedTextContainer.appendChild(div);
    }
  });
}

function createHighlightedText(text, probability, description) {
  const div = document.createElement("div");
  div.classList.add("word-highlight");
  div.style.backgroundColor = `rgba(255, 165, 0, ${probability})`;
  div.textContent = text;
  div.setAttribute('data-tooltip', description)

  return div;
}