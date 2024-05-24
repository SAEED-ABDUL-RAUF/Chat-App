
const groupName = JSON.parse(document.getElementById('groupName').textContent)
let chatSocket = null
function connect() {
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/group/${groupName}/`)
    chatSocket.onopen = function(e){
        console.log('Connect Sucessfully.')
    }

    chatSocket.onclose = function(e){
        console.log('Connection unexpectedly closed.');
        setTimeout(function(){
            console.log('Reconnecting....');
            connect()
        }, 10000)

    }

    chatSocket.onerror = function(e) {
        console.log('Web socket encountered an error: ' + e);
        console.log('Closing connection.');
        chatSocket.close();
    }

    chatSocket.onmessage = function(e){
        data = JSON.parse(e.data);
        console.log(data);
        document.getElementById('chat-log').innerHTML += data.message + '<br>'
    }
}

connect()



document.getElementById('chat-message-input').focus();
document.getElementById('chat-message-input').onkeyup = function(e){
    if (e.keyCode === 13) {
        document.getElementById('chat-message-submit').click();
    }
}

document.getElementById('chat-message-submit').onclick = function(e) {
        const messageDOM = document.getElementById('chat-message-input');
        chatSocket.send(JSON.stringify({
            'message':messageDOM.value
        }));

        messageDOM.value = '';
}
