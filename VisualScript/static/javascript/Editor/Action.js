function onChange(event) {
    console.log(event.type);
    console.log(workspace);
    console.log(workspace.getBlockById(event.blockId));
    console.log(event.group);
    var block = workspace.getBlockById(event.blockId);
    if (block != null && block.type == 'main') {
        if (event.type == 'create') {
            block.disabled = true;
            console.log("HIHIHI");
        }
        else if (event.type == 'delete') {
            block.disabled = false;
        }
    }

}

workspace.addChangeListener(onChange);
