import { http } from '@/utils/axios';
import { DEFAULT_HEADERS, DEVICES_ROUTE, WAKE_ROUTE, EVENTS_ROUTE } from '@/config';
import { AxiosResponse } from 'axios';
import { IBaseDevice, IDevice, IDeviceList, IEventList, IGenericDataRes, IWakeReq } from '@/types';

// This functions are just used to wrap specific REST API calls
// Not using try/catch statement here so every specific component
// can handle the error in his own way

class RESTManager {
  async getDevices(): Promise<AxiosResponse<IDeviceList>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).get<IDeviceList>(DEVICES_ROUTE.BASE);
    return res;
  }

  async addDevice(data: IBaseDevice): Promise<AxiosResponse<IGenericDataRes>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).post<IGenericDataRes>(DEVICES_ROUTE.BASE, data);
    return res;
  }

  async getDevice(deviceId: string): Promise<AxiosResponse<IDevice>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).get<IDevice>(`${DEVICES_ROUTE.BASE}/${deviceId}`);
    return res;
  }

  async deleteDevice(deviceId: string): Promise<AxiosResponse<IGenericDataRes>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).delete<IGenericDataRes>(`${DEVICES_ROUTE.BASE}/${deviceId}`);
    return res;
  }

  async wakeDevice(data: IWakeReq): Promise<AxiosResponse<IGenericDataRes>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).post<IGenericDataRes>(WAKE_ROUTE.BASE, data);
    return res;
  }

  async getEvents(): Promise<AxiosResponse<IEventList>> {
    const res = await http({
      headers: DEFAULT_HEADERS,
      blob: false,
    }).get<IEventList>(EVENTS_ROUTE.BASE);
    return res;
  }
}
export const RESTManagerInstance = new RESTManager();
