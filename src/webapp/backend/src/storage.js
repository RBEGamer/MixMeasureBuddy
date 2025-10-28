import { promises as fs } from 'fs';
import path from 'path';
import sqlite3 from 'sqlite3';

const DB_PATH =
  process.env.RECIPE_DB_PATH || path.join(process.cwd(), 'data', 'mixmeasurebuddy.sqlite');

sqlite3.verbose();

let dbPromise;

const ensureDirectory = async () => {
  await fs.mkdir(path.dirname(DB_PATH), { recursive: true });
};

const schema = `
        PRAGMA journal_mode = WAL;
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS systems (
          id TEXT PRIMARY KEY,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS assignments (
          system_id TEXT NOT NULL,
          recipe_id TEXT NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (system_id, recipe_id),
          FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS custom_recipes (
          id TEXT PRIMARY KEY,
          owner TEXT NOT NULL,
          name TEXT NOT NULL,
          description TEXT DEFAULT '',
          recipe_json TEXT NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (owner) REFERENCES systems(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS available_recipes (
          id TEXT PRIMARY KEY,
          recipe_json TEXT NOT NULL
        );
      `;

const initialize = async () => {
  await ensureDirectory();
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        reject(err);
        return;
      }

      db.exec(schema, (execError) => {
        if (!execError) {
          resolve(db);
          return;
        }

        if (execError.code === 'SQLITE_NOTADB') {
          db.close(async (closeErr) => {
            if (closeErr) {
              reject(closeErr);
              return;
            }

            try {
              await fs.unlink(DB_PATH);
            } catch (unlinkErr) {
              if (unlinkErr.code !== 'ENOENT') {
                reject(unlinkErr);
                return;
              }
            }

            try {
              const freshDb = await initialize();
              resolve(freshDb);
            } catch (retryErr) {
              reject(retryErr);
            }
          });
        } else {
          reject(execError);
        }
      });
    });
  });
};

const getDb = async () => {
  if (!dbPromise) {
    dbPromise = initialize();
  }
  return dbPromise;
};

const runRaw = (db, sql, params = []) =>
  new Promise((resolve, reject) => {
    db.run(sql, params, function runCallback(err) {
      if (err) {
        reject(err);
      } else {
        resolve(this);
      }
    });
  });

const getRaw = (db, sql, params = []) =>
  new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) {
        reject(err);
      } else {
        resolve(row);
      }
    });
  });

const allRaw = (db, sql, params = []) =>
  new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
    });
  });

const run = async (sql, params = []) => {
  const db = await getDb();
  return runRaw(db, sql, params);
};

const all = async (sql, params = []) => {
  const db = await getDb();
  return allRaw(db, sql, params);
};

const withTransaction = async (handler) => {
  const db = await getDb();
  await runRaw(db, 'BEGIN IMMEDIATE');
  try {
    const result = await handler(db);
    await runRaw(db, 'COMMIT');
    return result;
  } catch (error) {
    try {
      await runRaw(db, 'ROLLBACK');
    } catch {
      // ignore rollback errors
    }
    throw error;
  }
};

const ensureSystem = async (db, systemId) => {
  if (!systemId || !systemId.trim()) {
    return;
  }
  await runRaw(db, 'INSERT OR IGNORE INTO systems (id) VALUES (?)', [systemId.trim()]);
};

export const getSystemAssignments = async (systemId) => {
  const rows = await all('SELECT recipe_id FROM assignments WHERE system_id = ? ORDER BY created_at, recipe_id', [
    systemId,
  ]);
  return rows.map((row) => row.recipe_id);
};

export const replaceSystemAssignments = async (systemId, assignments) => {
  await withTransaction(async (db) => {
    await ensureSystem(db, systemId);
    await runRaw(db, 'DELETE FROM assignments WHERE system_id = ?', [systemId]);
    for (const recipeId of assignments) {
      await runRaw(db, 'INSERT OR IGNORE INTO assignments (system_id, recipe_id) VALUES (?, ?)', [
        systemId,
        recipeId,
      ]);
    }
  });
  return assignments;
};

export const addRecipeRecord = async (systemId, recipeName) => {
  await withTransaction(async (db) => {
    await ensureSystem(db, systemId);
    await runRaw(db, 'INSERT OR IGNORE INTO assignments (system_id, recipe_id) VALUES (?, ?)', [
      systemId,
      recipeName,
    ]);
  });
  return getSystemAssignments(systemId);
};

export const removeRecipeRecord = async (systemId, recipeName) => {
  await run('DELETE FROM assignments WHERE system_id = ? AND recipe_id = ?', [systemId, recipeName]);
  return getSystemAssignments(systemId);
};

export const listSystems = async () => {
  const rows = await all('SELECT id FROM systems ORDER BY id ASC');
  return rows.map((row) => row.id);
};

export const setAvailableRecipes = async (recipes) => {
  await withTransaction(async (db) => {
    await runRaw(db, 'DELETE FROM available_recipes');
    for (const [id, recipe] of Object.entries(recipes ?? {})) {
      await runRaw(db, 'INSERT INTO available_recipes (id, recipe_json) VALUES (?, ?)', [
        id,
        JSON.stringify(recipe ?? {}),
      ]);
    }
  });
};

export const getAvailableRecipes = async () => {
  const rows = await all('SELECT id, recipe_json FROM available_recipes');
  return rows.reduce((acc, row) => {
    try {
      acc[row.id] = JSON.parse(row.recipe_json);
    } catch {
      acc[row.id] = null;
    }
    return acc;
  }, {});
};

export const storeCustomRecipe = async (systemId, recipeId, recipe) => {
  await withTransaction(async (db) => {
    await ensureSystem(db, systemId);
    await runRaw(
      db,
      `
        INSERT INTO custom_recipes (id, owner, name, description, recipe_json, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(id) DO UPDATE SET
          owner = excluded.owner,
          name = excluded.name,
          description = excluded.description,
          recipe_json = excluded.recipe_json
      `,
      [
        recipeId,
        systemId,
        recipe?.name ?? recipeId,
        recipe?.description ?? '',
        JSON.stringify(recipe ?? {}),
      ],
    );
  });
};

export const getCustomRecipe = async (recipeId) => {
  const db = await getDb();
  const row = await getRaw(db, 'SELECT id, owner, name, description, recipe_json, created_at FROM custom_recipes WHERE id = ?', [
    recipeId,
  ]);
  if (!row) {
    return undefined;
  }
  let recipe;
  try {
    recipe = JSON.parse(row.recipe_json);
  } catch {
    recipe = null;
  }
  return {
    owner: row.owner,
    name: row.name,
    description: row.description,
    createdAt: row.created_at,
    recipe,
  };
};

export const getAllCustomRecipes = async () => {
  const rows = await all('SELECT id, owner, name, description, recipe_json, created_at FROM custom_recipes');
  return rows.reduce((acc, row) => {
    let recipe;
    try {
      recipe = JSON.parse(row.recipe_json);
    } catch {
      recipe = null;
    }
    acc[row.id] = {
      owner: row.owner,
      name: row.name,
      description: row.description,
      createdAt: row.created_at,
      recipe,
    };
    return acc;
  }, {});
};

export const listCustomRecipesForSystem = async (systemId) => {
  const rows = await all(
    `SELECT id, name, description, owner
     FROM custom_recipes
     WHERE owner = ?
     ORDER BY created_at DESC, id ASC`,
    [systemId],
  );
  return rows.map((row) => ({
    id: row.id,
    name: row.name ?? row.id,
    description: row.description ?? '',
    owner: row.owner,
  }));
};
