const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const production = true
const { dialog } = require('electron')
const rq = require('request-promise')
const fixPath = require('fix-path');

fixPath();

let pyProc = null
let pyPort = null

let mainWindow = null
const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1920, height: 1080})
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'static/index.html'),
    protocol: 'file:',
    slashes: true
  }))
  if (!production) mainWindow.webContents.openDevTools()
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

const mainAddr = 'http://localhost:5000'
const startUp = () => {
  rq(mainAddr)
    .then(function(htmlString) {
      console.log('server started!');
      createWindow();
    })
    .catch(function(err) {
      console.log('waiting for the server start...');
      startUp();
    });
}
app.on('ready', startUp)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
app.on('activate', () => {
  if (mainWindow === null) {
    startUp()
  }
})

const selectPort = () => {
  pyPort = 5000
  return pyPort
}

const PY_DIST_FOLDER = 'pydist'
const PY_FOLDER = 'main'
const PY_MODULE = 'main' // without .py suffix

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return PY_MODULE + '.py'
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const createPyProc = () => {
  let port = '' + selectPort()
  let script = getScriptPath()
  if (guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
  } else {
    if (process.platform === 'win32') {
      pyProc = require('child_process').spawn('py', [script])
    } else {
      pyProc = require('child_process').spawn('python', [script])
    }
  }

  if (pyProc != null) {
    //console.log(pyProc)
    console.log('child process success on port ' + port)
  }
}
const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)

exports.selectDirectory = function(callback) {
  dialog.showOpenDialog(
      mainWindow, {properties: ['openDirectory'], multiSelections: false},
      callback);
}

exports.selectProject = function(callback) {
  const dialogOption = {
    filters: [
      {name: 'Test Project', extensions: ['json']},
    ],
    properties: ['openFile'],
    multiSelections: false
  };
  dialog.showOpenDialog(mainWindow, dialogOption, callback);
}

var screenProcess = null;

const RESOURCE_FOLDER = 'resources'
const SCRCPY_RESOURCE_FOLDER = 'scrcpy-resources'
const ADB_RESOURCE_FOLDER = 'adb_resources'
const SCRCPY_BIN = 'scrcpy'
const getScrcpyPath = () => {
  if (process.platform === 'darwin') {
    return path.join(__dirname, RESOURCE_FOLDER, SCRCPY_RESOURCE_FOLDER, 'mac', SCRCPY_BIN)
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, SCRCPY_BIN + '.exe')
  }
  return 'scrcpy'
}

exports.startLive = function() {
  if (screenProcess !== null) {
    screenProcess.kill('SIGINT');
  }
  const script = getScrcpyPath();
  if (script === 'scrcpy' ) {
    return 
  } else if (process.platform === 'win32') {
    screenProcess = require('child_process').spawn(script);
  } else {
    screenProcess = require('child_process').execFile(script);
  }
  screenProcess.on('error', function (err) {
    console.log('scrcpy not installed');
  });
}

exports.endLive = function() {
  if (screenProcess === null)
    return;
  screenProcess.kill('SIGINT');
  screenProcess = null;
}
