import React from "react";
import ReactDOM from "react-dom";
import { Formik, Field, Form } from "formik";
import "../css/meetingform.css";
import { Dropdown, Input } from 'semantic-ui-react'
import MeetingForm from "./components/MeetingForm";


const formTypes = [
    {
        key: 'ONL',
        text: 'Online only',
        value: 'ONL',

    },
    {
        key: 'F2F',
        text: 'Face to Face',
        value: 'F2F',

    },
    {
        key: 'HYB',
        text: 'Hybrid',
        value: 'HYB',

    }]




function MeetingFormSelector() {
    const [formType, setFormType] = React.useState('select')
    let activeForm =<></>
  
    activeForm = formType === 'select' ? <></> : <MeetingForm formType={formType}/> 
    
    return (
        <>
            <label htmlFor="notes">Meeting Type(Hybrid,Online or Physical)</label>
            <Dropdown
                placeholder='Please choose meeting type'
                // fluid
                selection
                options={formTypes}
                icon='dropdown'
                onChange={(e, data) => setFormType(data.value)}
                scrolling={false}
            />
            {activeForm}
        </>
    )

}




ReactDOM.render(<MeetingFormSelector />, document.getElementById("root"));
