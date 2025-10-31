import { Routes, Route } from 'react-router-dom'
import AuthForm from './containers/AuthForm.jsx';
import Error from "./pages/Error.jsx"
import Footer from "./components/layout/Footer.jsx";
import Header from "./components/layout/Header.jsx";
import Home from "./pages/Home.jsx"
import Properties from "./pages/Properties.jsx";

const App = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header/>
      <main className="flex-1">
        <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/login" element={<AuthForm mode="login"/>}/>
            <Route path="/signup" element={<AuthForm mode="signup"/>}/>
            <Route path="/properties" element={<Properties/>}/>
            <Route path="/services" element={<div>Services Page</div>} />
            <Route path="*" element={<Error/>}/>
        </Routes>
      </main>
      <Footer/>
    </div>
  )
}

export default App;