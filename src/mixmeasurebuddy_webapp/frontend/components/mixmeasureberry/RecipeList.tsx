import {FeatureListItem} from "@/components/landing/LandingFeatureList";
import {
    GlassWater} from 'lucide-react';


import { LandingFeature } from '@/components/landing/feature/LandingFeature';
import { cn } from '@/lib/utils';



import clsx from 'clsx';
import {alignments} from "@floating-ui/utils";

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
            description={description}
            featureItems={items}
        />
    );
};

