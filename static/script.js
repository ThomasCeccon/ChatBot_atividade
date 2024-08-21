  // Gerar um identificador único para o usuário
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
          messagesDiv.innerHTML += `<p><strong>Você:</strong> ${message}</p>`;
          messagesDiv.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
          document.getElementById('userInput').value = '';
          messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom
      });
  }

  // Enviar mensagem inicial quando a página carregar
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
          messagesDiv.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
          messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom
      });
  };