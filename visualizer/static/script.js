// static/script.js
document.addEventListener("DOMContentLoaded", function () {

  const predictButton = document.getElementById("predictButton");
  predictButton.addEventListener("click", predict);
});

function predict() {
  const loadingSign = document.createElement("div");
  loadingSign.innerText = "Loading...";
  loadingSign.style.position = "fixed";
  loadingSign.style.top = "50%";
  loadingSign.style.left = "50%";
  loadingSign.style.transform = "translate(-50%, -50%)";
  document.body.appendChild(loadingSign);

  const userInput = document.getElementById("textInput").value;

  fetch('/perform_magic', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ userInput }),
  })
  .then(response => response.json())
  .then(result => {
    document.body.removeChild(loadingSign);

    // Create a new page
    localStorage.setItem('jsonPrediction', JSON.stringify(result));
  })
  .catch(error => {
    document.body.removeChild(loadingSign);
    console.error('Error:', error);
  });
}
