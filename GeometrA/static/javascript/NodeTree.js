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
}
