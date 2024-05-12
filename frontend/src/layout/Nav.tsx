import { Link, useLocation } from 'react-router-dom';
import Tippy from '@tippyjs/react';
import { MdOutlineDevices, MdDarkMode, MdLightMode } from 'react-icons/md';

// Local imports
import { useTheme } from '@/context';
import { INavLink, Theme } from '@/types';

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

export const Nav = () => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const widthClass = 'w-60';

  return (
    <nav className={`${widthClass} z-30`}>
      <div className={`${widthClass} fixed-nav flex flex-col text-slate-200`}>
        {/* Navbar Collapse Btn */}
        <div
          className={`grid grid-cols-1 bg-gray-900  border-slate-700 p-2 justify-center items-center md:grid-cols-2 border-b-[1px]`}
        >
          <div className='flex items-center justify-center p-1'>
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
          </div>
        </div>
        <div className='flex flex-col flex-1 justify-between bg-gray-900 p-2 pt-4'>
          {/* Nav Content */}
          <ul className='flex flex-col gap-4'>
            {navlinks.map((navlink: INavLink, key: number) => {
              const isActive = location.pathname === navlink.link ? true : false;
              return (
                <Tippy content={navlink.innerTxt} placement='right' className='block' key={key}>
                  <Link
                    to={navlink.link}
                    className={`rounded-md
                  ${isActive ? 'font-bold bg-gray-700' : 'font-normal hover:bg-gray-700'}
                  ${'px-2 py-4'}
                  `}
                  >
                    <li className={`flex items-center gap-2 ${'justify-start'}`}>
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
  );
};
