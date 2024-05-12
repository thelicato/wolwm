import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { IDevice } from '@/types';
import { RESTManagerInstance } from '@/utils/rest';
import { sleep } from '@/utils/helpers';
import { Loading } from '@/components';
import { IoIosWarning } from 'react-icons/io';

export const Devices = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [devices, setDevices] = useState<IDevice[]>([]);

  const loadDevices = async () => {
    try {
      const res = await RESTManagerInstance.getDevices();
      setDevices(res.data.devices);
      await sleep(500);
      setIsLoading(false);
      toast.success('Devices loaded');
    } catch (err) {
      toast.error('Unable to load devices');
    }
  };

  const wakeDevice = async (deviceId: string) => {
    setIsLoading(true);
    try {
      await RESTManagerInstance.wakeDevice({ deviceId: deviceId });
      await sleep(500);
      toast.success('Magic Packet correctly sent');
    } catch (err) {
      toast.error('Unable to wake device');
    }
    setIsLoading(false);
  };

  useEffect(() => {
    loadDevices();
  }, []);

  if (isLoading) {
    return <Loading blur />;
  }

  return (
    <div className='p-4'>
      <h1 className='font-bold text-4xl mb-4'>Devices</h1>
      <div className='flex gap-2 bg-amber-100 p-2 rounded-lg mb-4 shadow-sm'>
        <IoIosWarning size={24} className='text-amber-500' />
        <p className='dark:text-slate-800'>
          You cannot send multiple wake commands to the same device in a <b>short amount of time</b>{' '}
          as it will result in an <b>error</b>.
        </p>
      </div>
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
        {devices.map((device: IDevice, key: number) => {
          return (
            <div className='card p-4' key={key}>
              <h2 className='text-2xl font-bold mb-2'>{device.name}</h2>
              <p>
                <b>MAC Address:</b> {device.mac.toUpperCase()}
              </p>
              <div className='flex gap-2'>
                <button
                  className='my-4 py-2 w-full bg-cyan-700 hover:bg-cyan-900 text-white font-bold rounded-sm'
                  onClick={() => wakeDevice(device.id)}
                >
                  Wake
                </button>
                <button className='my-4 py-2 w-full bg-rose-700 hover:bg-rose-900 text-white font-bold rounded-sm'>
                  Remove
                </button>
              </div>
            </div>
          );
        })}
        <div className='card bg-cyan-700 hover:bg-cyan-900 cursor-pointer transition-all duration-200 flex flex-col items-center justify-center'>
          <h2 className='text-slate-100 text-5xl'>+</h2>
          <h3 className='text-slate-100 text-md font-semibold'>Add Device</h3>
        </div>
      </div>
    </div>
  );
};
