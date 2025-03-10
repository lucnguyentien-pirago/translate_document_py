import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': 'var(--primary-color)',
        'primary-light': 'var(--primary-300)',
        'primary-dark': 'var(--primary-700)',
        'surface-ground': 'var(--surface-ground)',
        'surface-section': 'var(--surface-section)',
        'surface-border': 'var(--surface-border)',
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
} satisfies Config 