import { promises as fs } from 'fs';
import path from 'path';
import rss from './rss.mjs';

const STUB_CONTENT =
  "self.__next_script_stub||(self.__next_script_stub=!0,console.info('[NextJS] script.js stub served from static export.'));\n";

async function ensureScriptStub() {
  const buildDir = path.join(process.cwd(), 'out', '_next', 'static', 'chunks');
  const scriptPath = path.join(buildDir, 'script.js');

  try {
    await fs.mkdir(buildDir, { recursive: true });
    await fs.writeFile(scriptPath, STUB_CONTENT, 'utf8');
    console.info('[postbuild] Ensured /_next/static/chunks/script.js stub exists.');
  } catch (error) {
    console.warn('[postbuild] Failed to write script.js stub:', error);
  }
}

async function postbuild() {
  await rss();
  await ensureScriptStub();
}

postbuild();
