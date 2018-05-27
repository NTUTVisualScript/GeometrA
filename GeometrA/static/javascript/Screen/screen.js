initDraw(document.getElementById('Screen'));

function initDraw(canvas) {
    var widthMulti;
    var heightMulti;

    function getPos() {
        var screenElement = document.getElementById("ScreenCapture");
        var bound = (screenElement.getBoundingClientRect());
        // We should get real number instead of 1080x1920 as default.
        widthMulti = 1080/bound.width;
        heightMulti = 1920/bound.height;
        return {x:bound.x, y: bound.y};
    }

    var pos = getPos();
    function setMousePosition(e) {
        pos = getPos();
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX - pos.x;
            mouse.y = ev.pageY - pos.y;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX + document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    };


    var mouse = {
        x: 0,
        y: 0,
        startX: 0,
        startY: 0
    };
    var element = null;

    canvas.onmousemove = function (e) {
        setMousePosition(e);

        if (element !== null) {
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            element.style.left = (mouse.x - mouse.startX <= 0) ? mouse.x + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY <= 0) ? mouse.y + 'px' : mouse.startY + 'px';
        }
    }

    canvas.onmousedown = function (e) {
        mouse.startX = mouse.x;
        mouse.startY = mouse.y;
        element = document.createElement('div');
        element.className = 'rectangle'
        element.style.left = mouse.x + 'px';
        element.style.top = mouse.y + 'px';
        canvas.removeChild(canvas.lastChild);
        canvas.appendChild(element);
        canvas.style.cursor = "crosshair";
    }
    canvas.onmouseup = function (e) {
        element = null;
        canvas.style.cursor = "default";
        var data = {
            startX: mouse.startX * widthMulti,
            startY: mouse.startY * heightMulti,
            endX: mouse.x * widthMulti,
            endY: mouse.y * heightMulti
        }
        Post("/GeometrA/Screen/Crop", data, function(image){

            Get("/GeometrA/Screen/"+ image, function (data) {
                Blockly.selected.update(data);
                workspace.fireChangeListener(saveOnChange);
            })
        });
    }
}
