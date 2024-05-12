import { useEffect, useState, ReactNode, createRef } from 'react';
import { useHotkeys } from 'react-hotkeys-hook';
import { AiFillCloseCircle } from 'react-icons/ai';
import { useOnClickOutside } from '@/utils/hooks';
import { useTheme } from '@/context';

interface IModalProps {
  title: string;
  children: ReactNode;
  size?: 'big' | 'normal' | 'small';
  overflow?: 'auto' | 'hidden';
  noBlur?: boolean;
  fixed?: boolean;
  keepLayout?: boolean;
  onClose: () => void;
}

const modalClassesMapping: { [properties: string]: string } = {
  big: 'w-5/6 lg:w-3/6',
  normal: 'w-5/6 sm:w-4/6 lg:w-3/6 2xl:w-2/6',
  small: 'w-5/6 sm:w-4/6 lg:w-3/6 xl:w-1/6',
};

interface IConfirmModalContentProps {
  onConfirm: () => void;
  onCancel: () => void;
}

export const ConfirmModalContent = ({ onConfirm, onCancel }: IConfirmModalContentProps) => {
  return (
    <div>
      <h2 className='font-bold text-xl text-center mt-2 mb-4'>Are you sure?</h2>
      <div className='flex justify-center mt-6 gap-4'>
        <button className='button-green' onClick={onConfirm}>
          Confirm
        </button>
        <button className='button-red' onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export const Modal = (props: IModalProps) => {
  const { setIsModalOpen } = useTheme();
  const [currentScroll, setCurrentScroll] = useState<number>(0);
  const ref = createRef<HTMLInputElement>();

  const restoreStyle = () => {
    document.body.style.overflowY = 'scroll';
    setIsModalOpen(false);
  };

  useEffect(() => {
    setIsModalOpen(true);
    const _currentScroll = JSON.parse(JSON.stringify(window.scrollY));
    setCurrentScroll(_currentScroll);
    window.scrollTo(0, 0);
    document.body.style.overflowY = 'hidden';
    return restoreStyle;
  }, []);

  const closeModal = () => {
    window.scrollTo(0, currentScroll);
    props.onClose();
  };

  if (!props.fixed) {
    useOnClickOutside(ref, closeModal);
    useHotkeys('Escape', closeModal, { enableOnFormTags: true });
  }
  const modalClasses = props.size ? modalClassesMapping[props.size] : modalClassesMapping['normal'];
  const modalBlurClasses = props.noBlur ? '' : 'backdrop-blur-sm blur-bg';
  const overflowClass = props.overflow ? `overflow-y-${props.overflow}` : `overflow-y-auto`;

  return (
    <>
      <div
        className={`w-screen h-screen py-4 flex justify-start fixed bottom-0 left-0 ${modalBlurClasses} ${
          props.keepLayout ? 'z-10' : 'z-[999]'
        }`}
      >
        <div
          ref={ref}
          className={`${modalClasses} ${overflowClass} relative flex flex-col p-10 bg-white dark:bg-gray-800 m-auto rounded-md max-h-full`}
        >
          <div className='flex justify-between relative align-center'>
            <h3 className='flex-1 text-4xl font-bold py-2'>{props.title}</h3>
            {!props.fixed && (
              <>
                <span className='absolute right-10 top-2 border-2 border-gray-400 text-gray-500 rounded text-xs p-1 mr-1 dark:bg-white'>
                  ESC
                </span>
                <AiFillCloseCircle
                  className='absolute right-0 cursor-pointer transition-colors duration-300 text-red-500 hover:text-red-700'
                  size={38}
                  onClick={props.onClose}
                />
              </>
            )}
          </div>
          {props.children}
        </div>
      </div>
    </>
  );
};
