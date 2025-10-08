/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      animation: {
        "pulse-glow": "pulse-glow 2s ease-in-out infinite alternate",
      },
      keyframes: {
        "pulse-glow": {
          from: { boxShadow: "0 0 5px #3b82f6" },
          to: { boxShadow: "0 0 20px #3b82f6, 0 0 30px #3b82f6" },
        },
      },
    },
  },
  plugins: [],
}
