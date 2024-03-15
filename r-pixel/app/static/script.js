var canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');

console.log(window.location.hostname);
const socket = new WebSocket(`ws://localhost:8765/r-pixel/app/template/`) // 172.31.181.197

//
// CANVAS STUFF
//

function setCanvasSize() {
    console.log("creating canvas")
    canvas.width = document.body.clientWidth;
    canvas.height = 1080;

    for (let x = 0.5; x < canvas.width; x += 10) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
    }

    for (let y = 0.5; y < canvas.height; y += 10) {
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
    }

    ctx.strokeStyle = "#d3d3d3";
    ctx.stroke();
}

function colorPicker(newColor) {
    console.log(newColor);
    ctx.fillStyle = `rgb(${newColor[0]}, ${newColor[1]}, ${newColor[2]})`
}

canvas.addEventListener("click", function (evt) {
    var mousePos = getMousePos(canvas, evt);

    drawPixel(mousePos.x, mousePos.y)
}, false);

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

function drawPixel(x, y) {
    x = Math.floor(x / 10) * 10;
    y = Math.floor(y / 10) * 10;
    ctx.fillRect(x, y, 10.25, 10.25);
    SendMessage(x, y)
}

//
// COMMUNICATION STUFF
// 

function connectToServer() {

    socket.onopen = function () {
        console.log("Status: Connected\n");
        
        var obj_to_send = {
            "cmd": "data",
        }
        socket.send(JSON.stringify(obj_to_send));
    };

    socket.onmessage = function (e) {
        console.log("Server: " + e.data + "\n");
        console.log(e.data);
        let data = JSON.parse(String(e.data));
        for (let i = 0; i < data.length; i++) {
            ctx.fillStyle = String(data[i]['color']);
            ctx.fillRect(data[i]['xCoord'], data[i]['yCoord'], 10.25, 10.25);
        }
        // drawPixel();
    };
}

function SendMessage(x, y) {

    var obj_to_send = {
        'cmd': 'pxl',
        'data':
        {
            'timeMS': Date.now(),
            'xCoord': parseInt(x),
            'yCoord': parseInt(y),
            'color': ctx.fillStyle,
        },
    }

    // console.log(obj_to_send);
    socket.send(JSON.stringify(obj_to_send));
}

//
// STARTUP STUFF
//

function startUp() {
    connectToServer();
    setCanvasSize();
    requestAccess();
}

function requestAccess() {

    var video = document.createElement('video');
    video.setAttribute('playsinline', '');
    video.setAttribute('autoplay', '');
    video.setAttribute('muted', '');
    video.style.width = '200px';
    video.style.height = '200px';

    /* Setting up the constraint */
    var facingMode = "user"; // Can be 'user' or 'environment' to access back or front camera (NEAT!)
    var constraints = {
        audio: false,
        video: {
            facingMode: facingMode
        }
    };

    /* Stream it to video element */
    navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
        video.srcObject = stream;
    });
}

window.onload = startUp;

// zur synchronisation vom canvas websockets verwendetn

// der ebnutzer setzt ein pixel -> das geht an den server weiter
// -> der schaut ob eh die 5 minuten vergangen sind -> wenn ja pixel setzen & speichern ->
// andere benutzer benachrichtigen das ein pixel gesetzt wurde und die information
// auch an diese benutzer schicken

// also ein websocket pro benutzer der immer zum server offen ist