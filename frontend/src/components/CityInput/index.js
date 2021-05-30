import * as React from "react";
import { useStore } from "effector-react";
import { $cities } from "../../stores";
import { AutoComplete } from "antd";
import { useEffect, useState } from "react";

export function CityInput({ width = 200, placeholder = "", onSelect }) {
  const cities = useStore($cities);
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if (cities.length && !options.length)
      setOptions(() => cities.map((city) => ({ value: city })));
  }, [options, cities]);

  return (
    <AutoComplete
      style={{ width }}
      options={options}
      onSelect={onSelect}
      placeholder={placeholder}
      disabled={!cities.length}
      onChange={(value) => {
        onSelect(value);
      }}
      onSearch={(value) => {
        const nextOptions = options.filter((option) =>
          option.value.toLowerCase().includes(value.toLowerCase())
        );

        setOptions(nextOptions);
      }}
    />
  );
}
