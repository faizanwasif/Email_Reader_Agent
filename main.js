const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
    },
  });

  mainWindow.loadFile('renderer/index.html');
}

app.whenReady().then(() => {
  createWindow();
  startFlaskServer();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

function startFlaskServer() {
  flaskProcess = spawn('python', ['src/email_extraction.py']);
  
}

ipcMain.handle('start-extraction', async () => {
  shell.openExternal('http://127.0.0.1:5000/start-extraction');
});

ipcMain.handle('start-agent', async () => {
  const pythonProcess = spawn('python', ['src/run_agent.py']);
  let output = '';
  
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
    mainWindow.webContents.send('agent-log', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Agent Error: ${data}`);
    mainWindow.webContents.send('agent-error', data.toString());
  });

  return new Promise((resolve) => {
    pythonProcess.on('close', (code) => {
      resolve({ code, output });
    });
  });
});