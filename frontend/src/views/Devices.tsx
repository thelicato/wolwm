export const Devices = () => {
  return (
    <div className='p-4'>
      <h1 className='font-bold text-4xl mb-4'>Devices</h1>
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
        <div className='card p-4'>
          <h2 className='text-2xl font-bold mb-2'>Device Name</h2>
          <p>
            <b>MAC Address:</b> FF:FF:FF:FF:FF:FF
          </p>
        </div>
      </div>
    </div>
  );
};
