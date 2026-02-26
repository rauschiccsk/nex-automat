import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { initApiConfig } from './lib/api'
import './index.css'

// Load runtime API URL from Electron config before rendering
initApiConfig().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
})
