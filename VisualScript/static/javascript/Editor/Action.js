function mainDisabled(event) {
    console.log(event.type);
    console.log( workspace);
    if ( workspace.getBlockById(event.blockId) != null &&
        workspace.getBlockById(event.blockId).type == 'main') {
        if (event.type == 'create') {
            workspace.updateToolbox("<xml id='toolbox' style='display:none'> \
                <block type='main' disabled = 'true'></block> \
                <block type='sleep'></block> \
            </xml>")
        }
        else if (event.type == 'delete') {
            workspace.updateToolbox("<xml id='toolbox' style='display:none'> \
                <block type='main' disabled = 'false'></block> \
                <block type='sleep'></block> \
            </xml>")
        }
    }
};

workspace.addChangeListener(mainDisabled);

// Disabled the blocks don't attached to main.
workspace.addChangeListener(Blockly.Events.disableOrphans);

// function actionAdd(event) {
//     if (event.type == "change") {
//
//     }
// }
