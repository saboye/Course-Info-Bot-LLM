function getResponse() {
  const userInput = $("#user_input").val().trim();
  if (userInput === "") {
    alert("Please enter a query.");
    return;
  }

  appendUserMessage(userInput);
  sendUserQuery(userInput);
  clearInputField();
}

function appendUserMessage(message) {
  $("#chat-box").prepend(`<div class="message user-message">${message}</div>`);
}

function sendUserQuery(query) {
  $.ajax({
    url: "/get_response",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ user_input: query }),
    success: handleResponse,
    error: handleError,
  });
}

function handleResponse(response) {
  const botMessage = $('<div class="message bot-message"></div>');
  const responseText = response.response;

  if (responseText.includes("* ")) {
    const bulletPoints = responseText
      .split("\n")
      .filter((line) => line.startsWith("* "));
    const ul = $('<ul class="bot-response-list"></ul>');
    bulletPoints.forEach((point) => {
      ul.append(`<li>${point.substring(2)}</li>`);
    });
    botMessage.append(ul);
  } else {
    botMessage.html(responseText.replace(/\n/g, "<br>"));
  }

  $("#chat-box").prepend(botMessage);
}

function handleError() {
  alert("Error occurred while processing your query.");
}

function clearInputField() {
  $("#user_input").val("");
}
