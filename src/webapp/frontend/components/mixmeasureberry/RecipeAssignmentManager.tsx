'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button } from '@/components/shared/ui/button';
import { Badge } from '@/components/shared/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/shared/ui/card';
import { ScrollArea } from '@/components/shared/ui/scroll-area';
import { Separator } from '@/components/shared/ui/separator';
import { Loader2, PlusCircle, Trash2 } from 'lucide-react';

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

const fetchJSON = async <T,>(endpoint: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(endpoint, options);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
};

export default function RecipeAssignmentManager({ systemId }: RecipeAssignmentManagerProps) {
  const [available, setAvailable] = useState<string[]>([]);
  const [assigned, setAssigned] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [availableData, assignedData] = await Promise.all([
        fetchJSON<AvailableRecipesResponse>(`${BACKEND_URL}/recipes/available`),
        fetchJSON<AssignedRecipesResponse>(`${BACKEND_URL}/recipes/assigned/${systemId}`),
      ]);
      setAvailable(availableData.recipes ?? []);
      setAssigned(assignedData.recipes ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load recipes.');
    } finally {
      setLoading(false);
    }
  }, [systemId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const availableToAssign = useMemo(() =>
    available.filter((recipe) => !assigned.includes(recipe)),
  [available, assigned]);

  const handleAddRecipe = async (recipe: string) => {
    setLoading(true);
    setError(null);
    try {
      await fetchJSON(`${BACKEND_URL}/recipes/assigned/${systemId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe }),
      });
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to assign recipe.');
      setLoading(false);
    }
  };

  const handleRemoveRecipe = async (recipe: string) => {
    setLoading(true);
    setError(null);
    try {
      await fetchJSON(`${BACKEND_URL}/recipes/assigned/${systemId}/${encodeURIComponent(recipe)}`, {
        method: 'DELETE',
      });
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove recipe.');
      setLoading(false);
    }
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
            <Badge variant="outline">Available: {available.length}</Badge>
          </div>
          <Separator />
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
            <div className="grid gap-6 md:grid-cols-2">
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
                  Available recipes
                </h2>
                <ScrollArea className="h-64 rounded-lg border border-primary-100/60 bg-background/70 p-3 dark:border-primary-900/40">
                  {availableToAssign.length === 0 ? (
                    <p className="text-sm text-muted-foreground">
                      All recipes are currently assigned.
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
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
