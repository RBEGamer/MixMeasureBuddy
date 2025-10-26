#!/usr/bin/env node

import { promises as fs } from 'fs';
import path from 'path';

const projectRoot = process.cwd();
const recipesDir = path.join(projectRoot, '..', '..', 'recipes');
const outputDir = path.join(projectRoot, 'public', 'data');
const outputFile = path.join(outputDir, 'sample-recipes.json');

async function collectRecipes() {
  try {
    const files = await fs.readdir(recipesDir);
    const recipeFiles = files.filter((file) => file.endsWith('.recipe'));

    const recipes = [];
    for (const filename of recipeFiles) {
      const fullPath = path.join(recipesDir, filename);
      try {
        const content = await fs.readFile(fullPath, 'utf8');
        const parsed = JSON.parse(content);
        recipes.push(parsed);
      } catch (error) {
        console.warn(
          `[build-sample-recipes] Skipped "${filename}" – invalid JSON (${error?.message ?? error})`,
        );
      }
    }

    recipes.sort((a, b) =>
      (a?.name ?? '').localeCompare(b?.name ?? '', undefined, {
        sensitivity: 'base',
      }),
    );

    return recipes;
  } catch (error) {
    console.error(
      '[build-sample-recipes] Failed to read recipes directory:',
      error,
    );
    return [];
  }
}

async function main() {
  const recipes = await collectRecipes();
  await fs.mkdir(outputDir, { recursive: true });
  await fs.writeFile(outputFile, JSON.stringify(recipes, null, 2), 'utf8');
  console.log(
    `[build-sample-recipes] wrote ${recipes.length} recipe(s) to ${path.relative(
      projectRoot,
      outputFile,
    )}`,
  );
}

main().catch((error) => {
  console.error('[build-sample-recipes] Unexpected failure:', error);
  process.exitCode = 1;
});
