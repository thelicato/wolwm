import { Link } from 'react-router-dom';
import Logo from '@/assets/logo.png';

export const Header = () => {
  return (
    <>
      <header className='h-16'>
        <div
          className={
            'w-full h-16 fixed mx-auto bg-gray-800 font-Jost flex flex-row justify-between items-center pr-4'
          }
        >
          <div className='w-14 md:w-60 flex justify-left pl-4 items-center gap-2'>
            <h1 className='text-2xl select-none'>
              <Link
                to='/'
                className='no-underline text-slate-300 hover:text-slate-100 flex items-center'
              >
                <img src={Logo} className='inline h-10' alt='wolwm' />
                <span className='font-semibold ml-2 hidden md:block'>wolwm</span>
              </Link>
            </h1>
          </div>
        </div>
      </header>
    </>
  );
};
