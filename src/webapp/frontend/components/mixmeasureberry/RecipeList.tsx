import { GlassWater } from 'lucide-react';
import clsx from 'clsx';
import { cn } from '@/lib/utils';
import path from 'path';
import { promises as fs } from 'fs';
import { recipeSchema, type Recipe } from '@/lib/recipes';

export interface MMBRecipeListItem {
    name: string;
    description: string;
    author: string;
}

/**
 * This component is meant to be used in the landing page, in the features list.
 *
 * Describes a single feature, with a title, description and icon.
 */
export const MMBLandingFeatureITEM = ({
                                   className,
                                   title,
                                   description,
                                   author,
                                   icon,
                               }: {
    className?: string;
    title: string;
    description: string;
    author: string;
    icon: React.ReactNode;
}) => {
    return (
        <div className={clsx('flex flex-col gap-4 py-4', className)}>

                <div className="flex w-100  align-middle rounded-md bg-primary-100/30 border border-primary-100/70 dark:bg-primary-900/70">
                    <div className={clsx('flex-col gap-6 py-6 left-0', className)}>{icon}</div>
                    <div className={clsx('flex-col gap-6 py-6 right-0', className)}><h3
                        className="font-semibold text-xl">{title}</h3></div>
                    </div>


                    <p className="text-sm text-gray-800 dark:text-gray-200">{description}</p>
            <h4 className="text-small font-semibold">by {author}</h4>
        </div>
    );
};


export const MMBRecipeListVisual = ({
                                        className,
                                        title,
                                        description,
                                        featureItems,
                                       withBackground = false,
                                   }: {
    className?: string;
    title: string | React.ReactNode;
    description: string | React.ReactNode;
    featureItems: MMBRecipeListItem[];
    withBackground?: boolean;
}) => {
    return (
        <section
            className={cn(
                'w-full flex justify-center items-center gap-8 pb-12 flex-col',
                withBackground ? 'bg-primary-100/20 dark:bg-primary-900/10' : '',
                className,
            )}
        >
            <section className={cn('wide-container mt-12 md:mt-16')}>
                <h2 className="text-4xl font-semibold leading-tight md:leading-tight max-w-xs sm:max-w-none md:text-5xl">
                    {title}
                </h2>
                <p className="mt-6 md:text-xl">{description}</p>

                <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-12">
                    {featureItems.map((featureItem, index) => (
                        <MMBLandingFeatureITEM
                            key={index}
                            title={featureItem.name}
                            author={featureItem.author}
                            description={featureItem.description}
                            icon=<GlassWater/>
                        />
                    ))}
                </div>
            </section>
        </section>
    );
};




const SAMPLE_DATA_PATH = path.join(
  process.cwd(),
  'public',
  'data',
  'sample-recipes.json',
);

const loadFallbackRecipes = async (limit: number): Promise<MMBRecipeListItem[]> => {
  try {
    const raw = await fs.readFile(SAMPLE_DATA_PATH, 'utf8');
    const json = JSON.parse(raw);
    const parsed = recipeSchema.array().safeParse(json);
    if (!parsed.success) {
      console.warn('[MMBRecipeList] Sample recipes failed validation');
      return [];
    }
    return parsed.data.slice(0, limit).map((recipe: Recipe) => ({
      name: recipe.name,
      description: recipe.description,
      author: 'Bundled Sample',
    }));
  } catch (error) {
    console.warn('[MMBRecipeList] Unable to read sample recipes:', error);
    return [];
  }
};

export const MMBRecipeList = async ({
  className,
  title,
  description,
  api_endpoint,
  max_items = 9,
}: {
  className?: string;
  title: string | React.ReactNode;
  description: string | React.ReactNode;
  api_endpoint?: string;
  max_items?: number;
}) => {
  const endpoint =
    api_endpoint ?? process.env.NEXT_PUBLIC_RECIPE_API_ENDPOINT ?? null;

  let items: MMBRecipeListItem[] = [];
  let resolvedDescription = description;

  if (endpoint) {
    try {
      const response = await fetch(
        `${endpoint}?max_items=${encodeURIComponent(String(max_items))}`,
        {
          next: { revalidate: 300 },
        },
      );

      if (response.ok) {
        items = await response.json();
      } else {
        console.warn(
          `[MMBRecipeList] Failed to load recipes: ${response.status} ${response.statusText}`,
        );
      }
    } catch (error) {
      console.warn('[MMBRecipeList] Recipe fetch failed:', error);
    }
  } else {
    const fallback = await loadFallbackRecipes(max_items);
    if (fallback.length) {
      items = fallback;
      resolvedDescription = description;
    } else {
      resolvedDescription =
        'Connect the API service to showcase the latest community cocktails.';
    }
  }

  return (
    <MMBRecipeListVisual
      className={className}
      title={title}
      description={
        items.length
          ? description
          : resolvedDescription
      }
      featureItems={items}
      withBackground={items.length === 0}
    />
  );
};
