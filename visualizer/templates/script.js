// static/script.js
document.addEventListener("DOMContentLoaded", function () {

  const predictButton = document.getElementById("predictButton");
  predictButton.addEventListener("click", predict);
});

function predict() {
  // Create and append loading spinner with white background
  const loadingSign = document.createElement("div");
  loadingSign.innerHTML = '<div class="loader"></div><p>Loading...</p>';
  loadingSign.style.position = "fixed";
  loadingSign.style.top = "0";
  loadingSign.style.left = "0";
  loadingSign.style.width = "100%";
  loadingSign.style.height = "100%";
  loadingSign.style.backgroundColor = "rgba(255, 240, 235, 0.8)"; /* Semi-transparent white background */
  loadingSign.style.display = "flex";
  loadingSign.style.flexDirection = "column";
  loadingSign.style.alignItems = "center";
  loadingSign.style.justifyContent = "center";
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
    // Remove loading spinner
    document.body.removeChild(loadingSign);

    // Create a new page
    localStorage.setItem('jsonPrediction', JSON.stringify(result));
    window.location.href = "predictionPage.html";
  })
  .catch(error => {
    // Remove loading spinner
    document.body.removeChild(loadingSign);

    // Handle error
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