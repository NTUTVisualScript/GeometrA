var treeFile = "./workspace.json"

function WorkSpace() {
    this.update = function() {
        $("#FileStructure").jstree({
            'core' : {
              'data' : [
                { "text" : "Project1", "children" : [
                    { "text" : "Suite1" , "children":[
                        {"text":"case1"},
                        {"text":"case2"}
                    ]},
                    { "text" : "Suite2" , "children": [
                        {"text":"case2"}
                    ]}
                  ]}
              ]}
          });
    };


    $('#FileStructure').on("changed.jstree", function (e, data) {
        console.log("The selected nodes are:");
        console.log(data.selected);
      });
}
