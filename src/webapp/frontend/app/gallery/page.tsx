import { Metadata } from 'next';
import path from 'path';
import { promises as fs } from 'fs';
import { Badge } from '@/components/shared/ui/badge';
import { recipeSchema, type Recipe } from '@/lib/recipes';
import { RecipeGalleryGrid } from '@/components/recipes/RecipeGalleryGrid';

export const metadata: Metadata = {
  title: 'Recipe Gallery · MixMeasureBuddy',
  description:
    'Browse every MixMeasureBuddy cocktail recipe bundled with the firmware and download your favourites as .recipe files.',
};

const SAMPLE_DATA_PATH = path.join(
  process.cwd(),
  'public',
  'data',
  'sample-recipes.json',
);

const readSampleRecipes = async (): Promise<Recipe[]> => {
  try {
    const raw = await fs.readFile(SAMPLE_DATA_PATH, 'utf8');
    const json = JSON.parse(raw);
    const parsed = recipeSchema.array().safeParse(json);
    if (!parsed.success) {
      console.warn(
        '[RecipeGallery] Sample recipes failed validation:',
        parsed.error.message,
      );
      return [];
    }
    return parsed.data;
  } catch (error) {
    console.warn('[RecipeGallery] Unable to read sample recipes:', error);
    return [];
  }
};

export default async function RecipeGalleryPage() {
  const recipes = await readSampleRecipes();

  return (
    <div className="w-full bg-gradient-to-b from-primary-100/20 to-transparent py-12 dark:from-primary-900/10">
      <div className="wide-container flex w-full flex-col gap-6">
        <header className="flex flex-col gap-3 text-center md:text-left">
          <h1 className="text-3xl font-semibold md:text-4xl">
            MixMeasureBuddy Recipe Gallery
          </h1>
          <p className="text-base text-muted-foreground md:text-lg">
            Every recipe below ships with the firmware. Download, remix, or use
            them as inspiration for your own creations.
          </p>
          <div className="flex flex-wrap justify-center gap-2 md:justify-start">
            <Badge variant="outline" className="text-xs font-medium">
              {recipes.length} recipes available
            </Badge>
          </div>
        </header>

        {recipes.length === 0 ? (
          <div className="rounded-xl border border-dashed p-8 text-center text-muted-foreground">
            No recipes are available yet. Run the build again to regenerate the
            bundled library.
          </div>
        ) : (
          <RecipeGalleryGrid recipes={recipes} />
        )}
      </div>
    </div>
  );
}
