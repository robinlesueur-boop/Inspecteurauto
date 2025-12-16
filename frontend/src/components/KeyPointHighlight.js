import React from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, AlertCircle, CheckCircle, Info } from 'lucide-react';

function KeyPointHighlight({ type = 'tip', title, children, className = '' }) {
  const configs = {
    tip: {
      icon: <Lightbulb className="h-5 w-5" />,
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-400',
      textColor: 'text-yellow-800',
      iconColor: 'text-yellow-600'
    },
    warning: {
      icon: <AlertCircle className="h-5 w-5" />,
      bgColor: 'bg-red-50',
      borderColor: 'border-red-400',
      textColor: 'text-red-800',
      iconColor: 'text-red-600'
    },
    success: {
      icon: <CheckCircle className="h-5 w-5" />,
      bgColor: 'bg-green-50',
      borderColor: 'border-green-400',
      textColor: 'text-green-800',
      iconColor: 'text-green-600'
    },
    info: {
      icon: <Info className="h-5 w-5" />,
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-400',
      textColor: 'text-blue-800',
      iconColor: 'text-blue-600'
    }
  };

  const config = configs[type] || configs.info;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      viewport={{ once: true }}
      className={`${config.bgColor} ${config.borderColor} border-l-4 p-4 rounded-r-lg ${className}`}
    >
      <div className="flex items-start space-x-3">
        <div className={`${config.iconColor} flex-shrink-0 mt-0.5`}>
          {config.icon}
        </div>
        <div className="flex-1">
          {title && (
            <h4 className={`${config.textColor} font-semibold mb-2`}>
              {title}
            </h4>
          )}
          <div className={`${config.textColor} text-sm leading-relaxed`}>
            {children}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default KeyPointHighlight;