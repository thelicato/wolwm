export enum Theme {
  Dark = 'dark',
  Light = 'light',
}

export enum EventType {
  WAKE = 'wake',
  DEVICE_ADDED = 'device_added',
  DEVICE_REMOVED = 'device_removed',
}

export interface INavLink {
  link: string;
  innerTxt: string;
  icon: JSX.Element;
}

export interface IGenericDataRes {
  msg: string;
}

export interface IBaseDevice {
  name: string;
  mac: string;
}

export interface IDevice extends IBaseDevice {
  id: string;
}

export interface IDeviceList {
  devices: IDevice[];
}

export interface IWakeReq {
  deviceId: string;
}

export interface IEvent {
  id: string;
  eventType: EventType;
  eventData: string;
  timestamp: string;
}

export interface IEventList {
  events: IEvent[];
}
