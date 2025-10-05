
import HeroSection from '../components/home/HeroSection';
import FeaturesSection from '../components/home/FeaturesSection';
import StatisticsSection from '../components/home/StatisticsSection';

const Home = () => {
  return (
    <div className="min-h-screen">
      <main>
        <HeroSection />
        <FeaturesSection />
        <StatisticsSection />
      </main>
    </div>
  );
};

export default Home;
