import { useEffect, RefObject, useRef, useCallback } from 'react';

export const useOnClickOutside = (
  ref: RefObject<HTMLElement>,
  handler: (event: MouseEvent) => void,
) => {
  useEffect(
    () => {
      const listener = (e: Event) => {
        // Do nothing if clicking ref's element or descendent elements
        if (!ref.current || (e.target !== null && ref.current.contains(e.target as Node))) {
          return;
        }
        handler(e as MouseEvent);
      };
      document.addEventListener('mousedown', listener);
      document.addEventListener('touchstart', listener);
      return () => {
        document.removeEventListener('mousedown', listener);
        document.removeEventListener('touchstart', listener);
      };
    },
    // Add ref and handler to effect dependencies
    // It's worth noting that because passed in handler is a new ...
    // ... function on every render that will cause this effect ...
    // ... callback/cleanup to run every render. It's not a big deal ...
    // ... but to optimize you can wrap handler in useCallback before ...
    // ... passing it into this hook.
    [ref, handler],
  );
};

type AnyFunction = (...args: any[]) => any;

export const useDebouncedFunction = <F extends (...args: any[]) => Promise<any>>(
  func: F,
  delay: number,
): F => {
  // Define the generic type for the function that returns a promise
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const functionCalled = useRef(false);

  // The debounced function maintains the signature and return type of the original function
  const debouncedFunction = useCallback(
    (...args: any[]) => {
      if (!functionCalled.current) {
        // Immediately invoke the function and ignore subsequent calls until the delay has passed
        const result = func(...args);
        functionCalled.current = true;

        // Reset the debounce mechanism after a delay
        timeoutRef.current = setTimeout(() => {
          functionCalled.current = false;
        }, delay);
        return result; // Return the result of the function call
      }
      // If the function has already been called, return a rejected promise
      return Promise.resolve();
    },
    [func, delay],
  ) as F;

  // Clear the timeout when the component unmounts or the delay changes
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [delay]);

  return debouncedFunction;
};
