import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { MdError } from 'react-icons/md';
import { IEvent } from '@/types';
import { RESTManagerInstance } from '@/utils/rest';
import { sleep } from '@/utils/helpers';
import { Loading } from '@/components';

export const Events = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [events, setEvents] = useState<IEvent[]>([]);

  const loadEvents = async () => {
    try {
      const res = await RESTManagerInstance.getEvents();
      setEvents(res.data.events);
      await sleep(500);
      setIsLoading(false);
      toast.success('Events loaded');
    } catch (err) {
      toast.error('Unable to load events');
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  if (isLoading) {
    return <Loading blur />;
  }

  if (events.length === 0) {
    return (
      <>
        <div className='p-4'>
          <h1 className='font-bold text-4xl mb-4'>Events</h1>
          <div className='w-full flex flex-col justify-center items-center'>
            <MdError size={100} className='dark:text-white'/>
            <h2 className='text-2xl font-semibold'>No Events</h2>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <div className='p-4'>
        <h1 className='font-bold text-4xl mb-4'>Events</h1>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
          {events.map((event: IEvent, key: number) => {
            return (
              <div className='card p-4' key={key}>
                <h2 className='text-2xl font-bold mb-2'>{event.eventType}</h2>
                <p>
                  <b></b> {event.eventData}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};
