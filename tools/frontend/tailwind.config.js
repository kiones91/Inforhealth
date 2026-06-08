/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../site/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'monospace'],
      },
      colors: {
        ih: {
          primary: '#09314d',
          secondary: '#2f80b5',
          accent: '#16a89a',
          'accent-dark': '#118a7e',
          orange: '#ff8e2b',
          surface: '#ffffff',
          muted: '#f4f8fa',
          seguranca: '#0d9488',
        },
        stone: {
          200: '#e7e5e4',
        },
      },
    },
  },
  plugins: [],
};
