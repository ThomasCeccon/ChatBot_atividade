const userId = Date.now();

function sendMessage() {
    const message = document.getElementById('userInput').value.trim();
    const sendButton = document.getElementById('sendButton');
    const errorElement = document.getElementById('error');

    if (message === "") {
        errorElement.style.display = 'block';
        sendButton.style.backgroundColor = 'red';
        return;
    } else {
        errorElement.style.display = 'none';
        sendButton.style.backgroundColor = '#007bff';
    }
    
    if (message.includes("obrigado")) {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<p class="user-message"><strong>Você:</strong> ${message}</p>`;
        messagesDiv.innerHTML += `<p class="bot-message"><strong>Bot:</strong> De nada! Se precisar de mais alguma coisa, estarei aqui. Tenha um ótimo dia!</p>`;
        
        document.getElementById('userInput').disabled = true;
        sendButton.disabled = true;
        sendButton.style.backgroundColor = '#ccc';
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        return;
    }

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message, user_id: userId }),
    })
    .then(response => response.json())
    .then(data => {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<div class="message user"><strong>Você:</strong> ${message}</div>`;
        messagesDiv.innerHTML += `<div class="message bot"><strong>Bot:</strong> ${data.response}</div>`;
        document.getElementById('userInput').value = '';
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

window.onload = function() {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'start', user_id: userId }),
    })
    .then(response => response.json())
    .then(data => {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<div class="message bot"><strong>Bot:</strong> ${data.response}</div>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
};
