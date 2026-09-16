/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './apps/**/*.py',
    './node_modules/flowbite/**/*.js',
  ],
  darkMode: 'class',
  safelist: [
    // Forzar que se generen estas clases siempre
    'bg-brand-500',
    'bg-brand-600',
    'text-brand-500',
    'text-brand-400',
    'border-brand-500',
    'border-brand-500/20',
    'border-brand-500/30',
    'bg-brand-500/10',
    'bg-brand-500/20',
    'shadow-glow-brand',
    'shadow-glow-brand-sm',
    'bg-dark-900',
    'bg-dark-800',
    'bg-dark-700',
    'bg-dark-600',
    'border-dark-600',
    'border-dark-500',
    'text-white',
    'text-slate-400',
    'text-slate-500',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#FFF5F0',
          100: '#FFE6D5',
          200: '#FFC9A8',
          300: '#FFA470',
          400: '#FF8552',
          500: '#FF6B35',
          600: '#E5521A',
          700: '#C23E0F',
          800: '#9A3109',
          900: '#7A2706',
        },
        dark: {
          950: '#050505',
          900: '#0A0A0A',
          800: '#141414',
          700: '#1A1A1A',
          600: '#2A2A2A',
          500: '#3A3A3A',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '3xl': '24px',
        '4xl': '32px',
        '5xl': '40px',
      },
      boxShadow: {
        'card': '0 4px 24px rgba(0, 0, 0, 0.4)',
        'card-hover': '0 12px 40px rgba(0, 0, 0, 0.5)',
        'glow-brand': '0 0 40px rgba(255, 107, 53, 0.25)',
        'glow-brand-sm': '0 0 20px rgba(255, 107, 53, 0.15)',
      },
    },
  },
  plugins: [
    require('flowbite/plugin'),
  ],
}