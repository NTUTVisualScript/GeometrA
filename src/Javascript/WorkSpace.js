var treeFile = "./workspace.json"

function FileTree() {
    this.update = function(files) {
        $("#FileStructure").jstree({
            'core' : {
              'data' : files}
          });
    }

    $('#FileStructure').on("changed.jstree", function (e, data) {
        console.log("The selected nodes are:");
        console.log(data.selected);
      });
}

// [
//   { "text" : "Project1", "children" : [
//       { "text" : "Suite1" , "children":[
//           {"text":"case1"},
//           {"text":"case2"}
//       ]},
//       { "text" : "Suite2" , "children": [
//           {"text":"case2"}
//       ]}
//     ]}
// ]
