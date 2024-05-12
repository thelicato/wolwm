import { Link } from 'react-router-dom';
import ErrorImg from '@/assets/generic_error.png';

export const Error = () => {
  return (
    <div className='bg-gray-900 w-screen min-h-screen m-auto font-Jost py-4'>
      <div className='m-auto'>
        <div className='content'>
          <div className='inset-0 text-center flex flex-col justify-center p-8'>
            <div className='flex flex-col items-center gap-2'>
              <img src={ErrorImg} className='w-96 h-96 mb-4' />
              <Link to={'/'}>
                <button className='text-white rounded bg-cyan-600 p-3 mt-4 hover:bg-cyan-800'>
                  Go back Home
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
