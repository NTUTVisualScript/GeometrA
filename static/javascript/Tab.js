const TabGroup = require('electron-tabs')
var tabGroup = new TabGroup();

tabGroup.on("tab-active", (tab, tabGroup) => {
    data = JSON.parse(tab.badge)
    Post('/GeometrA/WorkSpace/open', data, function(xml){
        openTestCase(xml);
    });
    Post('/GeometrA/WorkSpace/Focus', data, function(msg) {});
});

tabGroup.on("tab-removed", (tab, tabGroup) => {
    tabs = tabGroup.getTabs()
    if (tabs.length == 0) {
        Blockly.mainWorkspace.clear();
    }
});

var Tab = {
    createTab: function(data) {
        dataString = JSON.stringify(data)
        tabGroup.addTab({
            title: data["Case"],
            badge: dataString,
            visible: true,
            active: true
        })
    },
    checkTabExist: function(data) {
        checkString = JSON.stringify(data)
        tabs = tabGroup.getTabs()
        if (tabs != null){
            for (var i=0; i< tabs.length; i++) {
                if(tabs[i].badge == checkString) {
                    tabs[i].activate()
                    return true
                }
            }
        }
        return false
    }
}
