import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Plans from './pages/Plans'
import Register from './pages/Register'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/plans" element={<Plans />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}