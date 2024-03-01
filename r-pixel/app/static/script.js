var canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');

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
}



window.onload = setCanvasSize;

// zur synchronisation vom canvas websockets verwendetn 

// der ebnutzer setzt ein pixel -> das geht an den server weiter
// -> der schaut ob eh die 5 minuten vergangen sind -> wenn ja pixel setzen & speichern ->
// andere benutzer benachrichtigen das ein pixel gesetzt wurde und die information 
// auch an diese benutzer schicken

// also ein websocket pro benutzer der immer zum server offen ist