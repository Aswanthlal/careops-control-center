const BASE = window.location.origin;

let currentConversation = null;

function loadConversations() {
    fetch(BASE + "/api/conversations/")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("conversationList");
            list.innerHTML = "";

            data.forEach(conv => {
                const div = document.createElement("div");
                div.className = "conversation-item";
                div.innerHTML = conv.contact;

                if (conv.alert) {
                    div.innerHTML += "<span class='alert-dot'> ⚠</span>";
                }

                div.onclick = () => loadMessages(conv.id);
                list.appendChild(div);
            });
        });
}

function loadMessages(convId) {
    currentConversation = convId;

    fetch(BASE + `/api/messages/${convId}/`)
        .then(res => res.json())
        .then(data => {
            const messagesDiv = document.getElementById("messages");
            messagesDiv.innerHTML = "";

            data.forEach(msg => {
                const div = document.createElement("div");
                div.className = "message";
                div.innerText = `${msg.sender}: ${msg.content}`;

                if (msg.content.includes("Low stock")) {
                    div.style.color = "red";
                }

                messagesDiv.appendChild(div);
            });
        });
}

function sendReply() {
    const input = document.getElementById("replyInput");

    fetch(BASE + "/api/send-reply/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            conversation_id: currentConversation,
            content: input.value
        })
    }).then(() => {
        input.value = "";
        loadMessages(currentConversation);
    });
}

loadConversations();
