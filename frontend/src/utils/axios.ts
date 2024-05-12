import axios, { AxiosInstance, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';
import { BACKEND } from '@/config';

interface ILoggedInstanceOptions {
  headers?: RawAxiosRequestHeaders;
  withRefreshToken?: boolean;
  blob?: boolean;
}

const baseURL =
  process.env.NODE_ENV === 'development'
    ? `${BACKEND.DEV_BACKEND}${BACKEND.BASE_URL}`
    : BACKEND.BASE_URL;

const instance = (options: ILoggedInstanceOptions): AxiosInstance => {
  const instanceHeaders: any = {
    ...options?.headers,
  };

  const axiosConfig: AxiosRequestConfig = {
    baseURL: baseURL,
    headers: instanceHeaders,
  };
  if (options && options.blob) {
    axiosConfig.responseType = 'blob';
  }

  const instance = axios.create(axiosConfig);

  return instance;
};

export const http = instance;
