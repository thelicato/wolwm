import AppRouter from '@/AppRouter';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from '@/context';
import 'tippy.js/dist/tippy.css';

export const App = () => {
  return (
    <ThemeProvider>
      <RouterProvider router={AppRouter} />
      <Toaster position='bottom-left' />
    </ThemeProvider>
  );
};
