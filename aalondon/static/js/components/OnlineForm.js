import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Dropdown, TextArea, Checkbox } from 'semantic-ui-react'
import moment from 'moment';
import  SemanticField  from '../components/SemanticField'


const submitOptions = [
  {
    key: 'new',
    text: 'New',
    value: 'new',

  },
  {
    key: 'existing',
    text: 'Existing',
    value: 'existing',

  }]

const dayOptions = [
  {
    key: 'Monday',
    text: 'Monday',
    value: 'Monday',

  },
  {
    key: 'Tuesday',
    text: 'Tuesday',
    value: 'Tuesday',

  },
  {
    key: 'Wednesday',
    text: 'Wednesday',
    value: 'Wednesday',

  },
  {
    key: 'Thursday',
    text: 'Thursday',
    value: 'Thursday',

  },
  {
    key: 'Friday',
    text: 'Friday',
    value: 'Friday',

  },
  {
    key: 'Saturday',
    text: 'Saturday',
    value: 'Saturday',

  },
  {
    key: 'Sunday',
    text: 'Sunday',
    value: 'Sunday',

  },

]




function OnlineForm(props) {




  return (
    <Formik
      initialValues={{
        formType:props.formType,
        day: '',
        startTime: '',
        link:'',
        paymentLink: '',
        email: '',
        description: '',
        notes: '',
      }}
      validationSchema={Yup.object().shape({
        day: Yup.array()
          .test("not-empty","You must select at least one day of the week", function(value){
            if (value === undefined){
              return false
            }else if (value.length === 0)
            {
              return false
            }
            else {
              return true
            }
            
          }),
        startTime: Yup.string()
          .required('Start time is required')
          .test("is-valid", "Start time needs to be in 24 hour format e.g. 13:30", function (value) {
            return moment(value, "HH:mm", true).isValid();
          }),
          link: Yup.string()
          .required('Link is required')
          .url('Please enter valid url!'),
        email: Yup.string()
          .email('Email is invalid')
          .required('Email is required'),
        description: Yup.string()
          .required('Description is required'),
      })}
      onSubmit={fields => {
        alert('SUCCESS!! :-)\n\n' + JSON.stringify(fields, null, 4))
      }}>
      {({ errors, status, touched }) => (
        <Form>
          <div className="form-group">
            <label htmlFor="day">Day</label>
            <SemanticField
              name="day"
              component={Dropdown}
              options={dayOptions}
              multiple
              selection
              placeholder="Please select day of week"
              id={"day"}
              value={[]}
              className={'form-control' + (errors.day && touched.day ? ' is-invalid' : '')}
            />
            

            <ErrorMessage name="day" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="day">Day</label>
            <SemanticField
              name="submission"
              component={Dropdown}
              options={dayOptions}
              selection
              placeholder="Is this a new meeting or are you updating an existing one?"
              id={"day"}
              value={[]}
              className={'form-control' + (errors.day && touched.day ? ' is-invalid' : '')}
            />
            

            <ErrorMessage name="day" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="startTime">Start Time</label>
            <Field placeholder="Start time needs to be in 24 hour format e.g. 13:30" name="startTime" type="text" className={'form-control' + (errors.startTime && touched.startTime ? ' is-invalid' : '')} />
            <ErrorMessage name="startTime" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="link">Online Meeting Link</label>
            <Field placeholder="Please enter online meeting link. Zoom,Skype etc" name="link" type="text" className={'form-control' + (errors.link && touched.link ? ' is-invalid' : '')} />
            <ErrorMessage name="link" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="paymentLink">Payment Link</label>
            <Field placeholder="Paypal,Cashapp,Square... etc link"name="paymentLink" type="text" className={'form-control' + (errors.paymentLink && touched.paymentLink ? ' is-invalid' : '')} />
            <ErrorMessage name="paymentLink" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <Field placeholder="Please use a generic group email address." name="email" type="text" className={'form-control' + (errors.email && touched.email ? ' is-invalid' : '')} />
            <ErrorMessage name="email" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <Field name="description" component="textarea" type="text" className={'form-control' + (errors.description && touched.description ? ' is-invalid' : '')} />
            <ErrorMessage name="description" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <Field name="notes" component="textarea" type="text" className={'form-control' + (errors.notes && touched.notes ? ' is-invalid' : '')} />
            <ErrorMessage name="notes" component="div" className="invalid-feedback" />
          </div>
          
         

          <div className="form-group">
            <button type="submit" className="btn btn-primary mr-2">Submit</button>
            <button type="reset" className="btn btn-secondary">Reset</button>
          </div>



        </Form>
      )}
    </Formik>
  )
}

export default OnlineForm
