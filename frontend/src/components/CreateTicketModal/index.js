import { DatePicker, Form, Input, message, Modal, Select } from "antd";
import axios from "axios";
import moment from "moment";
import React, { useCallback, useEffect, useState } from "react";
import SeatPicker from "react-seat-picker";
import { baseUrl } from "../../config";

export function CreateTicketModal({ visible, flightId, onClose }) {
  const [form] = Form.useForm();
  const [seat, setSeat] = useState(null);
  const [seats, setSeats] = useState(null);
  const [serverSeats, setServerSeats] = useState(null);
  const [isSelectedSeat, setIsSelectedSeat] = useState(false);

  const handleSelectSeat = useCallback(
    ({ row, number, id }, addCb) => {
      addCb(row, number, id);

      setSeat(serverSeats.find((seat) => seat.id === id));
    },
    [serverSeats]
  );

  const handleRemoveSeat = useCallback(({ row, number, id }, removeCb) => {
    removeCb(row, number, id);
    setSeat(null);
  }, []);

  const submitForm = useCallback(() => {
    form.validateFields().then((fields) => {
      function onSignUp() {
        axios
          .post(`${baseUrl}/api-token-auth/`, {
            username: fields.username,
            password: fields.password,
          })
          .then((response) => {
            if (response.status === 200) {
              axios.post(
                `${baseUrl}/api/ticket/`,
                {
                  seat: seat.id,
                  flight: flightId,
                  total_amount: parseInt(seat.price).toString(),
                },
                {
                  headers: {
                    Authorization: "Token " + response.data.token,
                  },
                }
              );
            }
          })
          .then(() => {
            onClose();
            message.success("Ticked created !!!");
          });
      }

      const props = [
        "email",
        "phone",
        "birthday",
        "username",
        "password",
        "passport_number",
      ].map((prop) => fields[prop]);

      if (props.every(Boolean)) {
        axios
          .post(`${baseUrl}/signup/`, {
            user: {
              username: fields.username,
              password: fields.password,
              email: fields.email,
            },
            phone: fields.phone,
            passport_number: fields.passport_number,
            birthday: moment(fields.birthday).format("YYYY-MM-DD"),
          })
          .then(onSignUp)
          .catch(onSignUp);
      }
    });
  }, [seat, flightId, form, onClose]);

  useEffect(() => {
    axios.get(`${baseUrl}/api/seat/?flight_id=${flightId}`).then((response) => {
      if (response.status === 200) {
        const seatsInRow = 6;
        const nextSeats = [];

        for (let i = 0; i < response.data.length / seatsInRow; i++) {
          const seatsRow = [];

          for (let j = seatsInRow * i; j < seatsInRow * (i + 1); j++) {
            const seat = response.data[j];

            if (j > seatsInRow * i && j % 2 === 0) {
              seatsRow.push(null);
            }

            seatsRow.push({
              id: seat.id,
              number: seat.seat_no,
              isReserved: Boolean(seat.ticket),
            });
          }

          nextSeats.push(seatsRow);
        }

        setSeats(nextSeats);
        setServerSeats(response.data);
      }
    });
  }, [flightId]);

  const prefixSelector = (
    <Form.Item name="prefix" noStyle>
      <Select defaultValue="380" style={{ width: 200 }}>
        <Select.Option value="380">+380</Select.Option>
      </Select>
    </Form.Item>
  );

  return (
    <Modal
      width="50vw"
      title="Select seat"
      visible={visible}
      onCancel={onClose}
      className="create-seats-modal"
      okButtonProps={{ disabled: !seat }}
      onOk={() => (isSelectedSeat ? submitForm() : setIsSelectedSeat(true))}
    >
      {isSelectedSeat && (
        <Form form={form} name="basic" initialValues={{ remember: true }}>
          <Form.Item required label="Username" name="username">
            <Input />
          </Form.Item>

          <Form.Item
            required
            name="email"
            label="Email"
            rules={[{ type: "email" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item required label="Passport number" name="passport_number">
            <Input />
          </Form.Item>

          <Form.Item required label="Password" name="password">
            <Input.Password />
          </Form.Item>

          <Form.Item
            required
            name="phone"
            label="Phone"
            rules={[{ message: "Please input your phone number!" }]}
          >
            <Input addonBefore={prefixSelector} style={{ width: "100%" }} />
          </Form.Item>

          <Form.Item required label="Birthday" name="birthday">
            <DatePicker style={{ width: "100%" }} />
          </Form.Item>
        </Form>
      )}
      {!isSelectedSeat && (
        <div>
          {seat && (
            <div
              className="seat-name"
              style={{ display: "flex", justifyContent: "space-between" }}
            >
              <h3>Price: {parseInt(seat.price)}</h3>
              <h3>Class: {seat.fare_condition}</h3>
            </div>
          )}
          {seats && (
            <SeatPicker
              alpha
              visible
              rows={seats}
              loading={false}
              selectedByDefault
              maxReservableSeats={1}
              addSeatCallback={handleSelectSeat}
              removeSeatCallback={handleRemoveSeat}
            />
          )}
        </div>
      )}
    </Modal>
  );
}
