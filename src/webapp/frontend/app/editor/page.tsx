import { Metadata } from 'next';
import { RecipeEditor } from '@/components/recipes/RecipeEditor';
import { Toaster } from '@/components/shared/ui/sonner';

export const metadata: Metadata = {
  title: 'Recipe Editor · MixMeasureBuddy',
  description:
    'Create, edit, and manage MixMeasureBuddy .recipe files directly from your GitHub repository.',
};

export default function RecipeEditorPage() {
  return (
    <div className="w-full bg-gradient-to-b from-primary-100/30 to-transparent py-10 dark:from-primary-900/20">
      <div className="wide-container flex w-full flex-col gap-10">
        <section className="rounded-3xl bg-background/80 p-8 shadow-lg ring-1 ring-black/5 dark:bg-background/60">
          <h1 className="text-3xl font-semibold md:text-4xl">
            Manage your MixMeasureBuddy recipes
          </h1>
          <p className="mt-3 max-w-3xl text-base text-muted-foreground md:text-lg">
            Upload your local <code>.recipe</code> files, tweak steps directly in
            the browser, and download updated copies ready for your MixMeasureBuddy.
          </p>
        </section>

        <RecipeEditor />
      </div>
      <Toaster position="top-right" richColors />
    </div>
  );
}
