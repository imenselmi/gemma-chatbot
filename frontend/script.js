async function sendMessage() {
    const input = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const message = input.value;
    if (!message) return;

    chatbox.innerHTML += `<div class="message user">You: ${message}</div>`;
    input.value = "";

    const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await res.json();
    chatbox.innerHTML += `<div class="message bot">Bot: ${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
}
