import React from "react";
import { useField } from "formik";
import DatePicker from "react-datepicker";

// Styles
import "react-datepicker/dist/react-datepicker.css";

const DatePickerField = ({css="", name = "" }) => {
    const [field, meta, helpers] = useField(name);
  
    const { value } = meta;
    const { setValue } = helpers;
  
    return (
      <DatePicker
        {...field}
        id="meetingCalendarInput"
        className={css}
        selected={value}
        dateFormat="yyyy-MM-dd"
        onChange={(date) => setValue(date)}
      />
    );
  };


export default DatePickerField;