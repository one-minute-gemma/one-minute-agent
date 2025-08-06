/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'Helvetica', 'Arial', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', 'monospace'],
      },
      colors: {
        // Monochromatic Base - Deep Navy Blue Foundation
        base: {
          50: '#f8fafc',   // Lightest - for text on dark backgrounds
          100: '#f1f5f9',  // Very light gray-blue
          200: '#e2e8f0',  // Light gray-blue
          300: '#cbd5e1',  // Medium-light gray-blue
          400: '#94a3b8',  // Medium gray-blue
          500: '#64748b',  // Neutral gray-blue
          600: '#475569',  // Medium-dark gray-blue
          700: '#334155',  // Dark gray-blue
          800: '#1e293b',  // Very dark gray-blue
          900: '#0f172a',  // Darkest - primary background
          950: '#020617',  // Ultra dark - deepest backgrounds
        },
        // Single Primary Accent - Electric Blue
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',  // Main primary color
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        // Subtle Status Colors - Used sparingly for borders/icons only
        status: {
          safe: '#10b981',    // Green - only for confirmed safety
          warning: '#f59e0b', // Amber - for important updates
          danger: '#ef4444',  // Red - for critical situations
          info: '#3b82f6',    // Blue - for general information
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.3)' },
          '100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.6)' },
        },
      },
    },
  },
  plugins: [],
};