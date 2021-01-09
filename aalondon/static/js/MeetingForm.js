import React from "react";
import ReactDOM from "react-dom";
import { Formik, Field, Form } from "formik";
import "../css/meetingform.css";
import { Dropdown, Input } from 'semantic-ui-react'
import OnlineForm from './components/OnlineForm'
import PhysicalForm from "./components/PhysicalForm";
import HybridForm from "./components/HybridForm";


const formStages = [
    {
        key: 'online',
        text: 'Online',
        value: 'online',

    },
    {
        key: 'physical',
        text: 'Physical',
        value: 'physical',

    },
    {
        key: 'hybrid',
        text: 'Hybrid',
        value: 'hybrid',

    }]


function MeetingForm() {
    const [formStage, setFormStage] = React.useState('select')
    let activeForm =<></>
    if (formStage == 'online') {
        activeForm = <OnlineForm />

    }
    else if (formStage == 'physical') {
        activeForm = <PhysicalForm />

    }
    else if (formStage == 'hybrid') {
        activeForm = <HybridForm />

    }
    return (
        <>
            <Dropdown
                placeholder='Please choose meeting type'
                // fluid
                selection
                options={formStages}
                icon='dropdown'
                onChange={(e, data) => setFormStage(data.value)}
                scrolling={false}
            />
            {activeForm}
        </>
    )

}




ReactDOM.render(<MeetingForm />, document.getElementById("root"));
