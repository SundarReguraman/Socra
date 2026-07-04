import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowseRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Session from './pages/Session'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
    <Routes>
      <Route path = "/" elements = {<Home />} />
      <Route path = "/session/:id" element = {<Session />} />
    </Routes>
    </BrowserRouter>
  </StrictMode>
)

