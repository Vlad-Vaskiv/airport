import React from "react";
import { Table } from "antd";

const columns = [
  {
    title: "Flight code",
    dataIndex: "flight_code",
    key: "flight_code",
    // eslint-disable-next-line
    render: (text) => <a>{text}</a>,
  },
  {
    title: "Departure Airport",
    dataIndex: "departure_airport",
    key: "departure_airport",
  },
  {
    title: "Arrival Airport",
    dataIndex: "arrival_airport",
    key: "arrival_airport",
  },
  {
    title: "Aircraft",
    dataIndex: "aircraft",
    key: "address",
  },
  {
    title: "Scheduled arrival",
    key: "scheduled_arrival",
    dataIndex: "scheduled_arrival",
  },
  {
    title: "Scheduled Departure",
    key: "scheduled_departure",
    dataIndex: "scheduled_departure",
  },
];
export function FlightTable({ data, ...props }) {
  const { onSelectFlight } = props;

  return (
    <Table
      bordered
      columns={columns}
      dataSource={data}
      onRow={(record) => ({
        onClick: () => onSelectFlight && onSelectFlight(record.key),
      })}
    />
  );
}
