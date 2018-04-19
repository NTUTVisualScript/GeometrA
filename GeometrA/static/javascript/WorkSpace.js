function WorkSpace() {
    Get("/GeometrA/WorkSpace", function(response) {
        $("#FileStructure").jstree({
            'types': {
                'itsfile': {
                    'icon': 'jstree-file',
                },
            },
            'core': {
                'check_callback': true,
                'data': response
            },
            'checkbox': {
              'three_state' : true, // to avoid that fact that checking a node also check others
              'whole_node' : false,  // to avoid checking the box just clicking the node
              'tie_selection' : false, // for checking without selecting and selecting without checking
              'cascade' : "down",
            },
            'contextmenu': {
                show_at_node: true,
                items: Menu,
            },
            'plugins':["contextmenu", "checkbox", "types"]
        });

        //open the case whne double click testcase
        $("#FileStructure").on("dblclick.jstree",'.jstree-anchor', function(event){
            var tree = $.jstree.reference(this);
            var node = tree.get_node(this);
            var nodePath = tree.get_path(node).join("/");
            var caseInfo = nodePath.split("/");
            if(caseInfo.length != 3)
                return;
            var data = {
                Project: caseInfo[0],
                Suite: caseInfo[1],
                Case: caseInfo[2]
            }
            //Create Tab when double click a case
            Tab(data);
            if(!Tab.checkTab()) {
                Post('/GeometrA/WorkSpace/open', data, function(xml){
                    openTestCase(xml);
                });
                Tab.createTab();
                Tab.selectTab();
            } else {
                Tab.selectTab();
            }
        });

        Get('/GeometrA/saveLog', function(result) {
            if (result == 'Fail')
                alert("Saving Log File Failed");
        });
    });
};

function Tab(data){
    var index = -1;
    function createTab() {
        var _data = JSON.stringify(data);
        var num_tabs = $("div#tabs ul li").length + 1;

        $("div#tabs ul").append(
            "<li id='"+ _data + "'>" + "<a href='#tab" + num_tabs + "'>" + data['Case'] +
            "<p id='d_tab" + num_tabs + "' style='display:none;'>" + _data + "</p>" +
            "</a>"+"<span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span>"+"</li>"
        );

        $("div#tabs").append(
            "<div id='tab" + num_tabs + "'></div>"
        );

        $("div#tabs").tabs("refresh");
    };
    function checkTab(){
        var path = data.Project + '/' + data.Suite + '/' + data.Case;
        var numberOfList = $("div#tabs ul li").length + 1;
        var check = false;
        $("ul#ul_tabs li").each(function(){
            var _data = $(this).attr("id");
            console.log(_data);
            if(data == _data){
                check = true;

            }else{
                check = false;
            }

        });
        // for( index=1; index < numberOfList; ++index){
        //     var target = $("ul#ul_tabs li").first();
        //     console.log(target);
        //     var id = $(target).attr("id");
        //     if(!_data){
        //         continue;
        //     }
        //     var _data = JSON.parse(id);
        //     console.log(_data);
        //     var checkPath = _data.Project + '/' + _data.Suite + '/' + _data.Case;
        //     if(_data == data){
        //         return true;
        //     }
        //     target = $("ul#ul_tabs li").next();
        // }
        return check;
    };
    function selectTab () {
        $("#tabs").tabs({active: index-1});
        Post('/GeometrA/WorkSpace/Focus', data, function(msg) {});
    };
    Tab.createTab = createTab;
    Tab.checkTab = checkTab;
    Tab.selectTab = selectTab;
};

function Menu(node) {
    var items = {
        CreateItem: {
            label: "Create",
            action: function(data) {
                var inst = $.jstree.reference(data.reference);
                var obj = inst.get_node(data.reference);
                if (obj["parents"].length == 1) {
                    createSuite(inst, obj);
                }
                else {
                    createCase(inst, obj);
                }
            },
        },
        DeleteItem: {
            label: "Delete",
            action: function(data) {
                var inst = $.jstree.reference(data.reference);
                var obj = inst.get_node(data.reference);
                swal({
                    title: 'Deletion',
                    text: "Are you sure to delete: " + obj["text"],
                    type: 'info',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Delete',
                    cancelButtonText: 'Cancel',
                    buttonsStyling: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                }).then((result) => {
                    if (result.value) {
                    FileDelete(inst, obj);
                    }
                })
            },
        },
        RenameItem: {
            label: "Rename",
            action: function(data) {
                var inst = $.jstree.reference(data.reference);
                var obj = inst.get_node(data.reference);

                Rename(inst, obj);

            },
        }
    };

    if (node["parents"].length >= 3) {
        delete items.CreateItem;
    }
    return items;
}

function createSuite(inst, obj) {
    var data = {
        Project: obj["text"],
    };
    Post ('/GeometrA/WorkSpace/addSuite', data, function(suite_name) {
        inst.create_node(obj, {}, "last", function (new_node) {
            new_node.text = suite_name
            Rename(inst, new_node)
        });
    });
}

function createCase(inst, obj) {
    var data = {
        Project: inst.get_node(obj["parent"])["text"],
        Suite: obj["text"],
    };
    Post('/GeometrA/WorkSpace/addCase', data, function(case_name) {
        inst.create_node(obj, {}, "last", function (new_node) {
            new_node.icon = 'jstree-file';
            new_node.type = "itsfile";
            new_node.text = case_name;

            Rename(inst, new_node);
        });
    });
}

function checkName (inst, obj, name) {
    children_id = inst.get_node(obj.parent).children
    for (var i = 0; i < children_id.length; i++) {
        inst.get_node()
    }
}

function FileDelete(inst, obj) {
    if (obj["parents"].length == 1) {
        var data = {
            Project: obj["text"],
        };
    }
    else if (obj["parents"].length == 2) {
        var data = {
            Project: inst.get_node(obj["parent"])["text"],
            Suite: obj["text"],
        };
    }
    else {
        var data = {
            Project: inst.get_node(inst.get_node(obj["parent"])["parent"])["text"],
            Suite: inst.get_node(obj["parent"])["text"],
            Case: obj["text"],
        };
    }
    Post("/GeometrA/WorkSpace/delete", data, function(msg) {
        inst.delete_node(obj)
    });
}

function Rename(inst, obj) {
    if (obj["parents"].length == 1) {
        var data = {
            Project: obj["text"],
            new:"",
        };
    }
    else if (obj["parents"].length == 2) {
        var data = {
            Project: inst.get_node(obj["parent"])["text"],
            Suite: obj["text"],
            new:"",
        };
    }
    else {
        var data = {
            Project: inst.get_node(inst.get_node(obj["parent"])["parent"])["text"],
            Suite: inst.get_node(obj["parent"])["text"],
            Case: obj["text"],
            new:"",
        };
    }
    old_name = obj.text
    inst.edit(obj, null, function(node) {
        data["new"] = node["text"]
        Post('/GeometrA/WorkSpace/rename', data, function(msg) {
            if (msg != '') {
                swal("The name: '" + msg + "' has been used!\n \
                    Please Rename it. " + old_name).then(function () {
                        node.text = old_name;
                        Rename(inst, node);
                    });
            }
        });
    });
}
