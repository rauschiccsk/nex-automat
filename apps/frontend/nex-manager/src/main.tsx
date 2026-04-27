import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
// AG Grid v35 uses JS Theming API (theme={themeBalham} prop on AgGridReact).
// Legacy `ag-theme-balham.css` import is NOT needed and conflicts with the
// JS-built theme styles. Dark mode is wired via colorSchemeDark part inside
// BaseAgGrid (reactive to app-level Tailwind `dark` class).

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
