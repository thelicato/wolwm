import { ReactNode } from 'react';

interface IContentProps {
  children: ReactNode;
}

export const Content = ({ children }: IContentProps) => {
  return (
    <main className='main-content h-full grid bg-gray-100 dark:bg-gray-700 grow font-Jost z-[999]'>
      <div className='w-full mx-auto h-full'>{children}</div>
    </main>
  );
};
