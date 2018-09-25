function NodeTree(){
    $("#dumpButton").on("click", function() {
        Get('/GeometrA/Node', function(data) {
            var tmp = $.jstree.reference("#Nodes");
            if(tmp)
                tmp.destroy();
            $("#Nodes").jstree({
                grid: {
                columns: [
                    {width:'30%', header: "Index"},
                    {width:'30%', header: "Name", value: "name"},
                    {width:'40%', header: "Bounds", value: 'bounds'}
                ],
                    width: document.getElementById('Nodes').width
                },
                'core': {
                    'check_callback': true,
                    'data': data,
                },
                'plugins':["core", "ui", "grid"]
            });

            document.getElementById("loader").style.display = "none";
        })
    });

    var widthMulti;
    var heightMulti;

    function getPos() {
        var screenElement = document.getElementById("ScreenCapture");
        var bound = (screenElement.getBoundingClientRect());
        // We should get real number instead of 1080x1920 as default.
        widthMulti = screenWidth/bound.width;
        heightMulti = screenHeight/bound.height;
    }

    $("#Nodes").on('changed.jstree', function (e, data) {
        getPos();
        var tree = $.jstree.reference(data.selected);
        var bounds = tree.get_node(data.selected).data.bounds;
        var coor = bounds.split('][');
        var coor_start = coor[0].substring(1, coor[0].length).split(',');
        var coor_end = coor[1].substring(0, coor[1].length-1).split(',');
        var x1 = parseInt(coor_start[0]) / widthMulti;
        var y1 = parseInt(coor_start[1]) / heightMulti;
        var x2 = parseInt(coor_end[0]) / widthMulti;
        var y2 = parseInt(coor_end[1]) / heightMulti;

        var canvas = document.getElementById('Screen');
        element = document.createElement('div');
        element.className = 'rectangle'
        element.style.left = x1 + 'px';
        element.style.top = y1 + 'px';
        element.style.width = x2 - x1;
        element.style.height = y2 - y1;
        canvas.removeChild(canvas.lastChild);
        canvas.appendChild(element);
        canvas.style.cursor = "crosshair";

        var data = {
            startX: x1 * widthMulti,
            startY: y1 * heightMulti,
            endX: x2 * widthMulti,
            endY: y2 * heightMulti
        }

        var actionImageList = ["Click", "Assert Exist", "Assert Not Exist"]
        
        if((Blockly.selected) && actionImageList.includes( Blockly.selected.getField().text_ )) {
            Post("/GeometrA/Screen/Crop", data, function(image){

                Get("/GeometrA/Screen/"+ image, function (data) {
                        Blockly.selected.update(data);
                        workspace.fireChangeListener(saveOnChange);   
                    })
                });
        }
    });
}
