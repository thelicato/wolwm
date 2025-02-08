import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { IBaseDevice, IDevice } from '@/types';
import { RESTManagerInstance } from '@/utils/rest';
import { sleep } from '@/utils/helpers';
import { ConfirmModalContent, Loading, Modal } from '@/components';
import { IoIosWarning } from 'react-icons/io';
import { useForm } from 'react-hook-form';

export const Devices = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [devices, setDevices] = useState<IDevice[]>([]);

  // Add device
  const { register, handleSubmit, formState, setValue } = useForm<IBaseDevice>();
  const [addDeviceModalOpen, setAddDeviceModalOpen] = useState<boolean>(false);

  // Delete device
  const [deleteDeviceModalOpen, setDeleteDeviceModalOpen] = useState<boolean>(false);
  const [deviceIdToDelete, setDeviceIdToDelete] = useState<string>('');

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

  const openDeleteDeviceModal = (deviceId: string) => {
    setDeviceIdToDelete(deviceId);
    setDeleteDeviceModalOpen(true);
  };

  const closeDeleteDeviceModal = () => {
    setDeviceIdToDelete('');
    setDeleteDeviceModalOpen(false);
  };

  const closeAddDeviceModal = () => {
    setAddDeviceModalOpen(false);
    setValue('name', '');
    setValue('mac', '');
  };

  const addDevice = async (data: IBaseDevice) => {
    setIsLoading(true);
    try {
      await RESTManagerInstance.addDevice(data);
      const res = await RESTManagerInstance.getDevices();
      setDevices(res.data.devices);
      closeAddDeviceModal();
      await sleep(500);
      toast.success('Device added');
    } catch (err) {
      toast.error('Unable to add device');
    }
    setIsLoading(false);
  };

  const removeDevice = async () => {
    setIsLoading(true);
    try {
      await RESTManagerInstance.deleteDevice(deviceIdToDelete);
      const res = await RESTManagerInstance.getDevices();
      setDevices(res.data.devices);
      closeDeleteDeviceModal();
      await sleep(500);
      toast.success('Device removed');
    } catch (err) {
      toast.error('Unable to remove device');
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
    <>
      {/* Delete Device Modal */}
      {deleteDeviceModalOpen && (
        <Modal title='Delete Device' size='normal' onClose={closeDeleteDeviceModal}>
          <ConfirmModalContent onConfirm={removeDevice} onCancel={closeDeleteDeviceModal} />
        </Modal>
      )}

      {/* Add Device Modal */}
      {addDeviceModalOpen && (
        <Modal title='Add Device' size='big' onClose={closeAddDeviceModal}>
          <form className='flex flex-col gap-2' onSubmit={handleSubmit(addDevice)}>
            <div className='flex flex-col md:flex-row gap-2 bg-amber-100 p-2 rounded-lg mb-4 shadow-sm items-center'>
              <IoIosWarning size={24} className='text-amber-500' />
              <p className='dark:text-slate-800 text-center'>
                The only format allowed for the MAC address is
              </p>
              <pre className=' text-slate-500 pt-[1px]'>FF:FF:FF:FF:FF:FF</pre>
            </div>
            <label>Name</label>
            <input
              className='bg-slate-50 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline dark:bg-gray-800 dark:border-gray-700 dark:text-white'
              type='text'
              placeholder='Device Name'
              {...register('name', { required: 'true', minLength: 1 })}
            />
            <label className='mt-2'>MAC Address</label>
            <input
              className='bg-slate-50 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline dark:bg-gray-800 dark:border-gray-700 dark:text-white'
              type='text'
              placeholder='MAC Address'
              {...register('mac', {
                required: 'true',
                minLength: 1,
                pattern: /^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$/,
              })}
            />
            <button
              type='submit'
              disabled={!formState.isValid}
              className='my-4 py-2 w-full bg-cyan-700 hover:bg-cyan-900 text-white font-bold rounded-sm cursor-pointer disabled:cursor-default disabled:bg-gray-400'
            >
              Add Device
            </button>
          </form>
        </Modal>
      )}

      <div className='p-4'>
        <h1 className='font-bold text-4xl mb-4'>Devices</h1>
        <div className='flex gap-2 bg-amber-100 p-2 rounded-lg mb-4 shadow-sm'>
          <IoIosWarning size={24} className='text-amber-500' />
          <p className='dark:text-slate-800'>
            You cannot send multiple wake commands to the same device in a{' '}
            <b>short amount of time</b> as it will result in an <b>error</b>.
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
                  <button
                    className='my-4 py-2 w-full bg-rose-700 hover:bg-rose-900 text-white font-bold rounded-sm'
                    onClick={() => openDeleteDeviceModal(device.id)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            );
          })}
          <div
            className='card bg-cyan-700 hover:bg-cyan-900 cursor-pointer transition-all duration-200 flex flex-col items-center justify-center'
            onClick={() => setAddDeviceModalOpen(true)}
          >
            <h2 className='text-slate-100 text-5xl'>+</h2>
            <h3 className='text-slate-100 text-md font-semibold'>Add Device</h3>
          </div>
        </div>
      </div>
    </>
  );
};
