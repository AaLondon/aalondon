import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Dropdown, TextArea, Checkbox } from 'semantic-ui-react'
import moment from 'moment';
import SemanticField from '../components/SemanticField'



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

const intergroupOptions =[
{
  key: 'City Of London',
  text: 'City Of London',
  value: 'City Of London"',
},
{
  key: 'East London',
  text: 'East London',
  value: 'East London',
},
{
  key: 'Chelsea',
  text: 'Chelsea',
  value: 'Chelsea',
},
{
  key: 'Chelsea & Fulham',
  text: 'Chelsea & Fulham',
  value: 'Chelsea & Fulham',
},
{
  key: 'London North East',
  text: 'London North East',
  value: 'London North East',
},
{
  key: 'London North',
  text: 'London North',
  value: 'London North',
},
{
  key: 'London North Middlesex',
  text: 'London North Middlesex',
  value: 'London North Middlesex',
},
{
  key: 'London North West',
  text: 'London North West',
  value: 'London North West',
},
{
  key: 'London South Middlesex',
  text: 'London South Middlesex',
  value: 'London South Middlesex',
},
{
  key: 'London West End',
  text: 'London West End',
  value: 'London West End',
},

{
  key: 'London Westway',
  text: 'London Westway',
  value: 'London Westway',
},

{
  key: 'London Croydon Epsom & Sutton',
  text: 'London Croydon Epsom & Sutton',
  value: 'London Croydon Epsom & Sutton',
},
{
  key: 'London North Kent',
  text: 'London North Kent',
  value: 'London North Kent',
},
{
  key: 'London South East (East)"',
  text: 'London South East (East)"',
  value: 'London South East (East)"',
},
{
  key: 'London South East (West)',
  text: 'London South East (West)',
  value: 'London South East (West)',
},
{
  key: 'London South',
  text: 'London South',
  value: 'London South',
},
{
  key: 'London South West',
  text: 'London South West',
  value: 'London South West',
},


]



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




function HybridForm(props) {




  return (
    <Formik
      initialValues={{
        formType: props.formType,
        day: '',
        submission:'',
        intergroup:'',
        startTime: '',
        link: '',
        password:'',
        paymentLink: '',
        address: '',
        postcode: '',
        whatThreeWords: '',
        email: '',
        description: '',
        notes: '',
        wheelchair: false,
        signed: false,
        lgbt: false,
        chits: false,
        childFriendly: false,
        outdoors: false,
        creche: false,
        temporaryClosure: false
      }}
      validationSchema={Yup.object().shape({
        day: Yup.array()
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

        submission: Yup.string()
          .required('Submission type is required'),

        startTime: Yup.string()
          .required('Start time is required')
          .test("is-valid", "Start time needs to be in 24 hour format e.g. 13:30", function (value) {
            return moment(value, "HH:mm", true).isValid();
          }),
        link: Yup.string()
          .required('Link is required')
          .url('Please enter valid url!'),

        postcode: Yup.string()
          .required('Postcode is required'),
        address: Yup.string()
          .required('Address is required'),
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
            <label htmlFor="submission">Submission</label>
            <SemanticField
              name="submission"
              component={Dropdown}
              options={submitOptions}
              selection
              placeholder="Is this a new meeting or are you updating an existing one?"
              id={"submission"}
              className={'form-control' + (errors.submission && touched.submission ? ' is-invalid' : '')}
            />

            <ErrorMessage name="submission" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="intergroup">Intergroup</label>
            <SemanticField
              name="intergroup"
              component={Dropdown}
              options={intergroupOptions} 
              selection
              placeholder="Intergroup if your group is part of one?"
              id={"intergroup"}
              className={'form-control' + (errors.intergroup && touched.intergroup ? ' is-invalid' : '')}
            />
            <ErrorMessage name="intergroup" component="div" className="invalid-feedback" />
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
            <label htmlFor="password">Online Meeting Password</label>
            <Field placeholder="Please enter password" name="link" type="text" className={'form-control' + (errors.password && touched.password ? ' is-invalid' : '')} />
            <ErrorMessage name="password" component="password" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="address">Address</label>
            <Field name="address" type="text" className={'form-control' + (errors.address && touched.address ? ' is-invalid' : '')} />
            <ErrorMessage name="address" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="postcode">Postcode</label>
            <Field name="postcode" type="text" className={'form-control' + (errors.postcode && touched.postcode ? ' is-invalid' : '')} />
            <ErrorMessage name="postcode" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="paymentLink">Payment Link</label>
            <Field placeholder="Paypal,Cashapp,Square... etc link" name="paymentLink" type="text" className={'form-control' + (errors.paymentLink && touched.paymentLink ? ' is-invalid' : '')} />
            <ErrorMessage name="paymentLink" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="whatThreeWords">What Three Words(<a target="_blank" href="https://what3words.com/">Click here</a>)</label>
            <what3words-autosuggest
              id="autosuggest"
              placeholder="What three words tells us precisely where you are. Click above for info." />
            <ErrorMessage name="whatThreeWords" component="div" className="invalid-feedback" />
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

          <div className="auto-grid" role="group" aria-labelledby="checkbox-group">
            <div><span className="checkbox-title" htmlFor="wheelchair">Wheel Chair</span>
              <SemanticField
                name="wheelchair"
                component={Checkbox}
              />
            </div>
            <div>
              <span className="checkbox-title" htmlFor="creche">Creche</span>
              <SemanticField
                name="creche"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="signed">Signed</span>
              <SemanticField
                name="signed"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="lgbt">LGBT</span>
              <SemanticField
                name="lgbt"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="chits">Chits</span>
              <SemanticField
                name="chits"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="childFriendly">Child Friendly</span>
              <SemanticField
                name="childFriendly"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="outdoors">Outdoors</span>
              <SemanticField
                name="outdoors"
                component={Checkbox}
              />

            </div>
            <div>
              <span className="checkbox-title" htmlFor="temporaryClosure">Temporary Closure</span>
              <SemanticField
                name="temporaryClosure"
                component={Checkbox}
              />

            </div>
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

export default HybridForm
