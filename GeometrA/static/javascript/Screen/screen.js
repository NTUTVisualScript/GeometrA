function Screen(canvas) {
    var widthMulti;
    var heightMulti;
    this.screenWidth;
    this.screenHeight;

   function initScreenSize(data) {
       widthHeight = data.split("x");
       this.screenWidth = parseInt(widthHeight[0]);
       this.screenHeight = parseInt(widthHeight[1]);
   }

    (function init() {
        Get("/GeometrA/Screen/Size",function(data){
            initScreenSize(data);
        });
    })();
   
    function getPos() {
        var screenElement = document.getElementById("ScreenCapture");
        var bound = (screenElement.getBoundingClientRect());
        widthMulti = this.screenWidth/bound.width;
        heightMulti = this.screenHeight/bound.height;
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
                var actionImageList = ["Click", "Assert Exist", "Assert Not Exist"]
                if( (Blockly.selected) && actionImageList.includes( Blockly.selected.getField().text_ )) {
                    Blockly.selected.update(data);
                    workspace.fireChangeListener(saveOnChange);
                }
                else{
                    swal("You don't select an action that needs an image!");                }
            })
        });
    }
}
