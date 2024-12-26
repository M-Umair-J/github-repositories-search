/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        maroon: {
          50: '#fdf2f4',
          100: '#fce7ea',
          200: '#f9d0d7',
          300: '#f4a9b5',
          400: '#ed758c',
          500: '#e14668',
          600: '#cc2952',
          700: '#ac1d42',
          800: '#8f1b3c',
          900: '#7a1a37',
          950: '#440a1a',
        },
      },
    },
  },
  plugins: [],
};