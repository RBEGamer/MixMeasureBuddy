import { Router } from 'express';
import path from 'path';
import { promises as fs } from 'fs';
import {
  addRecipeRecord,
  getSystemAssignments,
  removeRecipeRecord,
  setAvailableRecipes,
  getAvailableRecipes,
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

export function createRecipeRouter({ recipesDir }) {
  const router = Router();

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
    try {
      const updated = await addRecipeRecord(systemId, recipe);
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
      const assignments = await getSystemAssignments(systemId);
      const payload = assignments.reduce((acc, recipeName) => {
        const key = recipeName.replace(/\.recipe$/i, '');
        if (available[key]) {
          acc[recipeName] = available[key];
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
