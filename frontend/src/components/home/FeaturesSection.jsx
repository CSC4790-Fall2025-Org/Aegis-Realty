import { FiBarChart2, FiUsers, FiFileText, FiCalendar, FiDollarSign, FiShield } from 'react-icons/fi';

const FeaturesSection = () => {
  const features = [
    {
      icon: <FiBarChart2 className="w-8 h-8" />,
      title: "Investment Analysis",
      description: "Get comprehensive cash flow projections, market trends, and ROI calculations powered by AI."
    },
    {
      icon: <FiUsers className="w-8 h-8" />,
      title: "Tenant Management",
      description: "Securely store tenant information, track rental payments, and manage lease agreements."
    },
    {
      icon: <FiFileText className="w-8 h-8" />,
      title: "Document Analysis",
      description: "Upload legal documents and receive AI-powered summaries highlighting key terms and risks."
    },
    {
      icon: <FiCalendar className="w-8 h-8" />,
      title: "Maintenance Scheduling",
      description: "Schedule and track property maintenance tasks with automated reminders and notifications."
    },
    {
      icon: <FiDollarSign className="w-8 h-8" />,
      title: "Financial Tracking",
      description: "Monitor property performance with detailed financial reports and expense tracking."
    },
    {
      icon: <FiShield className="w-8 h-8" />,
      title: "Risk Assessment",
      description: "Identify potential risks and opportunities with AI-driven market analysis and insights."
    }
  ];

  return (
    <section className="py-20 bg-white/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-text mb-4">
            Everything You Need to Succeed
          </h2>
          <p className="text-xl text-muted max-w-2xl mx-auto">
            Our comprehensive platform combines powerful analytics with practical management tools
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="text-primary mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-text mb-3">
                {feature.title}
              </h3>
              <p className="text-muted">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;