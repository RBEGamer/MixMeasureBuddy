'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  recipeSchema,
  type Recipe,
  type RecipeStep,
  slugifyRecipeName,
  stringifyRecipe,
  RecipeAction,
  type RecipeActionValue,
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

const normalizeIngredientName = (value: string): string =>
  value
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[\u2019'’"]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

const toTitleCase = (value: string): string =>
  value
    .split(' ')
    .map((segment) =>
      segment.length > 0
        ? segment.charAt(0).toUpperCase() + segment.slice(1).toLowerCase()
        : '',
    )
    .join(' ');

const RAW_INGREDIENT_SYNONYMS: Record<string, string[]> = {
  Vodka: ['Premium Vodka', 'Plain Vodka'],
  Rum: ['White Rum', 'Dark Rum', 'Aged Rum', 'Spiced Rum'],
  Tequila: ['Blanco Tequila', 'Reposado Tequila', 'Añejo Tequila'],
  Gin: ['London Dry Gin', 'Dry Gin'],
  Whiskey: ['Whisky', 'Bourbon', 'Rye Whiskey', 'Scotch'],
  'Coffee Liqueur': ['Kahlua', 'Espresso Liqueur', 'Cold Brew Liqueur'],
  Espresso: ['Fresh Espresso', 'Double Espresso'],
  'Cold Brew': ['Cold Brew Coffee'],
  'Simple Syrup': ['Sugar Syrup', 'Syrup'],
  'Agave Syrup': ['Agave Nectar'],
  'Lime Juice': ['Fresh Lime Juice', 'Lime'],
  'Lemon Juice': ['Fresh Lemon Juice', 'Lemon'],
  'Orange Juice': ['Fresh Orange Juice'],
  'Orange Liqueur': ['Triple Sec', 'Cointreau', 'Orange Curaçao'],
  'Grapefruit Juice': ['Pink Grapefruit Juice'],
  'Pineapple Juice': ['Fresh Pineapple Juice'],
  'Coconut Cream': ['Cream of Coconut'],
  'Mint Leaves': ['Fresh Mint', 'Mint'],
  Bitters: ['Aromatic Bitters', 'Angostura Bitters'],
  'Sparkling Water': ['Soda Water', 'Club Soda'],
  'Tonic Water': ['Indian Tonic'],
};

const INGREDIENT_SYNONYMS: Record<string, string[]> = Object.entries(
  RAW_INGREDIENT_SYNONYMS,
).reduce<Record<string, string[]>>((acc, [key, values]) => {
  const normalizedKey = normalizeIngredientName(key);
  if (!normalizedKey) {
    return acc;
  }
  const normalizedValues = Array.from(
    new Set(values.map((value) => normalizeIngredientName(value)).filter(Boolean)),
  );
  acc[normalizedKey] = normalizedValues;
  return acc;
}, {});

type IngredientVariantIndex = {
  canonical: string[];
  variantSet: Set<string>;
  variantToCanonical: Map<string, string>;
};

const buildIngredientVariantIndex = (ingredients: string[]): IngredientVariantIndex => {
  const canonicalSet = new Set<string>();
  const variantSet = new Set<string>();
  const variantToCanonical = new Map<string, string>();

  ingredients.forEach((ingredient) => {
    const normalized = normalizeIngredientName(ingredient);
    if (!normalized) return;

    canonicalSet.add(normalized);

    const synonyms = INGREDIENT_SYNONYMS[normalized] ?? [];
    const variants = new Set<string>([normalized, ...synonyms]);
    variants.forEach((variant) => {
      if (!variant) return;
      variantSet.add(variant);
      if (!variantToCanonical.has(variant)) {
        variantToCanonical.set(variant, normalized);
      }
    });
  });

  return {
    canonical: Array.from(canonicalSet),
    variantSet,
    variantToCanonical,
  };
};

const collectMatchingVariants = (
  normalizedIngredient: string,
  variants: Set<string>,
): string[] => {
  if (!normalizedIngredient) {
    return [];
  }

  const matches: string[] = [];
  variants.forEach((variant) => {
    if (!variant) return;
    if (
      normalizedIngredient === variant ||
      normalizedIngredient.includes(variant) ||
      variant.includes(normalizedIngredient)
    ) {
      matches.push(variant);
    }
  });
  return matches;
};

type IndexedMixerStep = RecipeStep & {
  sourceRecipe: string;
  sourceIndex: number;
  globalIndex: number;
  normalizedIngredient: string;
};

type ScoredMixerStep = {
  step: IndexedMixerStep;
  matches: Set<string>;
  score: number;
};

const ACTION_PRIORITY: Record<RecipeActionValue, number> = {
  [RecipeAction.SCALE]: 3,
  [RecipeAction.WAIT]: 2,
  [RecipeAction.CONFIRM]: 1,
};

const ACTION_WEIGHT: Record<RecipeActionValue, number> = {
  [RecipeAction.SCALE]: 3,
  [RecipeAction.WAIT]: 1.5,
  [RecipeAction.CONFIRM]: 1,
};

const MAX_GENERATED_STEPS = 16;
const MIN_GENERATED_STEPS = 5;

const parseIngredientList = (raw: string): string[] =>
  raw
    .split(/[\n,]+/)
    .map((entry) => normalizeIngredientName(entry))
    .filter((entry) => entry.length > 0);

const cloneStep = (step: RecipeStep): RecipeStep =>
  JSON.parse(JSON.stringify(step));

const flattenRecipeSteps = (recipes: Recipe[]): IndexedMixerStep[] => {
  const flattened: IndexedMixerStep[] = [];
  let globalIndex = 0;

  recipes.forEach((recipe) => {
    recipe.steps.forEach((step, sourceIndex) => {
      const copy = cloneStep(step);
      flattened.push({
        ...copy,
        sourceRecipe: recipe.name,
        sourceIndex,
        globalIndex: globalIndex++,
        normalizedIngredient: normalizeIngredientName(copy.ingredient ?? ''),
      });
    });
  });

  return flattened;
};

const DEFAULT_RECIPE_NAME = 'Custom Coffee Lab Mix';

const createRecipeNameFromIngredients = (ingredients: string[]): string => {
  if (ingredients.length === 0) {
    return DEFAULT_RECIPE_NAME;
  }

  const unique = Array.from(new Set(ingredients));
  unique.sort((a, b) => a.localeCompare(b));

  const first = unique[0];
  const second = unique[1];

  if (first && second) {
    return `${toTitleCase(first)} ${toTitleCase(second)} Fusion`;
  }

  if (first) {
    return `${toTitleCase(first)} Custom Blend`;
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
      try {
        const flattened = flattenRecipeSteps(state.samples);
        if (flattened.length === 0) {
          setGeneratedRecipe(null);
          return;
        }

        const variantIndex = buildIngredientVariantIndex(ingredientBadges);
        const trimmedName = desiredName.trim();
        const fallbackName =
          trimmedName.length > 0
            ? trimmedName
            : createRecipeNameFromIngredients(ingredientBadges);

        if (variantIndex.canonical.length === 0) {
          const fallbackSteps = flattened.slice(0, MIN_GENERATED_STEPS).map((step) => ({
            text: step.text,
            ingredient: step.ingredient,
            amount: step.amount,
            action: step.action,
          }));

          const recipe: Recipe = {
            filename: slugifyRecipeName(fallbackName),
            name: fallbackName,
            description:
              'A quick sample pulled from the MixMeasureBuddy library. Add ingredients to tailor the mix to your bar.',
            steps: fallbackSteps,
          };

          setGeneratedRecipe(recipe);
          return;
        }

        const scoredSteps: ScoredMixerStep[] = flattened.map((step) => {
          const variantMatches = collectMatchingVariants(
            step.normalizedIngredient,
            variantIndex.variantSet,
          );
          const canonicalMatches = new Set<string>();
          variantMatches.forEach((variant) => {
            const canonical = variantIndex.variantToCanonical.get(variant);
            if (canonical) {
              canonicalMatches.add(canonical);
            }
          });

          const matchScore = canonicalMatches.size * 3;
          const actionWeight = ACTION_WEIGHT[step.action as RecipeActionValue] ?? 0;
          const score = matchScore + actionWeight;

          return {
            step,
            matches: canonicalMatches,
            score,
          };
        });

        const matchedSteps = scoredSteps.filter((entry) => entry.matches.size > 0);

        const sortedMatched = [...matchedSteps].sort((a, b) => {
          if (b.score !== a.score) return b.score - a.score;
          const priorityDiff =
            ACTION_PRIORITY[b.step.action as RecipeActionValue] -
            ACTION_PRIORITY[a.step.action as RecipeActionValue];
          if (priorityDiff !== 0) return priorityDiff;
          return a.step.globalIndex - b.step.globalIndex;
        });

        const selectedEntries: ScoredMixerStep[] = [];
        const selectedIndices = new Set<number>();
        const coverage = new Set<string>();

        variantIndex.canonical.forEach((ingredient) => {
          const candidate = sortedMatched.find(
            (entry) =>
              entry.matches.has(ingredient) && !selectedIndices.has(entry.step.globalIndex),
          );
          if (candidate) {
            selectedEntries.push(candidate);
            selectedIndices.add(candidate.step.globalIndex);
            candidate.matches.forEach((match) => coverage.add(match));
          }
        });

        for (const entry of sortedMatched) {
          if (selectedEntries.length >= MAX_GENERATED_STEPS) break;
          if (selectedIndices.has(entry.step.globalIndex)) continue;
          selectedEntries.push(entry);
          selectedIndices.add(entry.step.globalIndex);
          entry.matches.forEach((match) => coverage.add(match));
        }

        const missingIngredients = variantIndex.canonical.filter(
          (ingredient) => !coverage.has(ingredient),
        );

        missingIngredients.forEach((ingredient) => {
          const ingredientVariants = new Set<string>([
            ingredient,
            ...(INGREDIENT_SYNONYMS[ingredient] ?? []),
          ]);

          const fallback = flattened.find(
            (step) =>
              !selectedIndices.has(step.globalIndex) &&
              collectMatchingVariants(step.normalizedIngredient, ingredientVariants).length > 0,
          );

          if (fallback) {
            selectedEntries.push({
              step: fallback,
              matches: new Set([ingredient]),
              score: ACTION_WEIGHT[fallback.action as RecipeActionValue] ?? 0,
            });
            selectedIndices.add(fallback.globalIndex);
            coverage.add(ingredient);
          }
        });

        if (selectedEntries.length < MIN_GENERATED_STEPS) {
          for (const step of flattened) {
            if (selectedEntries.length >= MIN_GENERATED_STEPS) break;
            if (selectedIndices.has(step.globalIndex)) continue;
            selectedEntries.push({
              step,
              matches: new Set(),
              score: ACTION_WEIGHT[step.action as RecipeActionValue] ?? 0,
            });
            selectedIndices.add(step.globalIndex);
          }
        }

        const waitCandidates = flattened
          .filter(
            (step) =>
              (step.action === RecipeAction.WAIT || step.action === RecipeAction.CONFIRM) &&
              !selectedIndices.has(step.globalIndex),
          )
          .sort((a, b) => a.globalIndex - b.globalIndex);

        const needsWait = !selectedEntries.some(
          (entry) => entry.step.action === RecipeAction.WAIT,
        );
        if (needsWait) {
          const candidate = waitCandidates.find((step) => step.action === RecipeAction.WAIT);
          if (candidate && selectedEntries.length < MAX_GENERATED_STEPS) {
            selectedEntries.push({
              step: candidate,
              matches: new Set(),
              score: ACTION_WEIGHT[candidate.action as RecipeActionValue] ?? 0,
            });
            selectedIndices.add(candidate.globalIndex);
          }
        }

        const needsConfirm = !selectedEntries.some(
          (entry) => entry.step.action === RecipeAction.CONFIRM,
        );
        if (needsConfirm) {
          const candidate = waitCandidates.find(
            (step) =>
              step.action === RecipeAction.CONFIRM && !selectedIndices.has(step.globalIndex),
          );
          if (candidate && selectedEntries.length < MAX_GENERATED_STEPS) {
            selectedEntries.push({
              step: candidate,
              matches: new Set(),
              score: ACTION_WEIGHT[candidate.action as RecipeActionValue] ?? 0,
            });
            selectedIndices.add(candidate.globalIndex);
          }
        }

        const finalSteps: RecipeStep[] = [];
        const seenKeys = new Set<string>();

        selectedEntries
          .sort((a, b) => a.step.globalIndex - b.step.globalIndex)
          .forEach(({ step }) => {
            const key = `${step.action}-${step.ingredient}-${step.text}-${step.amount}`;
            if (seenKeys.has(key)) return;
            seenKeys.add(key);
            finalSteps.push({
              text: step.text,
              ingredient: step.ingredient,
              amount: step.amount,
              action: step.action,
            });
          });

        if (finalSteps.length === 0) {
          const fallbackSteps = flattened.slice(0, MIN_GENERATED_STEPS).map((step) => ({
            text: step.text,
            ingredient: step.ingredient,
            amount: step.amount,
            action: step.action,
          }));
          finalSteps.push(...fallbackSteps);
        }

        const recipe: Recipe = {
          filename: slugifyRecipeName(fallbackName),
          name: fallbackName,
          description:
            'A custom recipe assembled from the MixMeasureBuddy library based on your available ingredients.',
          steps: finalSteps.slice(0, MAX_GENERATED_STEPS),
        };

        setGeneratedRecipe(recipe);
      } finally {
        setIsGenerating(false);
      }
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
                    {toTitleCase(ingredient)}
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
