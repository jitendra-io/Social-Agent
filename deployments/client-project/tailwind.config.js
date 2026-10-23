/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#6366f1',
          accent: '#06b6d4',
          dark: '#0f172a',
          card: '#1e293b'
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
