import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Clock } from 'lucide-react';

function ReadingProgressBar({ estimatedMinutes }) {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [timeSpent, setTimeSpent] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.scrollY;
      const progress = (scrolled / documentHeight) * 100;
      setScrollProgress(Math.min(progress, 100));
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 60000); // Chaque minute

    return () => clearInterval(timer);
  }, []);

  const getProgressColor = () => {
    if (scrollProgress < 33) return 'bg-blue-500';
    if (scrollProgress < 66) return 'bg-purple-500';
    return 'bg-green-500';
  };

  const getMotivationalMessage = () => {
    if (scrollProgress < 25) return 'Bon début ! 🚀';
    if (scrollProgress < 50) return 'Continue comme ça ! 💪';
    if (scrollProgress < 75) return 'Presque là ! 🎯';
    if (scrollProgress < 95) return 'Dernière ligne droite ! 🏁';
    return 'Module terminé ! 🎉';
  };

  return (
    <div className="fixed top-16 left-0 right-0 z-50 bg-white shadow-md border-b">
      <div className="max-w-4xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-gray-700">
              {getMotivationalMessage()}
            </span>
            <span className="text-xs text-gray-500 flex items-center">
              <Clock className="h-3 w-3 mr-1" />
              {timeSpent} min / {estimatedMinutes} min
            </span>
          </div>
          <span className="text-sm font-semibold text-gray-700">
            {Math.round(scrollProgress)}%
          </span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <motion.div
            className={`h-full ${getProgressColor()} transition-colors duration-300`}
            initial={{ width: 0 }}
            animate={{ width: `${scrollProgress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>
    </div>
  );
}

export default ReadingProgressBar;