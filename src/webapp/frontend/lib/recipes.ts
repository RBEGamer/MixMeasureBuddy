import { z } from 'zod';

export const recipeStepSchema = z.object({
  text: z
    .string()
    .trim()
    .max(280, 'Step notes should stay under 280 characters.')
    .or(z.literal('')),
  ingredient: z
    .string()
    .trim()
    .max(120, 'Ingredient names should stay under 120 characters.')
    .or(z.literal('')),
  amount: z
    .number({
      required_error: 'Provide an amount in milliliters (use -1 for n/a).',
      invalid_type_error: 'Amount must be a number.',
    })
    .finite(),
  action: z
    .number({
      required_error: 'Provide an action identifier.',
      invalid_type_error: 'Action must be a number.',
    })
    .int(),
});

export const recipeSchema = z.object({
  filename: z
    .string()
    .trim()
    .min(1, 'Filename is required.')
    .regex(/\.recipe$/i, 'Filename should end with .recipe'),
  name: z.string().trim().min(1, 'Give your recipe a display name.'),
  description: z
    .string()
    .trim()
    .min(1, 'Add a short description for the recipe.'),
  steps: z
    .array(recipeStepSchema)
    .min(1, 'Add at least one step to the recipe.'),
});

export type Recipe = z.infer<typeof recipeSchema>;
export type RecipeStep = z.infer<typeof recipeStepSchema>;

export const createEmptyStep = (): RecipeStep => ({
  text: '',
  ingredient: '',
  amount: -1,
  action: 0,
});

export const createEmptyRecipe = (): Recipe => ({
  filename: 'new_recipe.recipe',
  name: 'New Recipe',
  description: 'Describe what makes this recipe special.',
  steps: [createEmptyStep()],
});

export const RecipeAction = {
  SCALE: 0,
  CONFIRM: 1,
  WAIT: 2,
} as const;

export type RecipeActionValue =
  (typeof RecipeAction)[keyof typeof RecipeAction];

export const slugifyRecipeName = (name: string): string => {
  const base = name
    .trim()
    .replace(/['"]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_+/, '')
    .replace(/_+$/, '');

  const safeBase = base.length ? base : 'recipe';
  return safeBase.toLowerCase().endsWith('.recipe')
    ? safeBase
    : `${safeBase}.recipe`;
};

const encodeUTF8 = (data: string): string => {
  if (typeof window === 'undefined') {
    return Buffer.from(data, 'utf-8').toString('base64');
  }

  const encoder = new TextEncoder();
  const bytes = encoder.encode(data);
  let binary = '';
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary);
};

const decodeUTF8 = (data: string): string => {
  if (typeof window === 'undefined') {
    return Buffer.from(data, 'base64').toString('utf-8');
  }

  const binary = atob(data);
  const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
  const decoder = new TextDecoder();
  return decoder.decode(bytes);
};

export const encodeRecipe = (recipe: Recipe): string =>
  encodeUTF8(JSON.stringify(recipe, null, 4));

export const decodeRecipe = (payload: string): Recipe =>
  recipeSchema.parse(JSON.parse(decodeUTF8(payload)));

export const parseRecipeJson = (payload: string): Recipe =>
  recipeSchema.parse(JSON.parse(payload));

export const stringifyRecipe = (recipe: Recipe): string =>
  JSON.stringify(recipe, null, 2);
