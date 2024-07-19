document.addEventListener('DOMContentLoaded', () => {
    const groupName = JSON.parse(document.getElementById('groupName').textContent);
    console.log(groupName)
    const currentUser = JSON.parse(document.getElementById('currentUser').textContent);
    console.log(currentUser)
    const chatWindow = document.getElementById('chat-window');

    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/group/${groupName}/`)
    chatSocket.onopen = function (e) {
        console.log('Connect Sucessfully.')
    }

    chatSocket.onclose = function (e) {
        console.log('Connection unexpectedly closed.');
        setTimeout(function () {
            console.log('Reconnecting....');
            connect()
        }, 10000)

    }

    chatSocket.onerror = function (e) {
        console.log('Web socket encountered an error: ' + e);
        console.log('Closing connection.');
        chatSocket.close();
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case 'chat_message':
                displayMessage(currentUser, data.user, data.message)

            default:
                break;
        }
    }


    function displayMessage(currentUser, username, message) {
        const isSender = username === currentUser
        const newMsg = document.createElement('div');
        newMsg.classList.add('message', isSender ? 'sent' : 'received');

        if (!isSender) {
            const usernameLable = document.createElement('p');
            usernameLable.classList.add('username');
            usernameLable.textContent = username;
            newMsg.appendChild(usernameLable);
        }

        const msgContent = document.createElement('p');
        msgContent.textContent = message;
        newMsg.appendChild(msgContent)

        chatWindow.appendChild(newMsg)
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }



    document.getElementById('chat-message-input').focus();
    document.getElementById('chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {
            document.getElementById('chat-message-submit').click();
        }
    }

    document.getElementById('chat-message-submit').onclick = function (e) {
        e.preventDefault()
        const messageDOM = document.getElementById('chat-message-input');
        chatSocket.send(JSON.stringify({
            'message': messageDOM.value
        }));

        messageDOM.value = '';
    }

})
