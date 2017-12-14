import FileTree from './WorkSpace'

function ToolBar() {
    $('#load').click(function(){
        FileTree.update()
    });
}
