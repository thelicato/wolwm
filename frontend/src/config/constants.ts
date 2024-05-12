import { RawAxiosRequestHeaders } from 'axios';

export const DEFAULT_HEADERS: RawAxiosRequestHeaders = {
  'Content-Type': 'application/json',
  'Cache-Control': 'no-cache',
  Pragma: 'no-cache',
  Expires: '0',
};

export const UPLOAD_HEADERS: RawAxiosRequestHeaders = {
  'Content-Type': 'multipart/form-data',
};
