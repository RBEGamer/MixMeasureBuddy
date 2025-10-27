import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { promises as fs } from 'fs';
import path from 'path';
import { createRecipeRouter } from './routes/recipes.js';

const app = express();
const PORT = process.env.PORT || 4000;
const STORAGE_ROOT = process.env.RECIPE_STORAGE || path.join(process.cwd(), 'data', 'systems');
const STATIC_RECIPES_DIR = process.env.STATIC_RECIPES || path.join(process.cwd(), '..', '..', '..', 'src', 'recipes');

app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use(morgan('dev'));
const recipeRouter = createRecipeRouter({ recipesDir: STATIC_RECIPES_DIR });
app.use('/recipes', recipeRouter);

app.get('/', (_req, res) => {
  res.json({ status: 'ok', backend: 'MixMeasureBuddy', version: '1.0' });
});

const ensureSystemDirectory = async (systemId) => {
  const systemDir = path.join(STORAGE_ROOT, systemId);
  await fs.mkdir(systemDir, { recursive: true });
  return systemDir;
};

const isValidSystemId = (systemId) => /^[A-Za-z0-9_-]+$/.test(systemId);

const sanitizeRecipeName = (name) => {
  if (!name) return null;
  const base = decodeURIComponent(name)
    .trim()
    .replace(/\s+/g, '_')
    .replace(/[^A-Za-z0-9_.-]/g, '');
  if (!base || base === '' || base === '.' || base === '..') {
    return null;
  }
  if (!base.toLowerCase().endsWith('.recipe')) {
    return `${base}.recipe`;
  }
  return base;
};

const slugFromRecipeName = (name) =>
  name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '') || 'custom_mix';

const readRecipeFile = async (systemId, recipeFile) => {
  const systemDir = await ensureSystemDirectory(systemId);
  const filePath = path.join(systemDir, recipeFile);
  const data = await fs.readFile(filePath, 'utf8');
  return JSON.parse(data);
};

app.get('/:systemId', async (req, res) => {
  const { systemId } = req.params;
  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }

  try {
    const systemDir = await ensureSystemDirectory(systemId);
    const files = await fs.readdir(systemDir);
    const recipeCount = files.filter((file) => file.toLowerCase().endsWith('.recipe')).length;
    return res.json({ status: 'ok', systemId, totalRecipes: recipeCount, generatedAt: new Date().toISOString() });
  } catch (error) {
    console.error('[GET /:systemId] error', error);
    return res.status(500).json({ error: 'Failed to read system data.' });
  }
});

app.get('/:systemId/recipes', async (req, res) => {
  const { systemId } = req.params;
  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }

  try {
    const systemDir = await ensureSystemDirectory(systemId);
    const files = await fs.readdir(systemDir);
    const recipes = files.filter((file) => file.toLowerCase().endsWith('.recipe'));
    return res.json({ systemId, recipes });
  } catch (error) {
    console.error('[GET /:systemId/recipes] error', error);
    return res.status(500).json({ error: 'Failed to list recipes.' });
  }
});

app.get('/:systemId/recipe/:recipeName', async (req, res) => {
  const { systemId, recipeName } = req.params;
  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }
  const recipeFile = sanitizeRecipeName(recipeName);
  if (!recipeFile) {
    return res.status(400).json({ error: 'Invalid recipe name.' });
  }

  try {
    const recipe = await readRecipeFile(systemId, recipeFile);
    return res.json({ systemId, name: recipeFile.replace(/\.recipe$/i, ''), recipe });
  } catch (error) {
    console.error('[GET /:systemId/recipe/:recipeName] error', error);
    return res.status(404).json({ error: 'Recipe not found.' });
  }
});

app.post('/:systemId/recipes', async (req, res) => {
  const { systemId } = req.params;
  const { name, recipe } = req.body ?? {};

  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }

  if (!recipe || typeof recipe !== 'object') {
    return res.status(400).json({ error: 'Recipe payload is required.' });
  }

  const derivedName = name && typeof name === 'string' && name.trim().length > 0 ? name : recipe.name || slugFromRecipeName(systemId);
  const recipeFile = sanitizeRecipeName(derivedName);
  if (!recipeFile) {
    return res.status(400).json({ error: 'Unable to derive a valid recipe filename.' });
  }

  try {
    const systemDir = await ensureSystemDirectory(systemId);
    const filePath = path.join(systemDir, recipeFile);
    await fs.writeFile(filePath, JSON.stringify(recipe, null, 2), 'utf8');
    return res.status(201).json({ message: 'Recipe stored.', systemId, filename: recipeFile });
  } catch (error) {
    console.error('[POST /:systemId/recipes] error', error);
    return res.status(500).json({ error: 'Failed to store recipe.' });
  }
});

app.put('/:systemId/recipe/:recipeName', async (req, res) => {
  const { systemId, recipeName } = req.params;
  const { recipe } = req.body ?? {};

  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }
  if (!recipe || typeof recipe !== 'object') {
    return res.status(400).json({ error: 'Recipe payload is required.' });
  }

  const recipeFile = sanitizeRecipeName(recipeName);
  if (!recipeFile) {
    return res.status(400).json({ error: 'Invalid recipe name.' });
  }

  try {
    const systemDir = await ensureSystemDirectory(systemId);
    const filePath = path.join(systemDir, recipeFile);
    await fs.writeFile(filePath, JSON.stringify(recipe, null, 2), 'utf8');
    return res.json({ message: 'Recipe updated.', systemId, filename: recipeFile });
  } catch (error) {
    console.error('[PUT /:systemId/recipe/:recipeName] error', error);
    return res.status(500).json({ error: 'Failed to update recipe.' });
  }
});

app.delete('/:systemId/recipe/:recipeName', async (req, res) => {
  const { systemId, recipeName } = req.params;
  if (!isValidSystemId(systemId)) {
    return res.status(400).json({ error: 'Invalid system identifier.' });
  }
  const recipeFile = sanitizeRecipeName(recipeName);
  if (!recipeFile) {
    return res.status(400).json({ error: 'Invalid recipe name.' });
  }

  try {
    const systemDir = await ensureSystemDirectory(systemId);
    const filePath = path.join(systemDir, recipeFile);
    await fs.unlink(filePath);
    return res.json({ message: 'Recipe deleted.', systemId, filename: recipeFile });
  } catch (error) {
    if (error.code === 'ENOENT') {
      return res.status(404).json({ error: 'Recipe not found.' });
    }
    console.error('[DELETE /:systemId/recipe/:recipeName] error', error);
    return res.status(500).json({ error: 'Failed to delete recipe.' });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found.' });
});

const start = async () => {
  try {
    await fs.mkdir(STORAGE_ROOT, { recursive: true });
    app.listen(PORT, () => {
      // eslint-disable-next-line no-console
      console.log(`MixMeasureBuddy backend listening on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server', error);
    process.exit(1);
  }
};

start();
