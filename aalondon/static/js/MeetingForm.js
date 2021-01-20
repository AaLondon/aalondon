import React from "react";
import ReactDOM from "react-dom";
import { Formik, Field, Form } from "formik";
import "../css/meetingform.css";
import { Dropdown, Input } from 'semantic-ui-react'
import OnlineForm from './components/OnlineForm'
import PhysicalForm from "./components/PhysicalForm";
import HybridForm from "./components/HybridForm";


const formTypes = [
    {
        key: 'online',
        text: 'Online only',
        value: 'online',

    },
    {
        key: 'faceToFace',
        text: 'Face to Face',
        value: 'faceToFace',

    },
    {
        key: 'hybrid',
        text: 'Hybrid',
        value: 'hybrid',

    }]




function MeetingForm() {
    const [formType, setFormType] = React.useState('select')
    let activeForm =<></>
    if (formType == 'online') {
        activeForm = <OnlineForm  formType={formType}/>

    }
    else if (formType == 'physical') {
        activeForm = <PhysicalForm formType={formType} />

    }
    else if (formType == 'hybrid') {
        activeForm = <HybridForm formType={formType}/>

    }
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




ReactDOM.render(<MeetingForm />, document.getElementById("root"));
