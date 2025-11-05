import { Routes, Route } from 'react-router-dom'

import Footer from "./components/layout/Footer.jsx";
import Header from "./components/layout/Header.jsx";
import Home from "./pages/Home.jsx"
import Properties from "./pages/Properties.jsx";
import PropertyAnalysisPage from "./pages/PropertyAnalysisPage.jsx";

// AuthTest is for testing AuthContext functionality
import AuthTest from "./components/AuthTest.jsx";
// RegistrationForm is for user sign-up UI
import RegistrationForm from "./components/RegistrationForm.jsx";

const App = () => {
  return (
    <div className="min-h-screen">
      <Header/>
      <main>
        <Routes>
          {/* default page now*/}
          <Route path="/" element={<RegistrationForm />} />
          {/* Home page is now at /home */}
          <Route path="/home" element={<Home/>} />
          <Route path="/properties" element={<Properties/>}/>
          <Route path="/analysis" element={<PropertyAnalysisPage/>} />
          <Route path="/services" element={<div>Services Page</div>} />
          <Route path="/contact" element={<div>Contact Page</div>} />
          <Route path="/about" element={<div>About Page</div>} />
        </Routes>
        {/* AuthTest below is for testing AuthContext functionality. Remove when done testing. */}
        <AuthTest />
      </main>
      <Footer/>
    </div>
  )
}

export default App;