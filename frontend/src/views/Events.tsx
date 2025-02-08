import { useEffect, useMemo, useState } from 'react';
import {
  ColumnDef,
  PaginationState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';
import toast from 'react-hot-toast';
import { MdError } from 'react-icons/md';
import { IoChevronDown, IoChevronUp } from 'react-icons/io5';
import { HiChevronLeft, HiChevronRight, HiChevronDoubleLeft, HiChevronDoubleRight } from "react-icons/hi2";
import { IEvent, EventType } from '@/types';
import { RESTManagerInstance } from '@/utils/rest';
import { sleep } from '@/utils/helpers';
import { Loading } from '@/components';

const EVENT_TYPE_CLASSNAMES = "rounded-md text-white p-[4px]"

const EVENT_TYPE_MAPPINGS: {[key in EventType]: JSX.Element} = {
  [EventType.DEVICE_ADDED]: <span className={`${EVENT_TYPE_CLASSNAMES} bg-teal-500`}>DEVICE ADDED</span>,
  [EventType.DEVICE_REMOVED]: <span className={`${EVENT_TYPE_CLASSNAMES} bg-rose-500`}>DEVICE REMOVED</span>,
  [EventType.WAKE]: <span className={`${EVENT_TYPE_CLASSNAMES} bg-indigo-500`}>WAKE REQUEST</span>
}

const EventsTable = ({ data, columns }: { data: IEvent[]; columns: ColumnDef<IEvent>[] }) => {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });

  const table = useReactTable({
    columns,
    data,
    debugTable: true,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onPaginationChange: setPagination,
    //no need to pass pageCount or rowCount with client-side pagination as it is calculated automatically
    state: {
      pagination,
    },
    // autoResetPageIndex: false, // turn off page index reset when sorting or filtering
  });

  return (
    <div className='w-full'>
      <table className='w-full rounded-t-md overflow-hidden border-collapse'>
        <thead className='bg-gray-800 text-white h-10'>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header, index) => {
                const isLast = index === headerGroup.headers.length - 1;
                return (
                  <th
                    key={header.id}
                    colSpan={header.colSpan}
                    className={isLast ? '' : 'box-border border-r border-gray-400'}
                  >
                    <div
                      {...{
                        className: header.column.getCanSort()
                          ? 'flex justify-center items-center gap-2 cursor-pointer select-none'
                          : '',
                        onClick: header.column.getToggleSortingHandler(),
                      }}
                    >
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {{
                        asc: <IoChevronUp className='inline' />,
                        desc: <IoChevronDown className='inline' />,
                      }[header.column.getIsSorted() as string] ?? null}
                    </div>
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row, index) => {
            const rowBg = index % 2 === 0 ? 'bg-white' : 'bg-gray-100';

            return (
              <tr key={row.id} className={rowBg}>
                {row.getVisibleCells().map((cell) => {
                  return (
                    <td
                      key={cell.id}
                      className='text-center py-2 box-border border border-gray-400'
                    >
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
      {/* Pagination */}
      {table.getPageCount() > 1 && (
        <div className='flex items-center mt-4 border-collapse text-slate-700'>
          <button
            className='border border-box border-gray-400 rounded-l p-1 h-8 bg-white disabled:bg-gray-100'
            onClick={() => table.firstPage()}
            disabled={!table.getCanPreviousPage()}
          >
            <HiChevronDoubleLeft />
          </button>
          <button
            className='border border-box border-gray-400 p-1 h-8 bg-white disabled:bg-gray-100'
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            <HiChevronLeft />
          </button>
          <button
            className='border border-box border-gray-400 p-1 h-8 bg-white disabled:bg-gray-100'
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            <HiChevronRight />
          </button>
          <button
            className='border border-box border-gray-400 p-1 h-8 bg-white disabled:bg-gray-100'
            onClick={() => table.lastPage()}
            disabled={!table.getCanNextPage()}
          >
            <HiChevronDoubleRight />
          </button>
          <span className='flex items-center gap-1 border border-box border-gray-400 rounded-r p-1 h-8 bg-white'>
            <div>Page</div>
            <strong>
              {table.getState().pagination.pageIndex + 1} of {table.getPageCount().toLocaleString()}
            </strong>
          </span>
        </div>
      )}
    </div>
  );
};
export const Events = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [events, setEvents] = useState<IEvent[]>([]);

  const columns = useMemo<ColumnDef<IEvent>[]>(
    () => [
      {
        accessorFn: (row) => row.timestamp.slice(0, -7),
        id: 'timestamp',
        cell: (e) => e.getValue(),
        header: () => <span>Timestamp</span>,
        footer: (props) => props.column.id,
      },
      {
        accessorFn: (row) => EVENT_TYPE_MAPPINGS[row.eventType],
        id: 'eventType',
        cell: (e) => e.getValue(),
        header: () => <span>Type</span>,
        footer: (props) => props.column.id,
      },
      {
        accessorKey: 'eventData',
        header: () => 'Info',
        footer: (props) => props.column.id,
      },
    ],
    [],
  );

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
            <MdError size={100} className='dark:text-white' />
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
        <EventsTable columns={columns} data={events} />
      </div>
    </>
  );
};
