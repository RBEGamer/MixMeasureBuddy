import { siteConfig } from '@/data/config/site.settings';
import { headerNavLinks } from '@/data/config/headerNavLinks';
import Link from '@/components/shared/Link';
import MobileNav from '@/components/shared/MobileNav';
import ThemeSwitch from'@/components/shared/ThemeSwitch';
import SearchButton from '../search/SearchButton';
import ActiveLink from '@/components/shared/ActiveLink';
import Image from 'next/image';

const Header = () => {
  return (
    <header className="flex items-center justify-between py-10 flex-wrap w-full mb-20 lg:mb-32 pt-6 wide-container">
      <div>
        <Link href="/" aria-label={siteConfig.logoTitle}>
          <div className="flex items-center gap-3 justify-between">
            <Image
              src="/static/images/logo.svg"
              alt="MixMeasureBuddy logo"
              height={43}
              width={43}
              className="group-hover:animate-wiggle dark:hidden"
            />

            <Image
              src="/static/images/logo-dark.svg"
              alt="MixMeasureBuddy logo"
              height={43}
              width={43}
              className="group-hover:animate-wiggle hidden dark:inline-block"
            />

            <div className="hidden text-2xl font-semibold sm:flex h-full">
              MixMeasureBuddy
            </div>
          </div>
        </Link>
      </div>
      <div className="flex items-center leading-5 gap-4 sm:gap-6">
        {headerNavLinks.map((link) => (
          <ActiveLink
            key={link.title}
            href={link.href}
            className="nav-link hidden sm:block"
            activeClassName="nav-link-active"
          >
            <span>{link.title}</span>
          </ActiveLink>
        ))}

        <ThemeSwitch />
        <MobileNav />
      </div>
    </header>
  );
};

export default Header;
