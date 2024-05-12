import { ReactNode, createRef, useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Tippy from '@tippyjs/react';
import { useWindowSize } from '@uidotdev/usehooks';
import { MdOutlineDevices, MdDarkMode, MdLightMode } from 'react-icons/md';
import { PiListBold } from 'react-icons/pi';

// Local imports
import { useTheme } from '@/context';
import { INavLink, Theme } from '@/types';
import Logo from '@/assets/logo.png';
import { useOnClickOutside } from './utils/hooks';

const navbarIconSize = 28;
const navlinks: INavLink[] = [
  {
    link: '/',
    innerTxt: 'Devices',
    icon: <MdOutlineDevices size={navbarIconSize} />,
  },
];

const navbarActionBtnClass =
  'bg-gray-900 hover:bg-gray-700 text-slate-100 transition-all duration-200 rounded-md cursor-pointer p-1';
const breakpoint = 768;

interface IContentProps {
  children: ReactNode;
}

export const Layout = ({ children }: IContentProps) => {
  const size = useWindowSize();
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const [isMobileNavbarOpen, setIsMobileNavbarOpen] = useState<boolean>(false);
  const navbarRef = createRef<HTMLInputElement>();

  const navbarClass = useMemo(() => {
    if (!size.width || size.width > breakpoint) {
      return 'w-60';
    } else if (isMobileNavbarOpen) {
      return 'w-screen h-screen py-4 flex justify-start fixed bottom-0 left-0 backdrop-blur-sm blur-bg';
    } else {
      return 'hidden';
    }
  }, [size, isMobileNavbarOpen]);

  const restoreStyle = () => {
    document.body.style.overflowY = 'scroll';
    setIsMobileNavbarOpen(false);
  };

  //const navbarClass = size.width && size.width > breakpoint ? 'w-60' : 'hidden';
  const openNavbar = () => {
    window.scrollTo(0, 0);
    document.body.style.overflowY = 'hidden';
    setIsMobileNavbarOpen(true);
  };

  const closeNavbar = () => {
    restoreStyle();
  };

  useOnClickOutside(navbarRef, closeNavbar);

  return (
    <>
      {/* Header */}
      <header className='h-16'>
        <div
          className={
            'w-full h-16 fixed mx-auto bg-gray-800 font-Jost flex flex-row justify-between items-center pr-4'
          }
        >
          <div className='w-full flex justify-between pl-4 items-center gap-2'>
            <h1 className='text-2xl select-none'>
              <Link
                to='/'
                className='no-underline text-slate-300 hover:text-slate-100 flex items-center'
              >
                <img src={Logo} className='inline h-10' alt='wolwm' />
                <span className='font-semibold ml-2 block'>wolwm</span>
              </Link>
            </h1>
            <div className='flex gap-4'>
              {theme === Theme.Dark ? (
                <MdLightMode
                  size={navbarIconSize}
                  className={navbarActionBtnClass}
                  onClick={toggleTheme}
                />
              ) : (
                <MdDarkMode
                  size={navbarIconSize}
                  className={navbarActionBtnClass}
                  onClick={toggleTheme}
                />
              )}
              <PiListBold
                size={navbarIconSize}
                className={`${navbarActionBtnClass} block md:hidden`}
                onClick={openNavbar}
              />
            </div>
          </div>
        </div>
      </header>
      {/* Main Container */}
      <div className='flex'>
        {/* Sidebar */}
        <nav className={`${navbarClass} z-[9999]`}>
          <div ref={navbarRef} className='w-60 custom-nav flex flex-col text-slate-200'>
            <div className='flex flex-col flex-1 justify-between bg-gray-900 p-2 pt-4'>
              {/* Nav Content */}
              <ul className='flex flex-col gap-4'>
                {navlinks.map((navlink: INavLink, key: number) => {
                  const isActive = location.pathname === navlink.link ? true : false;
                  return (
                    <Tippy content={navlink.innerTxt} placement='right' className='block' key={key}>
                      <Link
                        to={navlink.link}
                        className={`rounded-md px-2 py-4 ${isActive ? 'font-bold bg-gray-700' : 'font-normal hover:bg-gray-700'}`}
                      >
                        <li className='flex items-center gap-2 justify-start'>
                          {navlink.icon}
                          <span className={'block'}>{navlink.innerTxt}</span>
                        </li>
                      </Link>
                    </Tippy>
                  );
                })}
              </ul>
            </div>
          </div>
        </nav>
        {/* Content */}
        <main className='main-content h-full grid bg-gray-100 dark:bg-gray-700 grow font-Jost z-[999]'>
          <div className='w-full mx-auto h-full'>{children}</div>
        </main>
      </div>
    </>
  );
};
