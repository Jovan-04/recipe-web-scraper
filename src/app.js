const { app, BrowserWindow } = require('electron')

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'
process.env['ELECTRON_ENABLE_LOGGING'] = 1


function createWindow () {
  const win = new BrowserWindow({
    width: 1000,
    minWidth: 800,
    height: 600,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      backgroundThrottling: false // Keep 'false' (Performance drops when window is minimized)
    },
    // titleBarStyle: 'hidden',
    // titleBarOverlay: {
    //   color: '#2f3241',
    //   symbolColor: '#74b1be',
    //   height: 15
    // }
  })

  win.removeMenu()
  // win.webContents.openDevTools()
  win.loadFile('index.html')

  return
}



app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})