import { Routes, Route } from 'react-router-dom'
import Footer from "./components/layout/Footer.jsx";
import Header from "./components/layout/Header.jsx";
import Home from "./pages/Home.jsx"

const App = () => {
  return (
    <div className="min-h-screen">
      <Header/>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/properties" element={<div>Properties Page</div>} />
          <Route path="/services" element={<div>Services Page</div>} />
          <Route path="/contact" element={<div>Contact Page</div>} />
          <Route path="/about" element={<div>About Page</div>} />
        </Routes>
      </main>
      <Footer/>
    </div>
  )
}

export default App;