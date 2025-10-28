'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button } from '@/components/shared/ui/button';
import { Badge } from '@/components/shared/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/shared/ui/card';
import { ScrollArea } from '@/components/shared/ui/scroll-area';
import { Separator } from '@/components/shared/ui/separator';
import { Input } from '@/components/shared/ui/input';
import { Textarea } from '@/components/shared/ui/textarea';
import { Loader2, PlusCircle, Trash2, Share2 } from 'lucide-react';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';

interface RecipeAssignmentManagerProps {
  systemId: string;
}

interface AvailableRecipesResponse {
  recipes: string[];
}

interface AssignedRecipesResponse {
  recipes: string[];
}

interface CustomRecipeSummary {
  id: string;
  name: string;
  description?: string;
  owner?: string;
}

interface CustomRecipesResponse {
  systemId: string;
  recipes: CustomRecipeSummary[];
}

const fetchJSON = async <T,>(endpoint: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(endpoint, options);
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Request failed with status ${response.status}: ${body}`);
  }
  return response.json();
};

const normalizeRecipeId = (recipe: string) =>
  recipe.endsWith('.recipe') ? recipe : `${recipe}.recipe`;

const DEFAULT_STEPS = `[
  {
    "text": "Add ingredient description",
    "ingredient": "Example Ingredient",
    "amount": 50,
    "action": 0
  },
  {
    "text": "Stir or shake as needed",
    "ingredient": "",
    "amount": 10,
    "action": 2
  }
]`;

export default function RecipeAssignmentManager({ systemId }: RecipeAssignmentManagerProps) {
  const [available, setAvailable] = useState<string[]>([]);
  const [assigned, setAssigned] = useState<string[]>([]);
  const [customRecipes, setCustomRecipes] = useState<CustomRecipeSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const [newRecipeName, setNewRecipeName] = useState('My Custom Mix');
  const [newRecipeDescription, setNewRecipeDescription] = useState('Describe what makes this recipe special.');
  const [newRecipeSteps, setNewRecipeSteps] = useState(DEFAULT_STEPS);
  const [assignById, setAssignById] = useState('');

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [availableData, assignedData, customData] = await Promise.all([
        fetchJSON<AvailableRecipesResponse>(`${BACKEND_URL}/recipes/available`),
        fetchJSON<AssignedRecipesResponse>(`${BACKEND_URL}/recipes/assigned/${systemId}`),
        fetchJSON<CustomRecipesResponse>(`${BACKEND_URL}/recipes/custom/${systemId}`),
      ]);
      setAvailable(availableData.recipes ?? []);
      setAssigned(assignedData.recipes ?? []);
      setCustomRecipes(customData.recipes ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load recipes.');
    } finally {
      setLoading(false);
    }
  }, [systemId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const availableToAssign = useMemo(
    () => available.filter((recipe) => !assigned.includes(normalizeRecipeId(recipe))),
    [available, assigned],
  );

  const ownerCustomIds = useMemo(() => customRecipes.map((recipe) => recipe.id), [customRecipes]);

  const customAvailable = useMemo(
    () => ownerCustomIds.filter((id) => !assigned.includes(id)),
    [ownerCustomIds, assigned],
  );

  const handleAddRecipe = async (recipe: string) => {
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      const normalized = normalizeRecipeId(recipe);
      await fetchJSON(`${BACKEND_URL}/recipes/assigned/${systemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe: normalized }),
      });
      await loadData();
      setInfo(`Assigned ${normalized} to ${systemId}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to assign recipe.');
      setLoading(false);
    }
  };

  const handleRemoveRecipe = async (recipe: string) => {
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      await fetchJSON(`${BACKEND_URL}/recipes/assigned/${systemId}/${encodeURIComponent(recipe)}`, {
        method: 'DELETE',
      });
      await loadData();
      setInfo(`Removed ${recipe} from ${systemId}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove recipe.');
      setLoading(false);
    }
  };

  const handleCreateCustomRecipe = async () => {
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      const steps = JSON.parse(newRecipeSteps);
      if (!Array.isArray(steps)) {
        throw new Error('Steps must be a JSON array.');
      }
      const recipePayload = {
        name: newRecipeName,
        description: newRecipeDescription,
        version: '1.0.0',
        steps,
      };
      const response = await fetchJSON<{ recipeId: string }>(`${BACKEND_URL}/recipes/custom/${systemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newRecipeName, recipe: recipePayload }),
      });
      await loadData();
      setInfo(`Created custom recipe ${response.recipeId}. Share this ID to let others add it.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create custom recipe.');
    } finally {
      setLoading(false);
    }
  };

  const handleAssignById = async () => {
    if (!assignById.trim()) {
      setError('Enter a recipe ID to assign.');
      return;
    }
    await handleAddRecipe(assignById.trim());
    setAssignById('');
  };

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Scale overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
            <Badge variant="outline">Scale ID: {systemId}</Badge>
            <Badge variant="outline">Assigned: {assigned.length}</Badge>
            <Badge variant="outline">Library: {available.length}</Badge>
            <Badge variant="outline">Custom recipes: {customRecipes.length}</Badge>
          </div>
          <Separator />
          {info && (
            <div className="rounded-md border border-primary-300/60 bg-primary-50 p-3 text-sm text-primary-800 dark:border-primary-700/50 dark:bg-primary-900/30 dark:text-primary-100">
              {info}
            </div>
          )}
          {loading ? (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              Syncing with backend…
            </div>
          ) : error ? (
            <div className="rounded-md border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
              {error}
            </div>
          ) : (
            <div className="grid gap-6 lg:grid-cols-3">
              <section className="flex flex-col gap-4">
                <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  Assigned recipes
                </h2>
                <ScrollArea className="h-64 rounded-lg border border-primary-100/60 bg-background/70 p-3 dark:border-primary-900/40">
                  {assigned.length === 0 ? (
                    <p className="text-sm text-muted-foreground">
                      No recipes assigned yet.
                    </p>
                  ) : (
                    <ul className="flex flex-col gap-2">
                      {assigned.map((name) => (
                        <li
                          key={name}
                          className="flex items-center justify-between rounded-md border border-dashed px-3 py-2 text-sm"
                        >
                          <span>{name}</span>
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={() => handleRemoveRecipe(name)}
                          >
                            <Trash2 className="mr-1 h-4 w-4" />
                            Remove
                          </Button>
                        </li>
                      ))}
                    </ul>
                  )}
                </ScrollArea>
              </section>

              <section className="flex flex-col gap-4">
                <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  Library recipes
                </h2>
                <ScrollArea className="h-64 rounded-lg border border-primary-100/60 bg-background/70 p-3 dark:border-primary-900/40">
                  {availableToAssign.length === 0 ? (
                    <p className="text-sm text-muted-foreground">
                      All library recipes are assigned.
                    </p>
                  ) : (
                    <ul className="flex flex-col gap-2">
                      {availableToAssign.map((name) => (
                        <li
                          key={name}
                          className="flex items-center justify-between rounded-md border border-dashed px-3 py-2 text-sm"
                        >
                          <span>{name}</span>
                          <Button
                            type="button"
                            variant="outlinePrimary"
                            size="sm"
                            onClick={() => handleAddRecipe(name)}
                          >
                            <PlusCircle className="mr-1 h-4 w-4" />
                            Assign
                          </Button>
                        </li>
                      ))}
                    </ul>
                  )}
                </ScrollArea>
              </section>

              <section className="flex flex-col gap-4">
                <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  Your custom recipes
                </h2>
                <ScrollArea className="h-64 rounded-lg border border-primary-100/60 bg-background/70 p-3 dark:border-primary-900/40">
                  {customRecipes.length === 0 ? (
                    <p className="text-sm text-muted-foreground">
                      Create a custom recipe below to see it here.
                    </p>
                  ) : (
                    <ul className="flex flex-col gap-2">
                      {customRecipes.map((recipe) => (
                        <li
                          key={recipe.id}
                          className="rounded-md border border-dashed px-3 py-2 text-sm"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-medium">{recipe.name}</span>
                            <Badge variant="outline">
                              <Share2 className="mr-1 h-3 w-3" />
                              {recipe.id}
                            </Badge>
                          </div>
                          {recipe.description && (
                            <p className="mt-1 text-xs text-muted-foreground">
                              {recipe.description}
                            </p>
                          )}
                          {!assigned.includes(recipe.id) && (
                            <div className="mt-2 flex justify-end">
                              <Button
                                type="button"
                                size="sm"
                                variant="outlinePrimary"
                                onClick={() => handleAddRecipe(recipe.id)}
                              >
                                <PlusCircle className="mr-1 h-4 w-4" /> Assign
                              </Button>
                            </div>
                          )}
                        </li>
                      ))}
                    </ul>
                  )}
                </ScrollArea>
                <div className="flex flex-col gap-2">
                  <label
                    htmlFor="assign-recipe-id"
                    className="text-xs font-semibold uppercase tracking-wide text-muted-foreground"
                  >
                    Assign by recipe ID
                  </label>
                  <div className="flex flex-col gap-2 sm:flex-row">
                    <Input
                      id="assign-recipe-id"
                      value={assignById}
                      onChange={(event) => setAssignById(event.target.value)}
                      placeholder="scale-custom-recipe-id.recipe"
                    />
                    <Button type="button" variant="outline" onClick={handleAssignById}>
                      Assign ID
                    </Button>
                  </div>
                </div>
              </section>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Create a custom recipe</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="flex flex-col gap-2">
              <label
                htmlFor="custom-recipe-name"
                className="text-sm font-medium text-muted-foreground"
              >
                Recipe name
              </label>
              <Input
                id="custom-recipe-name"
                value={newRecipeName}
                onChange={(event) => setNewRecipeName(event.target.value)}
                placeholder="My Custom Mix"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label
                htmlFor="custom-recipe-description"
                className="text-sm font-medium text-muted-foreground"
              >
                Description
              </label>
              <Textarea
                id="custom-recipe-description"
                value={newRecipeDescription}
                onChange={(event) => setNewRecipeDescription(event.target.value)}
                placeholder="Describe what this recipe does."
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="custom-recipe-steps"
              className="text-sm font-medium text-muted-foreground"
            >
              Steps (JSON array)
            </label>
            <Textarea
              id="custom-recipe-steps"
              className="font-mono text-xs"
              rows={8}
              value={newRecipeSteps}
              onChange={(event) => setNewRecipeSteps(event.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              Provide an array of step objects matching the MixMeasureBuddy format.
              Each step can include <code>text</code>, <code>ingredient</code>, <code>amount</code>, and <code>action</code>.
            </p>
          </div>

          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={() => setNewRecipeSteps(DEFAULT_STEPS)}>
              Reset steps
            </Button>
            <Button type="button" onClick={handleCreateCustomRecipe}>
              Create recipe
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
