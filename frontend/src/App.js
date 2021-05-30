import { Button, DatePicker } from "antd";
import axios from "axios";
import * as React from "react";
import { useCallback, useEffect, useState } from "react";
import { CityInput } from "./components/CityInput";
import { baseUrl } from "./config";
import { getAddressesFx } from "./stores";
import qs from "querystring";
import moment from "moment";
import { FlightTable } from "./components/FlightTable";
import { CreateTicketModal } from "./components/CreateTicketModal";

function App() {
  const [date, setDate] = useState(null);
  const [cityFrom, setCityFrom] = useState(null);
  const [cityTo, setCityTo] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [modal, setModal] = useState(null);

  useEffect(() => {
    getAddressesFx();
  }, []);

  const handleSubmitForm = useCallback(() => {
    const params = qs.stringify({
      departure_airport__address__city: cityFrom,
      arrival_airport__address__city: cityTo,
      scheduled_departure: moment(date).format("DD-MM-YYYY"),
    });

    axios.get(`${baseUrl}/api/flight/?${params}`).then((response) => {
      if (response.status === 200) {
        setTableData(() =>
          response.data.map((flight) => ({
            key: flight.id,
            flight_code: flight.flight_no,
            arrival_airport: flight.arrival_airport.name,
            departure_airport: flight.departure_airport.name,
            aircraft: flight.aircraft.model.name,
            scheduled_arrival: moment(flight.scheduled_departure).format(
              "YYYY-MM-DD HH:mm"
            ),
            scheduled_departure: moment(flight.scheduled_departure).format(
              "YYYY-MM-DD HH:mm"
            ),
          }))
        );

        setTimeout(
          () => window.scroll({ top: 1000000, left: 0, behavior: "smooth" }),
          100
        );
      }
    });
  }, [date, cityFrom, cityTo]);

  const showTicketModal = useCallback((flightId) => {
    setModal(
      <CreateTicketModal
        flightId={flightId}
        visible={Boolean(flightId)}
        onClose={() => setModal(null)}
      />
    );
  }, []);

  return (
    <div className="app">
      {modal && modal}
      <div className="header">
        <h1 style={{ color: "#2f5073" }}>Vaskiv Airlines</h1>

        <div className="flight-configurator">
          <div className="cities-selector">
            <CityInput placeholder="From" onSelect={setCityFrom} />
            <img alt="" src="https://svgsilh.com/svg_v2/154271.svg" />
            <CityInput placeholder="To" onSelect={setCityTo} />
          </div>
          <DatePicker onChange={setDate} style={{ width: "100%" }} />
          <Button
            shape="round"
            type="primary"
            onClick={handleSubmitForm}
            style={{ background: "#2f5073", borderColor: "#2f5073" }}
          >
            Find
          </Button>
        </div>
      </div>
      {tableData?.length && (
        <div className="info-bloc">
          <div className="flights">
            <FlightTable data={tableData} onSelectFlight={showTicketModal} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
