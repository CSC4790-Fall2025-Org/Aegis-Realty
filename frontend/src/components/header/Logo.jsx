import AegisLogo from "../../assets/images/Aegis_Realty_Logo_Transparent.png";

const Logo = ({ onClick }) => (
  <div className="flex items-center cursor-pointer" onClick={onClick}>
    <img src={AegisLogo} alt="Aegis Realty Logo" className="h-10 w-auto" />
    <span className="ml-2 text-xl font-bold text-text">Aegis Realty</span>
  </div>
);

export default Logo;