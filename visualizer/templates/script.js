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
  const model = whatButtonIsPressed();
  const body = {
    model: model,
    userInput: userInput
  }

  fetch('/perform_magic', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  .then(response => response.json())
  .then(result => {
    document.body.removeChild(loadingSign);

    // Create a new page
    localStorage.setItem('jsonPrediction', JSON.stringify(result));
    window.location.href = "predictionPage.html";
  })
  .catch(error => {
    document.body.removeChild(loadingSign);
    console.error('Error:', error);
  });
}
document.addEventListener('DOMContentLoaded', function () {
      const buttons = document.querySelectorAll('.button');

      buttons[0].classList.add('active');

      buttons.forEach(button => {
        button.addEventListener('click', function () {
          buttons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
          // You can now use this.id or other attributes to identify the pressed button
        });
      });
    });
function whatButtonIsPressed() {
  const buttons = document.querySelectorAll('.button');

  for (const button of buttons) {
    if (button.classList.contains('active')) {
      return button.id;
    }
  }
}