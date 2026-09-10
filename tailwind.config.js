/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './apps/**/*.py',
    './node_modules/flowbite/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        base: {
          900: '#0A0E1A',
          800: '#111827',
          700: '#1A2332',
          600: '#1F2937',
        },
        accent: {
          blue: '#0EA5E9',
          purple: '#8B5CF6',
          green: '#10B981',
          amber: '#F59E0B',
          red: '#EF4444',
          cyan: '#06B6D4',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        slideUp: {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      boxShadow: {
        'glow-blue': '0 0 30px rgba(14, 165, 233, 0.15)',
        'glow-purple': '0 0 30px rgba(139, 92, 246, 0.15)',
        'card-hover': '0 20px 40px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [
    require('flowbite/plugin'),
  ],
}