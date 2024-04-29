import {FeatureListItem, LandingFeatureList} from "@/components/landing/LandingFeatureList";
import {
    GlassWater} from 'lucide-react';


import { LandingFeature } from '@/components/landing/feature/LandingFeature';
import { cn } from '@/lib/utils';



/**
 * A component meant to be used in the landing page.
 * It displays a grid list of features.
 *
 * Each feature has a title, description and icon.
 */
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
    featureItems: FeatureListItem[];
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
                        <LandingFeature
                            key={index}
                            title={featureItem.title}
                            description={featureItem.description}
                            icon=<GlassWater/>
                        />
                    ))}
                </div>
            </section>
        </section>
    );
};




export const MMBRecipeList = async ({
                                        className,
                                        title,
                                        description,
                                        max_items
                                    }: {
    className?: string;
    title: string | React.ReactNode;
    description: string | React.ReactNode;
    api_endpoint?: string;
    max_items?: number;


}) => {
    const item_response = await fetch(`http://127.0.0.1:5500/api/recipes?max_items=${max_items}`, {cache: 'force-cache'});
    let items = [];
    if(item_response.ok){
        items = await item_response.json();
    }

    return (
        <MMBRecipeListVisual
            title="Online Recipe Database"
            description="Discover a treasure trove of culinary creations! Here you will not only find a large selection of traditional recipes, but also a wealth of user-created delicacies. Dive in and be inspired by the variety! From hearty main courses to tempting desserts, our community has something for everyone. Don't miss the chance to expand your cooking skills and discover new flavors. Join our growing community and share your own recipes with the world!"
            featureItems={items}
        />
    );
};

