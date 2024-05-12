/*
Configuration file containing constants
Convention: constants are declared in UPPERCASE
Usage: import { CONSTANT_NAME } from '@/config'
*/

export const BACKEND: { [properties: string]: string } = {
  DEV_BACKEND: `http://${window.location.hostname}:5000`,
  WEBSOCKET: `http://${window.location.hostname}:5000`,
  BASE_URL: '/api/v1',
};

export const INFO: { [properties: string]: string } = {
  BASENAME: '/ui', // Used only in production
};

export const DEVICES_ROUTE: { [properties: string]: string } = {
  BASE: '/devices',
};

export const WAKE_ROUTE: { [properties: string]: string } = {
  BASE: '/wake',
};
