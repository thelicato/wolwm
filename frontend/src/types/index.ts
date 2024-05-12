export enum Theme {
  Dark = 'dark',
  Light = 'light',
}

export enum NavbarStatus {
  Open = 'OPEN',
  Closed = 'CLOSED',
  AutoCollapsed = 'AUTO_COLLAPSED',
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
