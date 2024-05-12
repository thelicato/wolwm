import { useState } from 'react';
import { Nav, Header, Content } from '@/layout';
import { Devices, NoMatch, Error } from '@/views';
import { createBrowserRouter, Outlet } from 'react-router-dom';
import { INFO } from '@/config';

const NoMatchElement = () => {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);

  if (loggedIn) {
    return (
      <>
        <Header />
        <div className='flex'>
          <Nav />
          <Content>
            <NoMatch />
          </Content>
        </div>
      </>
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
    <>
      <Header />
      <div className='flex'>
        <Nav />
        <Content>
          <Outlet />
        </Content>
      </div>
    </>
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
