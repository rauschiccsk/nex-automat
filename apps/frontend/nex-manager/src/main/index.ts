import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { readFileSync } from 'fs'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'

// ─── Runtime config ──────────────────────────────────────────────
interface AppConfig {
  apiUrl: string
}

function loadConfig(): AppConfig {
  const defaults: AppConfig = { apiUrl: 'http://localhost:9110' }
  const paths = [
    join(process.resourcesPath, 'config.json'),
    join(app.getAppPath(), 'resources', 'config.json')
  ]
  for (const p of paths) {
    try {
      const raw = readFileSync(p, 'utf-8')
      return { ...defaults, ...JSON.parse(raw) }
    } catch {
      // try next path
    }
  }
  return defaults
}

const config = loadConfig()

function createWindow(): void {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.icc.nex-manager')

  // Expose runtime config to renderer via IPC
  ipcMain.handle('get-config', () => config)

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
