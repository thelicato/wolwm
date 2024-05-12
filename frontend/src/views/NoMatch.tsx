import { Link } from 'react-router-dom';

export const NoMatch = () => {
  return (
    <>
      <div className='absolute custom-min-h-screen inset-0 text-center flex flex-col justify-center'>
        <div>
          <h5 className='text-sky-600 font-bold'>404 Error</h5>
          <h3 className='text-5xl font-bold py-4'>Page not found.</h3>
          <h4>Please check the URL in the address bar and try again.</h4>
          <Link to={'/'}>
            <button className='text-white rounded bg-cyan-600 p-3 mt-4 hover:bg-cyan-800'>
              Go back Home
            </button>
          </Link>
        </div>
      </div>
    </>
  );
};
