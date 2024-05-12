import { Dispatch, createContext, useContext, useEffect, useState } from 'react';
import { Theme } from '@/types';

// Constants
const colorThemeLocalStorageKey = 'wolwm-color-theme';

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

interface ProviderInterface {
  theme: Theme;
  toggleTheme: () => void;
  isModalOpen: boolean;
  setIsModalOpen: Dispatch<boolean>;
}

export const ThemeContext = createContext<ProviderInterface | null>(null);

const ThemeProvider = ({ children }: any): any => {
  const [theme, setTheme] = useState<Theme>(getInitialTheme);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  const rawSetTheme = (rawTheme: Theme) => {
    const root = window.document.documentElement;
    const isDark = rawTheme === Theme.Dark;

    root.classList.remove(isDark ? 'light' : 'dark');
    root.classList.add(rawTheme);

    localStorage.setItem(colorThemeLocalStorageKey, rawTheme);
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
