import fs from 'fs';
import path from 'path';
import os from 'os';

const configPath = path.join(
  os.homedir(),
  '.config',
  'opencode',
  'configs',
  'local-plugins.json',
);

export function isPluginEnabled(pluginName: string): boolean {
  try {
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      // Default to false if not explicitly true
      return config[pluginName] === true;
    }
  } catch (err) {
    console.error(`[Plugin Config] Failed to read configs/local-plugins.json: ${err}`);
  }
  return false;
}
