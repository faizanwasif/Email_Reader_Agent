const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  startExtraction: () => ipcRenderer.invoke('start-extraction'),
  startAgent: () => ipcRenderer.invoke('start-agent'),
  onFlaskLog: (callback) => ipcRenderer.on('flask-log', (event, value) => callback(value)),
  onFlaskError: (callback) => ipcRenderer.on('flask-error', (event, value) => callback(value)),
  onAgentLog: (callback) => ipcRenderer.on('agent-log', (event, value) => callback(value)),
  onAgentError: (callback) => ipcRenderer.on('agent-error', (event, value) => callback(value)),
});