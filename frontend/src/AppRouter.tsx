import { useState } from 'react';
import { Layout } from '@/Layout';
import { Devices, NoMatch, Error } from '@/views';
import { createBrowserRouter, Outlet } from 'react-router-dom';
import { INFO } from '@/config';

const NoMatchElement = () => {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);

  if (loggedIn) {
    return (
      <Layout>
        <NoMatch />
      </Layout>
    );
  } else {
    return (
      <div className='m-auto'>
        <NoMatch />
      </div>
    );
  }
};

const CommonRoute = () => {
  return (
    <Layout>
      <Outlet />
    </Layout>
  );
};

const AppRouter = createBrowserRouter(
  [
    {
      path: '/',
      errorElement: <Error />,
      children: [
        {
          element: <CommonRoute />,
          children: [
            {
              path: '',
              element: <Devices />,
            },
          ],
        },
        { path: '*', element: <NoMatchElement /> },
      ],
    },
  ],
  {
    basename: import.meta.env.MODE === 'development' ? '/' : INFO.BASENAME,
  },
);

export default AppRouter;
