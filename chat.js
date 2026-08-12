(function (Drupal, once) {
  Drupal.behaviors.drupalAiChat = {
    attach: function (context) {
      once("drupal-ai-chat", "body", context).forEach(function () {
        const chatButton = document.createElement("button");
        chatButton.id = "drupal-ai-chat-button";
        chatButton.innerHTML = "💬";
        chatButton.setAttribute("aria-label", "Open AI Chat");

        const chatWindow = document.createElement("div");
        chatWindow.id = "drupal-ai-chat-window";

        chatWindow.innerHTML = `
          <div class="drupal-ai-chat-header">

            <div class="drupal-ai-chat-title">
              <span class="drupal-ai-chat-icon">🤖</span>
              <span>AI Assistant</span>
            </div>

            <button
              id="drupal-ai-chat-close"
              aria-label="Close chat">
              ×
            </button>

          </div>

          <div id="drupal-ai-chat-messages">

            <div class="drupal-ai-message bot">
              Hello! 👋<br>
              How can I help you?
            </div>

          </div>

          <div class="drupal-ai-chat-input-area">

            <input
              type="text"
              id="drupal-ai-chat-input"
              placeholder="Ask something..."
              autocomplete="off"
            />

            <button
              id="drupal-ai-chat-send"
              aria-label="Send message">
              ➤
            </button>

          </div>
        `;

        document.body.appendChild(chatButton);
        document.body.appendChild(chatWindow);

        const closeButton = document.getElementById("drupal-ai-chat-close");

        const input = document.getElementById("drupal-ai-chat-input");

        const sendButton = document.getElementById("drupal-ai-chat-send");

        const messages = document.getElementById("drupal-ai-chat-messages");

        chatButton.addEventListener("click", function () {
          chatWindow.classList.add("open");

          setTimeout(function () {
            input.focus();
          }, 200);
        });

        closeButton.addEventListener("click", function () {
          chatWindow.classList.remove("open");
        });

        function addUserMessage(text) {
          const message = document.createElement("div");

          message.className = "drupal-ai-message user";

          message.textContent = text;

          messages.appendChild(message);

          messages.scrollTop = messages.scrollHeight;
        }

        function addBotMessage(text) {
          const message = document.createElement("div");

          message.className = "drupal-ai-message bot";

          message.textContent = text;

          messages.appendChild(message);

          messages.scrollTop = messages.scrollHeight;
        }

        function addLoadingMessage() {
          const message = document.createElement("div");

          message.className = "drupal-ai-message bot drupal-ai-loading";

          message.textContent = "Thinking...";

          messages.appendChild(message);

          messages.scrollTop = messages.scrollHeight;

          return message;
        }

        async function sendMessage() {
          const text = input.value.trim();

          if (!text) {
            return;
          }

          addUserMessage(text);

          input.value = "";

          sendButton.disabled = true;
          input.disabled = true;

          const loadingMessage = addLoadingMessage();

          try {
            const response = await fetch("http://127.0.0.1:8000/chat", {
              method: "POST",

              headers: {
                "Content-Type": "application/json",
              },

              body: JSON.stringify({
                question: text,
              }),
            });

            if (!response.ok) {
              throw new Error("FastAPI returned HTTP " + response.status);
            }

            const data = await response.json();

            loadingMessage.remove();

            addBotMessage(data.answer || "I couldn't generate an answer.");
          } catch (error) {
            console.error("Drupal AI Chat error:", error);

            loadingMessage.remove();

            addBotMessage(
              "Sorry, I couldn't connect to the AI service. Please try again.",
            );
          } finally {
            sendButton.disabled = false;
            input.disabled = false;

            input.focus();
          }
        }

        sendButton.addEventListener("click", sendMessage);

        input.addEventListener("keydown", function (event) {
          if (event.key === "Enter") {
            event.preventDefault();

            sendMessage();
          }
        });
      });
    },
  };
})(Drupal, once);
