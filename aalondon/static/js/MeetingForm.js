import React, { useEffect, useState } from 'react';
import ReactDOM from "react-dom";
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import moment from 'moment';

import getCookie from './components/getCookie';
import axios from 'axios'
import MeetingFields from './components/MeetingFields'
import MeetingFormSuccess from './components/MeetingFormSuccess'
import MeetingFormType from './components/MeetingFormType'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


function MeetingForm(props) {

  const [threeWords, setThreeWords] = useState('')
  const [activeStep, setActiveStep] = useState(0);
  const [formType, setFormType] = useState(meetingData.formType)




  async function _submitForm(fields, actions) {

    let csrftoken = getCookie('csrftoken');
    let days = fields.days.map((day, index) => {
      return { value: day }
    })

    let subTypes = []
    if (fields.open) subTypes.push({ value: "Open" })
    if (fields.wheelchair) subTypes.push({ value: "Wheelchair Access" })
    if (fields.signed) subTypes.push({ value: "British Sign Language" })
    if (fields.lgbt) subTypes.push({ value: "LGBTQ" })
    if (fields.chits) subTypes.push({ value: "Chits" })
    if (fields.childFriendly) subTypes.push({ value: "Child-Friendly" })
    if (fields.hearingLoop) subTypes.push({ value: "Hearing Loop" })
    if (fields.creche) subTypes.push({ value: "Creche" })
    if (fields.temporaryClosure) subTypes.push({ value: "Location Temporarily Closed" })

    let data = {
      title: fields.title,
      type: formType,
      time: fields.startTime,
      end_time: fields.endTime,
      email: fields.email,
      days: days,
      location: fields.location,
      address: fields.address,
      postcode: fields.postcode,
      online_link: fields.link,
      online_password: fields.password,
      intergroup: fields.intergroup,
      submission: fields.submission,
      tradition_7_details: fields.tradition7Details,
      what_three_words: fields.whatThreeWords,
      description: fields.description,
      notes: fields.notes,
      sub_types: subTypes,
      gso_opt_out: fields.gsoOptOut,
    }

    axios.post('/api/meetingadd/', data,
      {
        headers: {
          'XCSRF-TOKEN': csrftoken,
        },
      }).then(response => {

        setActiveStep(1);
        return response.data;

      })
      .catch(error => {
        return error.response;
      });
  }

  function _renderStepContent(step, errors, touched, values) {

    switch (step) {
      case 0:
        return <MeetingFields setFormType={setFormType} setThreeWords={setThreeWords} errors={errors} touched={touched} formType={formType} values={values} />;
      case 1:
        return <MeetingFormSuccess />;
      default:
        return <div>Not Found</div>;
    }
  }

  let validationAllShape = {

    days: Yup.array()
      .test("not-empty", "You must select at least one day of the week", function (value) {
        if (value === undefined) {
          return false
        } else if (value.length === 0) {
          return false
        }
        else {
          return true
        }

      }),
    title: Yup.string()
      .required('Title is required'),
    submission: Yup.string()
      .required('Submission type is required'),

    startTime: Yup.string()
      .required('Start time is required')
      .test("is-valid", "Start time needs to be in 24 hour format e.g. 13:30", function (value) {
        return moment(value, "HH:mm", true).isValid();
      }),
    endTime: Yup.string()
      .required('End time is required')
      .test("is-valid", "End time needs to be in 24 hour format e.g. 14:30", function (value) {
        return moment(value, "HH:mm", true).isValid();
      }),
    email: Yup.string()
      .email('Email is invalid')
      .required('Email is required'),

    description: Yup.string()
      .required('Description is required'),

  };

  let validationPhysicalShape =
  {
    whatThreeWords: Yup.string()
      .required('What3Words is required'),
    postcode: Yup.string()
      .required('Postcode is required')
      .test("is-valid","postcode needs to be from UK", function(value){
        let value_str = value || '';
        let regex = new RegExp(/^([A-Z]{1,2}\d{1,2}[A-Z]?)\s*(\d[A-Z]{2})$/)
        return regex.test(value_str.replaceAll(' ', ''))
        
      })
      .test("is-valid","postcode has maximum 1 space", function(value){
       let value_str = value || '';
       let spaces = value_str.length - value_str.replaceAll(' ', '').length;
        return spaces < 2
      })
      ,
      location: Yup.string()
      .required('Location is required'),
      address: Yup.string()
      .required('Address is required'),
  }

  let validationOnlineShape = {
    link: Yup.string()
      .required('Link is required')
      .url('Please enter valid url!'),

  }

  let finalValidationShape
  if (formType === 'HYB') {
    finalValidationShape = { ...validationAllShape, ...validationPhysicalShape, ...validationOnlineShape }
  } else if (formType === 'F2F') {
    finalValidationShape = { ...validationAllShape, ...validationPhysicalShape }
  } else {
    finalValidationShape = { ...validationAllShape, ...validationOnlineShape }
  }
  const validationSchema = Yup.object().shape(finalValidationShape);


  let open
  let wheelchair
  let signed
  let lgbt
  let chits
  let childFriendly
  let hearingLoop
  let creche
  let temporaryClosure



  for (const subType of meetingData.subTypes) {
    if (subType === "Child-Friendly") {
      childFriendly = true
    } else if (subType === "LGBTQ") {
      lgbt = true
    } else if (subType === "Location Temporarily Closed") {
      temporaryClosure = true
    } else if (subType === "Hearinh Loop") {
      hearingLoop = true
    } else if (subType === "Wheelchair Access") {
      wheelchair = true
    } else if (subType === "British Sign Language") {
      signed = true
    } else if (subType === "Chits") {
      chits = true
    } else if (subType === "Creche") {
      creche = true
    } else if (subType === "Open") {
      open = true
    }
  }




  return (
    <Formik
      initialValues={{
        formType: formType,
        title: meetingData.title,
        days: meetingData.days,
        submission: meetingData.submission,
        intergroup: meetingData.intergroup,
        startTime: meetingData.startTime,
        endTime: meetingData.endTime,
        link: meetingData.link,
        password: meetingData.password,
        tradition7Details: meetingData.tradition7Details,
        location: meetingData.location,
        address: meetingData.address,
        postcode: meetingData.postcode,
        whatThreeWords: meetingData.whatThreeWords,
        email: '',
        description: meetingData.description,
        notes: '',
        open: open,
        wheelchair: wheelchair,
        signed: signed,
        lgbt: lgbt,
        chits: chits,
        childFriendly: childFriendly,
        hearingLoop: hearingLoop,
        creche: creche,
        temporaryClosure: temporaryClosure,
        gsoOptOut: false
      }}
      validationSchema={validationSchema}
      onSubmit={_submitForm}>
      {({ errors, status, touched, values }) => (

        <Form id="new-meeting-form">
          {_renderStepContent(activeStep, errors, touched, values)}

          {formType && activeStep === 0 &&
            <div className="form-group">
              <button type="submit" className="btn btn-primary mr-2">Submit</button>
              <button type="reset" className="btn btn-secondary">Reset</button>
              <div>*Click <b><u><a target="_blank" href="/about-us/terms-service/">here</a></u></b> for our Privacy Terms.</div>
            </div>
          }

        </Form>
      )}
    </Formik>
  )
}

ReactDOM.render(<MeetingForm />, document.getElementById("root"));
