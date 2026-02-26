import { ElectronAPI } from '@electron-toolkit/preload'

interface AppConfig {
  apiUrl: string
}

interface AppApi {
  config: {
    getConfig: () => Promise<AppConfig>
  }
}

declare global {
  interface Window {
    electron: ElectronAPI
    api: AppApi
  }
}
