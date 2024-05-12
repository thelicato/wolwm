import { Dispatch, createContext, useContext, useEffect, useState } from 'react';
import { useWindowSize } from '@uidotdev/usehooks';
import { NavbarStatus, Theme } from '@/types';

// Constants
const colorThemeLocalStorageKey = 'wolwm-color-theme';
const navbarStatusLocalStorageKey = 'wolwm-navbar-status';
const breakpoint = 960;

const getInitialTheme = (): Theme => {
  if (typeof window !== 'undefined' && window.localStorage) {
    const storedPrefs = window.localStorage.getItem(colorThemeLocalStorageKey);

    if (typeof storedPrefs === 'string') {
      return storedPrefs as Theme;
    }

    const userMedia = window.matchMedia('(prefers-color-scheme: dark)');
    if (userMedia.matches) {
      return Theme.Dark;
    }
  }

  return Theme.Light; // light theme as the default;
};

const getInitialNavbarStatus = (): NavbarStatus => {
  if (typeof window !== 'undefined' && window.localStorage) {
    const storedPrefs = window.localStorage.getItem(navbarStatusLocalStorageKey);

    if (typeof storedPrefs === 'string') {
      return storedPrefs as NavbarStatus;
    }
  }

  return NavbarStatus.Open; // open navbar as the default;
};

interface ProviderInterface {
  navbarStatus: NavbarStatus;
  setNavbarStatus: (navbarStatus: NavbarStatus) => void;
  theme: Theme;
  toggleTheme: () => void;
  isModalOpen: boolean;
  setIsModalOpen: Dispatch<boolean>;
}

export const ThemeContext = createContext<ProviderInterface | null>(null);

const ThemeProvider = ({ children }: any): any => {
  const size = useWindowSize();
  const [theme, setTheme] = useState<Theme>(getInitialTheme);
  const [navbarStatus, setNavbarStatus] = useState<NavbarStatus>(getInitialNavbarStatus);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  useEffect(() => {
    if (!size.width) {
      return;
    }
    if (navbarStatus !== NavbarStatus.AutoCollapsed && size.width < breakpoint) {
      setNavbarStatus(NavbarStatus.AutoCollapsed);
    } else if (navbarStatus === NavbarStatus.AutoCollapsed && size.width >= breakpoint) {
      setNavbarStatus(NavbarStatus.Open);
    }
  }, [size]);

  const rawSetTheme = (rawTheme: Theme) => {
    const root = window.document.documentElement;
    const isDark = rawTheme === Theme.Dark;

    root.classList.remove(isDark ? 'light' : 'dark');
    root.classList.add(rawTheme);

    localStorage.setItem(colorThemeLocalStorageKey, rawTheme);
  };

  const changeNavbarStatus = (navbarStatus: NavbarStatus) => {
    setNavbarStatus(navbarStatus);
    localStorage.setItem(navbarStatusLocalStorageKey, navbarStatus);
  };

  const toggleTheme = () => {
    const _theme: Theme = theme === Theme.Dark ? Theme.Light : Theme.Dark;
    setTheme(_theme);
  };

  useEffect(() => {
    rawSetTheme(theme);
  }, [theme]);

  return (
    <ThemeContext.Provider
      value={{
        navbarStatus,
        setNavbarStatus: changeNavbarStatus,
        theme,
        toggleTheme,
        isModalOpen,
        setIsModalOpen,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

export { ThemeProvider, useTheme };
