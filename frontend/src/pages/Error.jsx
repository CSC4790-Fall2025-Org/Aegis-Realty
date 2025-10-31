import { Link } from 'react-router-dom'
import { useScrollToTop } from "../hooks/useScrollToTop.js";

const Error = () => {
  useScrollToTop();

    return (
        <div className="min-h-screen flex items-center justify-center bg-background">
          <div className="container mx-auto px-4 py-16 text-center">
            <h1 className="text-6xl font-bold text-text mb-4">404</h1>
            <h2 className="text-3xl font-semibold text-text mb-4">Page Not Found</h2>
            <p className="text-text/80 mb-8">The page you're looking for doesn't exist.</p>
            <Link
              to="/"
              className="inline-block bg-primary text-white px-6 py-3 rounded-md
              hover:bg-primary/70 transition-colors cursor-pointer"
            >
              Go Back Home
            </Link>
          </div>
        </div>
    )
}

export default Error