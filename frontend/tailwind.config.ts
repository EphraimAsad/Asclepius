import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Disposition colors
        'disposition-911': {
          DEFAULT: '#DC2626',
          light: '#FEE2E2',
        },
        'disposition-er': {
          DEFAULT: '#EA580C',
          light: '#FFEDD5',
        },
        'disposition-urgent': {
          DEFAULT: '#F59E0B',
          light: '#FEF3C7',
        },
        'disposition-primary': {
          DEFAULT: '#EAB308',
          light: '#FEF9C3',
        },
        'disposition-self': {
          DEFAULT: '#16A34A',
          light: '#DCFCE7',
        },
      },
    },
  },
  plugins: [],
};

export default config;
