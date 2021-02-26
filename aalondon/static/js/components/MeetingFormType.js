import React from "react";
import ReactDOM from "react-dom";
import { Formik, Field, Form } from "formik";
import "../../css/meetingform.css";
import { Dropdown, Input } from 'semantic-ui-react'



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




export default function MeetingFormType(props) {
    
   const { setFormType ,setActiveStep} = props;
    
    return (
        <React.Fragment>
            <label htmlFor="notes">Meeting Type(Hybrid,Online or Physical)</label>
            <Dropdown
                placeholder='Please choose meeting type'
                // fluid
                selection
                options={formTypes}
                icon='dropdown'
                onChange={(e, data) => {
                setFormType(data.value)
                setActiveStep(1)
                
                }}
                scrolling={false}
            />
       
       </React.Fragment>
    )

}




ReactDOM.render(<MeetingFormType />, document.getElementById("root"));
