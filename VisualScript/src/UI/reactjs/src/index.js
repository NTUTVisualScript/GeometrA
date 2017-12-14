import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';

//Doms
import FileStructure from './Doms/FileStructure'
import TabList from './Doms/TabList'
import ActionList from './Doms/ActionList'
import TestSteps from './Doms/TestSteps'
import Nodes from './Doms/Nodes'
import MessageList from './Doms/MessageList'

ReactDOM.render(<FileStructure />, document.getElementById('FileStructure'));
ReactDOM.render(<TabList />, document.getElementById('TabList'));
ReactDOM.render(<ActionList />, document.getElementById('ActionList'));
ReactDOM.render(<TestSteps />, document.getElementById('TestSteps'));
ReactDOM.render(<Nodes />, document.getElementById('Nodes'));
ReactDOM.render(<MessageList />, document.getElementById('MessageList'));


//ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
