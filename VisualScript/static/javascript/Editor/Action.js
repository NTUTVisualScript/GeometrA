function mainDisabled(event) {
    console.log(event.type);
    console.log( workspace);
    if ( workspace.getBlockById(event.blockId) != null &&
        workspace.getBlockById(event.blockId).type == 'main') {
        if (event.type == 'create') {
            // workspace.flyout_.workspace_.topBlocks_[0].element = true;
            new Blockly.Events.BlockChange(workspace.flyout_.workspace_.topBlocks_[0], "disabled", "Used", false, true);
        }
        else if (event.type == 'delete') {
            // workspace.flyout_.workspace_.topBlocks_[0].element['disabled'] = false;
            new Blockly.Events.BlockChange(workspace.flyout_.workspace_.topBlocks_[0], "disabled", "unUsed", true, false);
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
