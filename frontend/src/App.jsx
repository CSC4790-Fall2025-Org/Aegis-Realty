import { Routes, Route } from 'react-router-dom'
import AuthForm from './containers/AuthForm.jsx';
import Error from "./pages/Error.jsx"
import Footer from "./components/layout/Footer.jsx";
import Header from "./components/layout/Header.jsx";
import Home from "./pages/Home.jsx"
import Analysis from "./pages/Analysis.jsx";
import Properties from "./pages/Properties.jsx";
import PropertyDetails from "./pages/PropertyDetails.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import UserProfile from "./pages/UserProfile.jsx"
import { useAuth } from './contexts/AuthContext.jsx';

const App = () => {
    const { isAuthenticated } = useAuth();
    return (
        <div className="min-h-screen flex flex-col">
        <Header/>
        <main className="flex-1">
            <Routes>
                <Route path="/" element={isAuthenticated ? <Home/> : <AuthForm mode="login"/>} />
                <Route path="/login" element={<AuthForm mode="login"/>}/>
                <Route path="/signup" element={<AuthForm mode="signup"/>}/>
                <Route path="/properties" element={
                    <ProtectedRoute>
                        <Properties/>
                    </ProtectedRoute>
                }/>
                <Route path="/properties/:id" element={
                    <ProtectedRoute>
                        <PropertyDetails/>
                    </ProtectedRoute>
                }/>
                <Route path="/analysis" element={
                    <ProtectedRoute>
                        <Analysis/>
                    </ProtectedRoute>
                }/>
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <UserProfile/>
                  </ProtectedRoute>
                }/>
                <Route path="*" element={<Error/>}/>
            </Routes>
        </main>
        <Footer/>
        </div>
  )
}

export default App;