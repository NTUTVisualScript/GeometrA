function Screen() {
    var widthMulti;
    var heightMulti;
    var canvas = document.getElementById('Screen');

    var actionImageList = ["Tap", "Assert Exist", "Assert Not Exist"];
    var actionArrowList = ["Swipe"];

    function getPos() {
        var screenElement = document.getElementById("ScreenCapture");
        var bound = (screenElement.getBoundingClientRect());
        widthMulti = screenWidth/bound.width;
        heightMulti = screenHeight/bound.height;
        return {x:bound.left, y: bound.top};
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
        if (element === null)
            return;
        if (document.getElementById("swipe-canvas")) {
            drawArrow();
        }
        else {
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            element.style.left = (mouse.x - mouse.startX <= 0) ? mouse.x + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY <= 0) ? mouse.y + 'px' : mouse.startY + 'px';
        }
    }

    canvas.onmousedown = function (e) {
        mouse.startX = mouse.x;
        mouse.startY = mouse.y;

        if ( (Blockly.selected) && actionArrowList.includes( Blockly.selected.getField().text_ ) ) {
            element = document.createElement('canvas');
            element.setAttribute('width', '500%');
            element.setAttribute('height', '500%');
            element.setAttribute('id', 'swipe-canvas');
        } else {
            element = document.createElement('div');
            element.className = 'rectangle'
            element.style.left = mouse.x + 'px';
            element.style.top = mouse.y + 'px';
        }

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
        if (document.getElementById("swipe-canvas")) {
            Blockly.selected.update(data);
        }
        else {
            Post("/GeometrA/Screen/Crop", data, function(image) {
                Get("/GeometrA/Screen/"+ image, function (data) {
                    if( (Blockly.selected) && actionImageList.includes( Blockly.selected.getField().text_ ) ) {
                        console.log(data);
                        Blockly.selected.update(data);
                        workspace.fireChangeListener(saveOnChange);
                    }
                    else{
                        swal("You don't select an action that needs an image!");
                    }
                })
            });
            Post("/GeometrA/Screen/Xpath", data, function(){

            });
        }
    }

    function drawArrow() {
        var canvas = document.getElementById('swipe-canvas');
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const PI = Math.PI;
        const headLength = 25;

        var screenElement = document.getElementById("ScreenCapture");
        var bound = (screenElement.getBoundingClientRect());

        var p1 = {x: 0, y: 0}, p0 = {x: 0, y: 0};
        p1.x = mouse.x/bound.width*500, p0.x = mouse.startX/bound.width*500;
        p1.y = mouse.y/bound.height*500, p0.y = mouse.startY/bound.height*500;
        // calc the angle of the line
        var dx = p1.x - p0.x;
        var dy = p1.y - p0.y;
        var angle = Math.atan2(-dy, -dx) * 180 / PI;
        var angle1 = (angle + 30) * PI / 180
        var angle2 = (angle - 30) * PI / 180
        // calc arrowhead points
        var x225 = p1.x + headLength * Math.cos(angle1);
        var y225 = p1.y + headLength * Math.sin(angle1);
        var x135 = p1.x + headLength * Math.cos(angle2);
        var y135 = p1.y + headLength * Math.sin(angle2);

        // draw line plus arrowhead
        ctx.beginPath();
        // draw the line from p0 to p1
        ctx.moveTo(p0.x, p0.y);
        ctx.lineTo(p1.x, p1.y);
        // draw partial arrowhead at 225 degrees
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(x225, y225);
        // draw partial arrowhead at 135 degrees
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(x135, y135);

        // set line color
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 5;
        // stroke the line and arrowhead
        ctx.stroke();
    }
}
