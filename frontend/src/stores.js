import axios from "axios";
import { createStore, createEffect } from "effector";
import { baseUrl } from "./config";

export const getAddressesFx = createEffect(async () => {
  const response = await axios.get(`${baseUrl}/api/address/`);
  return response.data;
});

const $addresses = createStore([]).on(
  getAddressesFx.doneData,
  (_, addresses) => addresses
);

export const $cities = createStore([]).on($addresses, (_, addresses) =>
  addresses.map((address) => address.city)
);
