import { promises as fs } from 'fs';
import path from 'path';

const DB_PATH = process.env.RECIPE_DB_PATH || path.join(process.cwd(), 'data', 'assignments.json');

const defaultDatabase = {
  systems: {},
  recipes: {},
  custom: {},
};

const ensureDatabase = async () => {
  try {
    await fs.mkdir(path.dirname(DB_PATH), { recursive: true });
    await fs.access(DB_PATH);
  } catch (error) {
    if (error.code === 'ENOENT') {
      await fs.writeFile(DB_PATH, JSON.stringify(defaultDatabase, null, 2), 'utf8');
      return;
    }
    throw error;
  }
};

const readDatabase = async () => {
  await ensureDatabase();
  const raw = await fs.readFile(DB_PATH, 'utf8');
  const data = JSON.parse(raw);
  return {
    systems: data.systems ?? {},
    recipes: data.recipes ?? {},
    custom: data.custom ?? {},
  };
};

const writeDatabase = async (data) => {
  await fs.writeFile(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
};

export const getSystemAssignments = async (systemId) => {
  const db = await readDatabase();
  return db.systems[systemId] ?? [];
};

export const replaceSystemAssignments = async (systemId, assignments) => {
  const db = await readDatabase();
  db.systems[systemId] = assignments;
  await writeDatabase(db);
};

export const addRecipeRecord = async (systemId, recipeName) => {
  const db = await readDatabase();
  const current = db.systems[systemId] ?? [];
  if (!current.includes(recipeName)) {
    current.push(recipeName);
    db.systems[systemId] = current;
    await writeDatabase(db);
  }
  return current;
};

export const removeRecipeRecord = async (systemId, recipeName) => {
  const db = await readDatabase();
  const current = db.systems[systemId] ?? [];
  db.systems[systemId] = current.filter((entry) => entry !== recipeName);
  await writeDatabase(db);
  return db.systems[systemId];
};

export const listSystems = async () => {
  const db = await readDatabase();
  return Object.keys(db.systems);
};

export const setAvailableRecipes = async (recipes) => {
  const db = await readDatabase();
  db.recipes = recipes;
  await writeDatabase(db);
};

export const getAvailableRecipes = async () => {
  const db = await readDatabase();
  return db.recipes ?? {};
};

export const storeCustomRecipe = async (systemId, recipeId, recipe) => {
  const db = await readDatabase();
  db.custom[recipeId] = {
    owner: systemId,
    recipe,
    name: recipe?.name ?? recipeId,
    description: recipe?.description ?? '',
    createdAt: new Date().toISOString(),
  };
  await writeDatabase(db);
};

export const getCustomRecipe = async (recipeId) => {
  const db = await readDatabase();
  return db.custom?.[recipeId];
};

export const getAllCustomRecipes = async () => {
  const db = await readDatabase();
  return db.custom ?? {};
};

export const listCustomRecipesForSystem = async (systemId) => {
  const db = await readDatabase();
  return Object.entries(db.custom ?? {})
    .filter(([, value]) => value?.owner === systemId)
    .map(([id, value]) => ({
      id,
      name: value?.name ?? id,
      description: value?.description ?? '',
      owner: value?.owner,
    }));
};
