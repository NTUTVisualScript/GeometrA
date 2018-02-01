function WorkSpace() {
    Get("/VisualScript/WorkSpace", function(response) {
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
              'three_state' : false, // to avoid that fact that checking a node also check others
              'whole_node' : false,  // to avoid checking the box just clicking the node
              'tie_selection' : false, // for checking without selecting and selecting without checking
              'cascade' : "down"
            },
            'contextmenu': {
                show_at_node: true,
                items: Menu,
            },
            'plugins':["contextmenu", "checkbox", "types"]
        });

        Get('/VisualScript/saveLog', function(result) {
            if (result == 'Fail')
                alert("Saving Log File Failed");
        });
    });
};

function Menu(node) {
    console.log(node)
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
    inst.create_node(obj, {}, "last", function (new_node) {
        new_node.text = "New Suite"
        try {
            inst.edit(new_node, null, function (node) {
                var data = {
                    Project: obj["text"],
                    Suite: node["text"],
                };
                Post("/VisualScript/WorkSpace/addSuite", data, function() {});
            });
        } catch (ex) {
            console.log(ex);
            setTimeout(function () { inst.edit(new_node); }, 0);
        }
    });
}

function createCase(inst, obj) {
    inst.create_node(obj, {}, "last", function (new_node) {
        new_node.icon = 'jstree-file'
        new_node.type = "itsfile"
        new_node.text = "New Case"

        try {
            inst.edit(new_node, null, function (node) {
                var data = {
                    Project: inst.get_node(obj["parent"])["text"],
                    Suite: obj["text"],
                    Case: node["text"],
                };
                Post("/VisualScript/WorkSpace/addCase", data, function() {});
            });
        } catch (ex) {
            console.log(ex);
            setTimeout(function () { inst.edit(new_node); }, 0);
        }
    });
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
    Post("/VisualScript/WorkSpace/delete", data, function(msg) {
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
    inst.edit(obj, null, function(node) {
        data["new"] = node["text"]
        Post('/VisualScript/WorkSpace/rename', data, function() {});
    });
}
