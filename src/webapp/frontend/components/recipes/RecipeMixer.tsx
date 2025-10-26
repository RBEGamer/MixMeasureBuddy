'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  recipeSchema,
  type Recipe,
  type RecipeStep,
  slugifyRecipeName,
  stringifyRecipe,
} from '@/lib/recipes';
import { withBasePath } from '@/lib/base-path';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/shared/ui/card';
import { Input } from '@/components/shared/ui/input';
import { Textarea } from '@/components/shared/ui/textarea';
import { Button } from '@/components/shared/ui/button';
import { Badge } from '@/components/shared/ui/badge';
import { Separator } from '@/components/shared/ui/separator';
import { Loader2, Wand2 } from 'lucide-react';

type MixerState = {
  loading: boolean;
  error: string | null;
  samples: Recipe[];
};

const SAMPLE_DATA_ENDPOINT = withBasePath('/data/sample-recipes.json');

const parseIngredientList = (raw: string): string[] =>
  raw
    .split(/[\n,]+/)
    .map((entry) => entry.trim().toLowerCase())
    .filter((entry) => entry.length > 0);

const cloneStep = (step: RecipeStep): RecipeStep =>
  JSON.parse(JSON.stringify(step));

const flattenRecipeSteps = (recipes: Recipe[]): RecipeStep[] =>
  recipes.flatMap((recipe) =>
    recipe.steps.map((step) => ({
      ...cloneStep(step),
      sourceRecipe: recipe.name,
    })),
  );

const DEFAULT_RECIPE_NAME = 'Custom Coffee Lab Mix';

const createRecipeNameFromIngredients = (ingredients: string[]): string => {
  if (ingredients.length === 0) {
    return DEFAULT_RECIPE_NAME;
  }

  const unique = Array.from(new Set(ingredients));
  unique.sort((a, b) => a.localeCompare(b));

  const first = unique[0];
  const second = unique[1];

  const formatWord = (word: string) => {
    if (!word || word.length === 0) {
      return '';
    }
    return word
      .split(' ')
      .map((segment) =>
        segment.length > 0
          ? segment.charAt(0).toUpperCase() + segment.slice(1).toLowerCase()
          : '',
      )
      .join(' ');
  };

  if (first && second) {
    return `${formatWord(first)} ${formatWord(second)} Fusion`;
  }

  if (first) {
    return `${formatWord(first)} Custom Blend`;
  }

  return DEFAULT_RECIPE_NAME;
};

export const RecipeMixer = () => {
  const [state, setState] = useState<MixerState>({
    loading: true,
    error: null,
    samples: [],
  });

  const [ingredientInput, setIngredientInput] = useState<string>('');
  const [desiredName, setDesiredName] = useState<string>('My Home Bar Creation');
  const [generatedRecipe, setGeneratedRecipe] = useState<Recipe | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  const recipeNameId = 'recipe-mixer-name';
  const ingredientInputId = 'recipe-mixer-ingredients';

  useEffect(() => {
    let active = true;
    const loadSamples = async () => {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      try {
        const response = await fetch(SAMPLE_DATA_ENDPOINT, {
          cache: 'force-cache',
        });
        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
        }
        const json = await response.json();
        const parsed = recipeSchema.array().safeParse(json);
        if (!parsed.success) {
          throw new Error('Sample recipe validation failed');
        }
        if (active) {
          setState({
            loading: false,
            error: null,
            samples: parsed.data,
          });
        }
      } catch (error) {
        if (active) {
          setState({
            loading: false,
            error:
              error instanceof Error
                ? error.message
                : 'Unable to load sample recipes.',
            samples: [],
          });
        }
      }
    };

    loadSamples();
    return () => {
      active = false;
    };
  }, []);

  const availableIngredients = useMemo(
    () => parseIngredientList(ingredientInput),
    [ingredientInput],
  );

  const ingredientBadges = useMemo(() => {
    const unique = Array.from(new Set(availableIngredients));
    unique.sort();
    return unique;
  }, [availableIngredients]);

  const generateRecipe = () => {
    if (state.samples.length === 0) {
      setGeneratedRecipe(null);
      return;
    }

    setIsGenerating(true);

    requestAnimationFrame(() => {
      const flattened = flattenRecipeSteps(state.samples);

      const filteredSteps = flattened.filter((step) => {
        if (!step.ingredient || step.ingredient.trim().length === 0) {
          return true;
        }

        const normalized = step.ingredient.trim().toLowerCase();
        return availableIngredients.includes(normalized);
      });

      const limitedSteps = filteredSteps.slice(0, 18);

      if (limitedSteps.length === 0) {
        // fallback: take first five steps regardless, so user still gets a recipe
        limitedSteps.push(...flattened.slice(0, 5));
      }

      const deduplicated = limitedSteps.reduce<RecipeStep[]>(
        (acc, step) => {
          const key = `${step.action}-${step.ingredient}-${step.text}-${step.amount}`;
          if (!acc.some((existing) => key === `${existing.action}-${existing.ingredient}-${existing.text}-${existing.amount}`)) {
            acc.push({
              text: step.text,
              ingredient: step.ingredient,
              amount: step.amount,
              action: step.action,
            });
          }
          return acc;
        },
        [],
      );

      const fallbackName = createRecipeNameFromIngredients(ingredientBadges);
      const finalName =
        desiredName.trim().length > 0 ? desiredName.trim() : fallbackName;

      const recipe: Recipe = {
        filename: slugifyRecipeName(finalName),
        name: finalName,
        description:
          'A custom recipe assembled from the MixMeasureBuddy library based on your available ingredients.',
        steps: deduplicated,
      };

      setGeneratedRecipe(recipe);
      setIsGenerating(false);
    });
  };

  const handleDownload = () => {
    if (!generatedRecipe) {
      return;
    }
    const blob = new Blob([stringifyRecipe(generatedRecipe)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = generatedRecipe.filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Create a recipe with what you have</CardTitle>
          <CardDescription>
            List the ingredients you can use at home. We&apos;ll stitch together
            compatible steps from the built-in recipe library so you can keep
            experimenting without hunting for missing bottles.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="flex flex-col gap-2">
              <label
                className="text-sm font-medium text-foreground"
                htmlFor={ingredientInputId}
              >
                List ingredients (comma or line separated)
              </label>
              <Textarea
                placeholder="Vodka, Coffee Liqueur, Lime Juice, Simple Syrup"
                value={ingredientInput}
                id={ingredientInputId}
                onChange={(event) => setIngredientInput(event.target.value)}
                className="min-h-[96px]"
              />
              <p className="text-xs text-muted-foreground">
                Tip: include flavorful extras like syrups or garnishes so we can
                weave those steps in too.
              </p>
            </div>

            <div className="flex flex-col gap-2">
              <label
                className="text-sm font-medium text-foreground"
                htmlFor={recipeNameId}
              >
                Recipe name (optional)
              </label>
              <Input
                placeholder="Auto-generated"
                value={desiredName}
                id={recipeNameId}
                onChange={(event) => setDesiredName(event.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                Leave blank to let Mix Lab build a title from your ingredients.
              </p>
            </div>
          </div>

          <Separator />

          <div className="flex flex-col gap-3">
            <span className="text-sm font-medium text-foreground">
              Recognised ingredients
            </span>
            {ingredientBadges.length === 0 ? (
              <div className="rounded-md border border-dashed p-4 text-sm text-muted-foreground">
                Add ingredients above to see them here.
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {ingredientBadges.map((ingredient) => (
                  <Badge key={ingredient} variant="outline">
                    {ingredient}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-3">
            <Button
              type="button"
              onClick={generateRecipe}
              disabled={state.loading || isGenerating}
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Mixing steps…
                </>
              ) : (
                <>
                  <Wand2 className="mr-2 h-4 w-4" />
                  Generate recipe
                </>
              )}
            </Button>
            <Button
              type="button"
              variant="outlinePrimary"
              disabled={!generatedRecipe}
              onClick={handleDownload}
            >
              Download .recipe
            </Button>
          </div>

          {state.loading && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading library…
            </div>
          )}
          {state.error && (
            <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">
              {state.error}
            </div>
          )}
        </CardContent>
      </Card>

      {generatedRecipe && (
        <Card>
          <CardHeader>
            <CardTitle>{generatedRecipe.name}</CardTitle>
            <CardDescription>
              {generatedRecipe.description} Save the file above to edit or load it
              on your MixMeasureBuddy.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-wrap gap-3">
              <Badge variant="outline">
                {generatedRecipe.steps.length} steps assembled
              </Badge>
              <Badge variant="outline">{generatedRecipe.filename}</Badge>
            </div>
            <ol className="space-y-3 text-sm">
              {generatedRecipe.steps.map((step, index) => (
                <li
                  key={`${step.ingredient}-${index}`}
                  className="rounded-md border border-dashed p-3"
                >
                  <span className="font-semibold text-foreground">
                    Step {index + 1}:{' '}
                  </span>
                  <span>
                    {step.text && step.text.length > 0
                      ? step.text
                      : 'Follow device instructions.'}
                  </span>
                  {step.ingredient && step.ingredient.length > 0 && (
                    <div className="mt-1 text-xs text-muted-foreground">
                      Ingredient: {step.ingredient}{' '}
                      {step.amount > 0 ? `(${step.amount})` : ''}
                    </div>
                  )}
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
