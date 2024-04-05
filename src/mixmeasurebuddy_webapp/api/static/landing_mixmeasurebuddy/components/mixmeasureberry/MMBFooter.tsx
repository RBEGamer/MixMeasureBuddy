import Image from 'next/image';
import Link from '../shared/Link';
import { siteConfig } from '@/data/config/site.settings';
import {
  MailIcon,
  GithubIcon,
  FacebookIcon,
  YoutubeIcon,
  LinkedinIcon,
  InstagramIcon,
  BoxesIcon,
} from 'lucide-react';
import { TwitterXIcon } from '@/components/icons/XIcon';

import ActiveLink from '@/components/shared/ActiveLink';
import { FooterSupportButton } from '@/components/shared/FooterSupportButton';
import { Button } from '@/components/shared/ui/button';
import { footerLinks } from '@/data/config/footerLinks';
import { cn } from '@/lib/utils';
import { TiktokIcon } from '@/components/icons/TiktokIcon';
import { ThreadsIcon } from '@/components/icons/ThreadsIcon';

export default function MMBFooter({ className }: { className?: string }) {
  const columnNumber = footerLinks.filter(({ links }) => links.length).length;

  return (
    <footer
      className={cn(
        'mt-auto w-full bg-gradient-to-r from-white/5 via-white/60 to-white/5 backdrop-blur-sm dark:from-slate-700/5 dark:via-slate-700/60 dark:to-slate-700/5',
        className,
      )}
    >


      <div>


        <div className="py-8 flex flex-col items-center">
          <div className="mb-3 flex flex-wrap justify-center gap-4">
            {siteConfig.email && (
              <a href={`mailto:${siteConfig.email}`}>
                <Button variant="ghost" size="icon" aria-label="Email">
                  <MailIcon className="w-6 h-6" />
                </Button>
              </a>
            )}

            {siteConfig.github && (
              <a href={siteConfig.github}>
                <Button variant="ghost" size="icon" aria-label="GitHub">
                  <GithubIcon className="w-6 h-6" />
                </Button>
              </a>
            )}


          </div>
          <div className="w-full text-center lg:flex lg:justify-center p-4 mb-2 space-x-2 text-sm text-gray-500 dark:text-gray-400">
            <span>MixMeasureBuddy is an 100% OpenSource project</span>
            <span>{` • `}</span>
            <span>{`last update  ${new Date().getFullYear()}`}</span>
            <span>{` • `}</span>
            <Link href="http://marcelochsendorf.com/impressum">{`Imprint`}</Link>
            
          </div>
        </div>
      </div>
    </footer>
  );
}
