'use client';

import { useMemo, useState } from 'react';
import { Recipe } from '@/lib/recipes';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/shared/ui/card';
import { Badge } from '@/components/shared/ui/badge';
import { Input } from '@/components/shared/ui/input';
import { Search } from 'lucide-react';
import { Button } from '@/components/shared/ui/button';

const summarizeIngredients = (recipe: Recipe) => {
  const uniques = new Set(
    recipe.steps
      .map((step) => step.ingredient?.trim())
      .filter((ingredient) => ingredient && ingredient.length > 0),
  );
  return Array.from(uniques);
};

const downloadRecipe = (recipe: Recipe) => {
  const blob = new Blob([JSON.stringify(recipe, null, 2)], {
    type: 'application/json',
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = recipe.filename ?? 'recipe.recipe';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export const RecipeGalleryGrid = ({ recipes }: { recipes: Recipe[] }) => {
  const [query, setQuery] = useState<string>('');

  const filteredRecipes = useMemo(() => {
    if (!query.trim().length) {
      return recipes;
    }
    const normalized = query.trim().toLowerCase();
    return recipes.filter((recipe) => {
      const haystack = [
        recipe.name,
        recipe.filename,
        recipe.description,
        ...recipe.steps.map((step) => step.ingredient ?? ''),
      ]
        .join(' ')
        .toLowerCase();
      return haystack.includes(normalized);
    });
  }, [query, recipes]);

  return (
    <div className="flex flex-col gap-6">
      <div className="relative">
        <Input
          placeholder="Search by name, ingredient, or description..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="pl-10"
        />
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      </div>

      {filteredRecipes.length === 0 ? (
        <div className="rounded-xl border border-dashed p-8 text-center text-muted-foreground">
          No recipes match “{query}”.
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredRecipes.map((recipe) => {
            const ingredients = summarizeIngredients(recipe);
            return (
              <Card
                key={recipe.filename}
                className="flex h-full flex-col justify-between"
              >
                <CardHeader>
                  <CardTitle className="text-xl font-semibold">
                    {recipe.name}
                  </CardTitle>
                  <CardDescription className="line-clamp-3">
                    {recipe.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-1 flex-col gap-4">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline">
                      {recipe.steps.length} step
                      {recipe.steps.length === 1 ? '' : 's'}
                    </Badge>
                    <Badge variant="outline">{recipe.filename}</Badge>
                  </div>

                  {ingredients.length > 0 && (
                    <div className="flex flex-col gap-2">
                      <h3 className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
                        Key ingredients
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {ingredients.slice(0, 6).map((ingredient) => (
                          <Badge key={ingredient} variant="secondary">
                            {ingredient}
                          </Badge>
                        ))}
                        {ingredients.length > 6 && (
                          <Badge variant="secondary">
                            +{ingredients.length - 6} more
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  <details className="rounded-md border border-dashed bg-muted/30 p-3 text-sm">
                    <summary className="cursor-pointer select-none font-medium">
                      Step overview
                    </summary>
                    <ol className="mt-3 space-y-2 pl-4">
                      {recipe.steps.slice(0, 4).map((step, index) => (
                        <li key={`${recipe.filename}-step-${index}`}>
                          <span className="font-semibold">
                            {step.ingredient ? `${step.ingredient}: ` : ''}
                          </span>
                          <span>
                            {step.text && step.text.length
                              ? step.text
                              : 'See device for instruction.'}
                          </span>
                        </li>
                      ))}
                      {recipe.steps.length > 4 && (
                        <li className="italic text-muted-foreground">
                          …{recipe.steps.length - 4} more step
                          {recipe.steps.length - 4 === 1 ? '' : 's'}
                        </li>
                      )}
                    </ol>
                  </details>

                  <Button
                    variant="outlinePrimary"
                    className="mt-auto"
                    onClick={() => downloadRecipe(recipe)}
                  >
                    Download .recipe
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
