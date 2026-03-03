import { app, shell, BrowserWindow, ipcMain, screen } from 'electron'
import { join } from 'path'
import { readFileSync } from 'fs'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import Store from 'electron-store'

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

// ─── Window state persistence ────────────────────────────────────
interface WindowState {
  width: number
  height: number
  x: number | undefined
  y: number | undefined
  maximized: boolean
}

const windowStore = new Store<{ windowState: WindowState }>({
  name: 'nex-manager-window-state',
  defaults: {
    windowState: {
      width: 1280,
      height: 800,
      x: undefined,
      y: undefined,
      maximized: false
    }
  }
})

/** Check if position is visible on any connected display */
function isPositionOnScreen(x: number, y: number): boolean {
  const displays = screen.getAllDisplays()
  return displays.some((display) => {
    const { x: dx, y: dy, width: dw, height: dh } = display.bounds
    return x >= dx && y >= dy && x < dx + dw && y < dy + dh
  })
}

function createWindow(): void {
  const saved = windowStore.get('windowState')
  let { x, y, width, height, maximized } = saved

  // Validate saved position — reset if off-screen
  if (x !== undefined && y !== undefined) {
    if (!isPositionOnScreen(x, y)) {
      x = undefined
      y = undefined
    }
  }

  const mainWindow = new BrowserWindow({
    width,
    height,
    ...(x !== undefined && y !== undefined ? { x, y } : {}),
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  // Restore maximized state after window creation
  if (maximized) {
    mainWindow.maximize()
  }

  // ─── Save window state (debounced 500ms) ─────────────────────
  let saveTimeout: ReturnType<typeof setTimeout> | null = null
  const saveState = (): void => {
    if (saveTimeout) clearTimeout(saveTimeout)
    saveTimeout = setTimeout(() => {
      if (!mainWindow.isDestroyed() && !mainWindow.isMaximized()) {
        const bounds = mainWindow.getBounds()
        windowStore.set('windowState', {
          ...bounds,
          maximized: false
        })
      }
    }, 500)
  }

  mainWindow.on('resize', saveState)
  mainWindow.on('move', saveState)
  mainWindow.on('maximize', () => windowStore.set('windowState.maximized', true))
  mainWindow.on('unmaximize', () => {
    windowStore.set('windowState.maximized', false)
    saveState()
  })

  // Save final state on close
  mainWindow.on('close', () => {
    if (saveTimeout) clearTimeout(saveTimeout)
    if (!mainWindow.isMaximized()) {
      const bounds = mainWindow.getBounds()
      windowStore.set('windowState', { ...bounds, maximized: false })
    } else {
      windowStore.set('windowState.maximized', true)
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
