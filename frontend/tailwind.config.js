/**
 * Tailwind CSS Configuration for ColorFocus
 *
 * This configuration extends the default Tailwind theme with the canonical
 * color tokens from the shared colors.json source of truth.
 *
 * Color classes follow the pattern: {property}-{color}-{variant}
 * Examples: text-blue-base, bg-orange-bright, border-purple-dark
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Load color tokens from the shared source of truth.
 * This runs at build time, not runtime.
 */
function loadColorTokens() {
  const colorsPath = resolve(__dirname, '../shared/colors.json');
  const colorsData = JSON.parse(readFileSync(colorsPath, 'utf-8'));

  const colors = {};

  for (const [tokenName, tokenData] of Object.entries(colorsData)) {
    const lowerToken = tokenName.toLowerCase();

    for (const [variant, hexValue] of Object.entries(tokenData.variants)) {
      const colorKey = `${lowerToken}-${variant}`;
      colors[colorKey] = hexValue;
    }
  }

  return colors;
}

const colorTokens = loadColorTokens();

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx,html}',
    './index.html',
  ],

  /**
   * Safelist ensures color token classes are not purged during production builds.
   * This is necessary because color classes may be dynamically constructed.
   */
  safelist: [
    // Safelist all color token classes
    {
      pattern: /^(text|bg|border|ring|outline)-(blue|orange|purple|black|cyan|amber|magenta|gray)-(dark|base|bright)$/,
    },
    // Safelist fill and stroke for SVG support
    {
      pattern: /^(fill|stroke)-(blue|orange|purple|black|cyan|amber|magenta|gray)-(dark|base|bright)$/,
    },
  ],

  theme: {
    extend: {
      /**
       * Color Token System
       *
       * All 24 color values (8 tokens x 3 variants) are available as Tailwind utilities.
       * Note: BLACK only has 'base' and 'bright' variants (no 'dark').
       *
       * Usage examples:
       * - text-blue-base     - Blue text at standard brightness
       * - bg-orange-bright   - Orange background at increased brightness
       * - border-purple-dark - Purple border at reduced brightness
       */
      colors: colorTokens,
    },
  },

  plugins: [],
};
