import { useLanguage } from '../context/LanguageContext';

const Home = () => {
  const { language } = useLanguage();

  const getWelcomeText = () => {
    switch (language) {
      case 'hindi':
        return 'फाइनेंस असिस्टेंट में आपका स्वागत है';
      case 'bengali':
        return 'ফাইন্যান্স অ্যাসিস্ট্যান্টে স্বাগতম';
      case 'english':
      default:
        return 'Welcome to Finance Assistant';
    }
  };

  return (
    <div className="min-h-screen p-8 flex items-center justify-center perspective-[1000px]">
      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative transform transition-all duration-500 hover:rotate-y-12 hover:rotate-x-12 hover:scale-105 preserve-3d">
          <div className="bg-gray-900 border border-gray-700/50 p-12 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] shadow-blue-500/10 backdrop-blur-sm">
            <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent rounded-2xl pointer-events-none border-t border-l border-white/10"></div>
            <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-white via-blue-100 to-gray-400 drop-shadow-sm mb-6 text-center transform translate-z-10">
              {getWelcomeText()}
            </h1>
            <p className="text-gray-400 text-center text-lg max-w-xl mx-auto transform translate-z-6">
              Manage your finances with AI-powered insights, multi-lingual support, and an immersive experience.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
