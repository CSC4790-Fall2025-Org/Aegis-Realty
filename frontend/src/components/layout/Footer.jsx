import { useNavigate } from "react-router-dom";
import AegisLogo from "../../assets/images/Aegis_Realty_Logo_Transparent.png";

const Footer = () => {
  const navigate = useNavigate();

  return (
    <footer className="bg-text text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <button
                onClick={() => navigate('/')}
                className="flex items-center space-x-3 hover:opacity-80 transition-opacity cursor-pointer"
              >
                <img
                  src={AegisLogo}
                  alt="Aegis Realty Logo"
                  className="h-8 w-auto"
                />
                <span className="text-xl font-bold">Aegis Realty</span>
              </button>
            </div>
            <p className="text-gray-300 mb-4">
              Empowering real estate investors with AI-driven insights and comprehensive property management solutions.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => navigate("/properties")}
                  className="text-gray-300 hover:text-white transition-colors text-left cursor-pointer"
                >
                  Properties
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigate("/services")}
                  className="text-gray-300 hover:text-white transition-colors text-left cursor-pointer"
                >
                  Services
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigate("/contact")}
                  className="text-gray-300 hover:text-white transition-colors text-left cursor-pointer"
                >
                  Contact
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigate("/about")}
                  className="text-gray-300 hover:text-white transition-colors text-left cursor-pointer"
                >
                  About Us
                </button>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <div className="space-y-2 text-gray-300">
              <p>Email: info@aegisrealty.com</p>
              <p>Phone: (555) 123-4567</p>
              <p>Address: 123 Real Estate Ave<br />Suite 100, City, State 12345</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
          <p>&copy; 2025 Aegis Realty. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
