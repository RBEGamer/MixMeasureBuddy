import { ComponentDemo } from 'demo/demo';
import { LandingBandSection } from '@/components/landing/LandingBand';
import { LandingFaqSection } from '@/components/landing/LandingFaq';
import { LandingFeatureList } from '@/components/landing/LandingFeatureList';
import { LandingProductFeature } from '@/components/landing/LandingProductFeature';
import { LandingSaleCtaSection } from '@/components/landing/LandingSaleCta';
import { LandingTestimonialListSection } from '@/components/landing/LandingTestimonialList';

import {
  ChromeIcon,
  FigmaIcon,
  FramerIcon,
  GithubIcon,
  LayersIcon,
  LightbulbIcon,
  LineChartIcon,
  SparklesIcon,
  ThumbsUpIcon,
  ZapIcon,
} from 'lucide-react';
import { MMBRecipeList } from '@/components/mixmeasureberry/RecipeList';
import {cn} from "@/lib/utils";
import Image from "next/image";
import { withBasePath } from '@/lib/base-path';

export default function Home() {
  // @ts-ignore
    return (
    <div className="flex flex-col w-full items-center fancy-overlay">
        <LandingProductFeature
            imagePosition="right"
            imageSrc={withBasePath('/static/images/A003_11281139_S044_.png')}
            imageAlt="Product image"
            title="Intelligent Mixing Made Simple"
            zoomOnHover={true}
            imagePerspective="none"
            description="MixMeasureBuddy's smart cocktail scale revolutionizes home bartending by offering accurate ingredient measurements and a vast library of cocktail recipes personalized to your liquor collection. Enjoy the art of mixology with ease and precision."
            withBackground
        />


        <MMBRecipeList
            className = ""
            title="Rising recipe satabase ready to use!"
            description="Discover a treasure trove of culinary creations! Here you will not only find a selection of traditional recipes, but also a wealth of user-created delicacies. Dive in and be inspired by the variety! Join our growing community and share your own recipes with the world!"
            max_items={9}
        />




        <LandingFeatureList
        title="Features - MixMeasureBuddy"
        description="Discover the advanced features that set MixMeasureBuddy apart from traditional kitchen scales."
        featureItems={[
          {
            title: 'Open-Source',
            description:
              'MixMeasureBuddy is 100% open-source and can be build using a few simple and cheap parts.',
            icon: <LayersIcon />,
          },
          {
            title: 'Connectivity Features',
            description:
              'Enjoy seamless integration with a companion webapp for sharing personalized cocktail recipes with other MixMeasureBuddy owners.',
            icon: <LineChartIcon />,
          },
          {
            title: 'Offline Usage',
            description:
              "Recipes are stored offline and locally on the MixMeasureBerry and can be edited using a text editor",
            icon: <SparklesIcon />,
          },
          {
            title: 'User-Friendly Interface',
            description:
              "Easily navigate the scale's intuitive interface for effortless cocktail making.",
            icon: <LightbulbIcon />,
          },
          {
            title: 'Customizable Recipes',
            description:
              'Access a plethora of cocktail recipes tailored to your liquor cabinet for endless mixing possibilities.',
            icon: <ZapIcon />,
          },
          {
            title: 'Precision Measurements',
            description:
              'Eliminate the guesswork and achieve consistent results with exact ingredient measurements every time.',
            icon: <ThumbsUpIcon />,
          },
        ]}
      />

      <LandingFaqSection
        title="Frequently Asked Questions"
        description="Get answers to common queries about MixMeasureBuddy."
        faqItems={[
          {
            question: 'Is MixMeasureBuddy easy to use?',
            answer:
              "Yes, MixMeasureBuddy's user-friendly design makes cocktail making simple and enjoyable for everyone.",
          },
          {
            question: 'Can I use MixMeasureBuddy for non-alcoholic drinks?',
            answer:
              'Absolutely, MixMeasureBuddy is versatile and can be used for a wide range of beverages beyond cocktails.',
          },
        ]}
        withBackground
      />



      <LandingSaleCtaSection
        title="Get your own MixMeasureBuddy"
        description="Just build your own MixMeasureBuddy with a few parts using a detailed sourcing and assembly instructions."
        ctaHref={'https://github.com/RBEGamer/MixMeasureBuddy'}
        ctaLabel={'Build your own - NOW'}
        withBackground
      />


    </div>
  );
}
