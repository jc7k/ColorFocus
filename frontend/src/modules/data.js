/**
 * JSON data loading module.
 * Loads shared JSON configuration files.
 */

/**
 * Load JSON file via fetch (better iOS Safari compatibility)
 */
async function loadJSON(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to load ${path}`);
  return response.json();
}

// Load all JSON data in parallel
const [colorsJson, colorLabelsJson, uiTextJson] = await Promise.all([
  loadJSON('/shared/colors.json'),
  loadJSON('/shared/color_labels.json'),
  loadJSON('/shared/ui_text.json')
]);

export { colorsJson, colorLabelsJson, uiTextJson };
