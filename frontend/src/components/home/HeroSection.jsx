import { FiTrendingUp, FiShield, FiZap } from 'react-icons/fi';

const HeroSection = () => {
  return (
    <section className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-text mb-6">
            Revolutionize Your
            <span className="text-primary block">Real Estate Investment</span>
          </h1>

          <p className="text-xl text-muted max-w-3xl mx-auto mb-8">
            Leverage AI-powered insights and comprehensive analysis to make smarter property investment decisions.
            From instant cash flow projections to automated property management - all in one platform.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <div className="flex items-center space-x-2 text-primary">
              <FiTrendingUp className="w-5 h-5" />
              <span>AI-Powered Analysis</span>
            </div>
            <div className="flex items-center space-x-2 text-primary">
              <FiShield className="w-5 h-5" />
              <span>Risk Assessment</span>
            </div>
            <div className="flex items-center space-x-2 text-primary">
              <FiZap className="w-5 h-5" />
              <span>Instant Reports</span>
            </div>
          </div>

          <div className="bg-white/80 backdrop-blur-sm rounded-lg shadow-lg p-6 max-w-md mx-auto">
            <h3 className="text-lg font-semibold text-text mb-4">Start Your Analysis</h3>
            <input
              type="text"
              placeholder="Enter property address..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;