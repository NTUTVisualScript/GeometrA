var treeFile = "./workspace.json"

function FileTree() {
    this.update = function(tree) {
        $("#FileStructure").jstree({
            'core' : {
              'data' : tree}
          });
    };


    $('#FileStructure').on("changed.jstree", function (e, data) {
        console.log("The selected nodes are:");
        console.log(data.selected);
      });
}
