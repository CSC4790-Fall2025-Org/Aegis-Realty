import React from "react";

const StatisticsSection = () => {
  const stats = [
    { number: "10,000+", label: "Properties Analyzed" },
    { number: "95%", label: "Accuracy Rate" },
    { number: "500+", label: "Active Investors" },
    { number: "$2.5M", label: "Properties Under Management" }
  ];

  return (
    <section className="py-20 bg-primary/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-text mb-4">
            Trusted by Investors Nationwide
          </h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">
                {stat.number}
              </div>
              <div className="text-muted">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatisticsSection;