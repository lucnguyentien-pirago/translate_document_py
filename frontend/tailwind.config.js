/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': 'var(--primary-color)',
        'primary-dark': 'var(--primary-600)',
        'primary-light': 'var(--primary-300)',
        'primary-text': 'var(--primary-color-text)',
        'surface-ground': 'var(--surface-ground)',
        'surface-section': 'var(--surface-section)',
        'surface-card': 'var(--surface-card)',
        'surface-border': 'var(--surface-border)',
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
      spacing: {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
      },
    },
  },
  plugins: [],
} 