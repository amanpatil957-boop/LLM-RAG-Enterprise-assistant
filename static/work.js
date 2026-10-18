
const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const messages = document.getElementById("messages");
const sources = document.getElementById("sources");
const sendButton = document.getElementById("sendButton");

function addMessage(role, label, content) {
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const messageLabel = document.createElement("div");
    messageLabel.className = "message-label";
    messageLabel.textContent = label;

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.textContent = content;

    message.appendChild(messageLabel);
    message.appendChild(messageContent);
    messages.appendChild(message);

    return messageContent;
}

async function askQuestion(question) {
    question = question.trim();
    if (!question || sendButton.disabled) return;

    addMessage("user", "You", question);

    questionInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";
    sources.textContent = "Searching documents...";

    const answerContent = addMessage(
        "assistant",
        "AI Assistant",
        "Generating answer..."
    );

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || `Request failed: ${response.status}`
            );
        }

        answerContent.textContent =
            data.answer || data.response || "No answer returned.";

        sources.replaceChildren();

        const sourceList = document.createElement("ul");
        const uniqueSources = [
            ...new Set(
                (data.sources || data.documents || []).map(source =>
                    typeof source === "string"
                        ? source
                        : source.source ||
                          source.filename ||
                          source.file_name ||
                          source.name
                ).filter(Boolean)
            )
        ];

        if (uniqueSources.length === 0) {
            sources.textContent = "No sources returned.";
        } else {
            uniqueSources.forEach(source => {
                const item = document.createElement("li");
                item.textContent = source;
                sourceList.appendChild(item);
            });

            sources.appendChild(sourceList);
        }
    } catch (error) {
        answerContent.textContent = "Unable to get an answer: " + error.message;
        sources.textContent = "Please check the backend terminal for errors.";
        console.error("Ask AI failed:", error);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Ask AI";
    }
}

questionForm.addEventListener("submit", event => {
    event.preventDefault();
    askQuestion(questionInput.value);
});

function askSuggested(question) {
    questionInput.value = question;
    askQuestion(question);
}
