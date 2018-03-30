function ToolBar() {
    $("#runButton").on("click", function(){
        var nodes = $("#FileStructure").jstree("get_checked",true);
        var data = [];
        for (i = 0; i < nodes.length; ++i) {
            if(nodes[i].parents.length != 3){
                continue;
            }
            var path = $("#FileStructure").jstree().get_path(nodes[i]).join('/');
            data.push(path);
        }
        data = {
            cases: data.join(','),
        };
        Post('/GeometrA/TestScript/run', data, function(msg){
            if(msg=='success'){
                swal("Success!");
            }
        });
    });
}
