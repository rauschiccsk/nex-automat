import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
// AG Grid balham theme — compact NEX Genesis-like layout with floating filters
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-balham.css'
// Dark-mode overrides scoped under :root.dark .ag-theme-balham
import './components/grids/agGridDarkMode.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
