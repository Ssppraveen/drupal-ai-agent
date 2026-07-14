const sendButton = document.getElementById("sendBtn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");

const API_URL = "http://127.0.0.1:8000/chat";

function addMessage(sender, text) {
  const message = document.createElement("div");
  message.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  message.appendChild(bubble);
  chatBox.appendChild(message);

  chatBox.scrollTop = chatBox.scrollHeight;
}

function addAIMessage(answer, citations) {
  const message = document.createElement("div");
  message.className = "message ai";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  bubble.innerHTML = `
        <div>${answer.replace(/\n/g, "<br>")}</div>

        <div class="sources">
            <strong>Sources</strong>
            <ul>
                ${citations.map((c) => `<li>${c.title}</li>`).join("")}
            </ul>
        </div>
    `;

  message.appendChild(bubble);

  chatBox.appendChild(message);

  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {
  const question = questionInput.value.trim();

  if (!question) return;

  addMessage("user", question);

  questionInput.value = "";

  addMessage("ai", "Thinking...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question: question,
      }),
    });

    const data = await response.json();

    chatBox.removeChild(chatBox.lastChild);

    addAIMessage(data.answer, data.citations);
  } catch (error) {
    chatBox.removeChild(chatBox.lastChild);

    addMessage("ai", "Unable to connect to the AI service.");

    console.error(error);
  }
}

sendButton.addEventListener("click", sendQuestion);

questionInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendQuestion();
  }
});
