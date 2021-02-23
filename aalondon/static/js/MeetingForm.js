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
  const [formType, setFormType] = useState('')
  console.log('sasas')
  async function _submitForm(fields, actions) {
 
        const w3w = threeWords;
        let csrftoken = getCookie('csrftoken');
        let days = fields.days.map((day,index)=>{
            return {value:day}
          })

          let subTypes=[]
          if (fields.wheelchair) subTypes.push({value:"Wheelchair Access"})
          if (fields.signed) subTypes.push({value:"British Sign Language"})
          if (fields.lgbt) subTypes.push({value:"LGBTQ"})
          if (fields.chits) subTypes.push({value:"Chits"})
          if (fields.childFriendly) subTypes.push({value:"Child-Friendly"})
          if (fields.outdoors) subTypes.push({value:"Outdoor"})
          if (fields.creche) subTypes.push({value:"Creche"})
          if (fields.temporaryClosure) subTypes.push({value:"Location Temporarily Closed"})

          axios.post('/api/meetingneuf/', {
            title: fields.title,
            type: formType,
            time:fields.startTime,
            email:fields.email,
            days:days,
            address:fields.address,
            postcode:fields.postcode,
            online_link:fields.link,
            online_password:fields.password,
            intergroup:fields.intergroup,
            submission:fields.submission,
            payment_details:fields.paymentLink,
            what_three_words:w3w,
            description: fields.description,
            notes:fields.notes,
            sub_types:subTypes,
     },
            {
              headers: {
                'XCSRF-TOKEN': csrftoken,
              },
            }).then(response => {
              console.log(response.data);
              setActiveStep(1);
              return response.data;
              
            })
            .catch(error => {
              console.log(error.response);
            });
  }

  function _renderStepContent(step,errors,touched) {
   
    switch (step) {
      case 0:
        return <MeetingFields setFormType={setFormType} setThreeWords={setThreeWords} errors={errors} touched={touched} formType={formType}/> ;
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
    email: Yup.string()
      .email('Email is invalid')
      .required('Email is required'),
    description: Yup.string()
      .required('Description is required'),

  };

  let validationPhysicalShape =
  {
    postcode: Yup.string()
      .required('Postcode is required'),
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

  return (
    <Formik
      initialValues={{
        formType: '',
        title:'',
        days: '',
        submission: '',
        intergroup: '',
        startTime: '',
        link: '',
        password: '',
        paymentLink: '',
        address: '',
        postcode: '',
        '3wa': '',
        email: '',
        description: '',
        notes: '',
        wheelchair: true,
        signed: false,
        lgbt: false,
        chits: false,
        childFriendly: false,
        outdoors: false,
        creche: false,
        temporaryClosure: false
      }}
      validationSchema={validationSchema}
      onSubmit={_submitForm}>
      {({ errors, status, touched }) => (
       
        <Form id="new-meeting-form">
          {_renderStepContent(activeStep,errors,touched)}

     {formType && activeStep===0  &&
        <div className="form-group">
        <button type="submit" className="btn btn-primary mr-2">Submit</button>
        <button type="reset" className="btn btn-secondary">Reset</button>
      </div>
      }
      
        </Form>
      )}
    </Formik>
  )
}

ReactDOM.render(<MeetingForm/>, document.getElementById("root"));
