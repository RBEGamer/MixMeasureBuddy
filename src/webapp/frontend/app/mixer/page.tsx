import { Metadata } from 'next';
import { RecipeMixer } from '@/components/recipes/RecipeMixer';

export const metadata: Metadata = {
  title: 'Mix Lab · Ingredient Mixer',
  description:
    'Combine your on-hand ingredients with MixMeasureBuddy recipes to build a custom cocktail in seconds.',
};

export default function RecipeMixerPage() {
  return (
    <div className="w-full bg-gradient-to-b from-primary-100/30 to-transparent py-10 dark:from-primary-900/20">
      <div className="wide-container flex w-full flex-col gap-10">
        <section className="rounded-3xl bg-background/80 p-8 shadow-lg ring-1 ring-black/5 dark:bg-background/60">
          <h1 className="text-3xl font-semibold md:text-4xl">
            Mix Lab: build a drink with what you have
          </h1>
          <p className="mt-3 max-w-3xl text-base text-muted-foreground md:text-lg">
            Tell us which ingredients are in your cabinet and our recipe library
            will weave them into a new MixMeasureBuddy-ready cocktail file.
          </p>
        </section>

        <RecipeMixer />
      </div>
    </div>
  );
}
