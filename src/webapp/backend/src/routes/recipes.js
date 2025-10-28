import { Router } from 'express';
import path from 'path';
import { promises as fs } from 'fs';
import {
  addRecipeRecord,
  getSystemAssignments,
  removeRecipeRecord,
  setAvailableRecipes,
  getAvailableRecipes,
  storeCustomRecipe,
  getCustomRecipe,
  listCustomRecipesForSystem,
  getAllCustomRecipes,
} from '../storage.js';

const loadRecipes = async (recipesDir) => {
  const files = await fs.readdir(recipesDir);
  const records = {};
  for (const file of files) {
    if (!file.toLowerCase().endsWith('.recipe')) continue;
    const filePath = path.join(recipesDir, file);
    const raw = await fs.readFile(filePath, 'utf8');
    const json = JSON.parse(raw);
    records[file.replace(/\.recipe$/i, '')] = json;
  }
  return records;
};

const slugify = (value) =>
  value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .replace(/_{2,}/g, '_');

export function createRecipeRouter({ recipesDir, storageRoot }) {
  const router = Router();

  const ensureSystemDir = async (systemId) => {
    const dir = path.join(storageRoot, systemId);
    await fs.mkdir(dir, { recursive: true });
    return dir;
  };

  const writeRecipeFile = async (systemId, recipeId, recipe) => {
    const dir = await ensureSystemDir(systemId);
    const filePath = path.join(dir, recipeId);
    const payload = { ...recipe, filename: recipeId };
    await fs.writeFile(filePath, JSON.stringify(payload, null, 2), 'utf8');
  };

  router.get('/available', async (_req, res) => {
    try {
      const json = await loadRecipes(recipesDir);
      await setAvailableRecipes(json);
      const recipeNames = Object.keys(json);
      return res.json({ recipes: recipeNames, map: json });
    } catch (error) {
      console.error('[backend] list available recipes error', error);
      return res.status(500).json({ error: 'Failed to load available recipes.' });
    }
  });

  router.get('/custom/:systemId', async (req, res) => {
    const { systemId } = req.params;
    try {
      const recipes = await listCustomRecipesForSystem(systemId);
      return res.json({ systemId, recipes });
    } catch (error) {
      console.error('[backend] list custom recipes', error);
      return res.status(500).json({ error: 'Failed to load custom recipes.' });
    }
  });

  router.get('/custom/shared/:recipeId', async (req, res) => {
    const { recipeId } = req.params;
    try {
      const custom = await getCustomRecipe(recipeId);
      if (!custom) {
        return res.status(404).json({ error: 'Custom recipe not found.' });
      }
      return res.json({ recipeId, ...custom });
    } catch (error) {
      console.error('[backend] get shared custom recipe', error);
      return res.status(500).json({ error: 'Failed to load custom recipe.' });
    }
  });

  router.post('/custom/:systemId', async (req, res) => {
    const { systemId } = req.params;
    const { name, recipe } = req.body ?? {};

    if (!recipe || typeof recipe !== 'object') {
      return res.status(400).json({ error: 'Recipe payload is required.' });
    }

    const recipeName = name && typeof name === 'string' && name.trim().length > 0 ? name.trim() : recipe.name || 'Custom Mix';
    const slug = slugify(recipeName) || 'custom_mix';
    const recipeId = `${systemId}-${slug}.recipe`;

    const recipePayload = {
      ...recipe,
      name: recipeName,
      description: recipe.description ?? '',
      version: recipe.version ?? '1.0.0',
    };

    try {
      await storeCustomRecipe(systemId, recipeId, recipePayload);
      await writeRecipeFile(systemId, recipeId, recipePayload);
      await addRecipeRecord(systemId, recipeId);
      return res.status(201).json({ systemId, recipeId });
    } catch (error) {
      console.error('[backend] store custom recipe', error);
      return res.status(500).json({ error: 'Failed to store custom recipe.' });
    }
  });

  router.get('/assigned/:systemId', async (req, res) => {
    const { systemId } = req.params;
    try {
      const list = await getSystemAssignments(systemId);
      return res.json({ systemId, recipes: list });
    } catch (error) {
      console.error('[backend] list assignments', error);
      return res.status(500).json({ error: 'Failed to read assignments.' });
    }
  });

  router.post('/assigned/:systemId', async (req, res) => {
    const { systemId } = req.params;
    const { recipe } = req.body ?? {};
    if (!recipe || typeof recipe !== 'string') {
      return res.status(400).json({ error: 'Recipe name is required.' });
    }

    const normalized = recipe.endsWith('.recipe') ? recipe : `${recipe}.recipe`;
    const staticMap = await getAvailableRecipes();
    const staticKey = normalized.replace(/\.recipe$/i, '');
    const customRecord = await getCustomRecipe(normalized);

    if (!staticMap[staticKey] && !customRecord) {
      return res.status(404).json({ error: 'Recipe not found in library.' });
    }

    try {
      const updated = await addRecipeRecord(systemId, normalized);
      if (available[staticKey]) {
        await writeRecipeFile(systemId, normalized, available[staticKey]);
      } else if (customRecord) {
        await writeRecipeFile(systemId, normalized, customRecord.recipe);
      }
      return res.status(201).json({ systemId, recipes: updated });
    } catch (error) {
      console.error('[backend] add assignment', error);
      return res.status(500).json({ error: 'Failed to assign recipe.' });
    }
  });

  router.delete('/assigned/:systemId/:recipeName', async (req, res) => {
    const { systemId, recipeName } = req.params;
    try {
      const updated = await removeRecipeRecord(systemId, recipeName);
      return res.json({ systemId, recipes: updated });
    } catch (error) {
      console.error('[backend] remove assignment', error);
      return res.status(500).json({ error: 'Failed to remove assignment.' });
    }
  });

  router.get('/sync/:systemId', async (req, res) => {
    const { systemId } = req.params;
    try {
      const available = await getAvailableRecipes();
      const custom = await getAllCustomRecipes();
      const assignments = await getSystemAssignments(systemId);
      const payload = assignments.reduce((acc, recipeName) => {
        const staticKey = recipeName.replace(/\.recipe$/i, '');
        if (available[staticKey]) {
          acc[recipeName] = available[staticKey];
        } else if (custom[recipeName]) {
          acc[recipeName] = custom[recipeName].recipe;
        }
        return acc;
      }, {});
      return res.json({ systemId, recipes: payload });
    } catch (error) {
      console.error('[backend] sync recipes', error);
      return res.status(500).json({ error: 'Failed to prepare sync payload.' });
    }
  });

  return router;
}
