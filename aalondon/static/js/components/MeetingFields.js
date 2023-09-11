import React, { useEffect, useState, useRef } from 'react';
import { Field, ErrorMessage } from 'formik';
import SemanticField from './SemanticField'
import { Dropdown, TextArea, Checkbox } from 'semantic-ui-react'
import axios from 'axios'


const CheckboxExampleChecked = () => (
  <Checkbox defaultChecked />
)


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

const intergroupOptions = [
  {
    key: 'City Of London',
    text: 'City Of London',
    value: 'City Of London',
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
    key: 'London South East (East)',
    text: 'London South East (East)',
    value: 'London South East (East)',
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
  {
    key: 'Poles in the UK',
    text: 'Poles in the UK',
    value: 'Poles in the UK',
  },


]



const dayOptions = [
  {
    key: 1,
    text: 'Monday',
    value: 'Monday',

  },
  {
    key: 2,
    text: 'Tuesday',
    value: 'Tuesday',

  },
  {
    key: 3,
    text: 'Wednesday',
    value: 'Wednesday',

  },
  {
    key: 4,
    text: 'Thursday',
    value: 'Thursday',

  },
  {
    key: 5,
    text: 'Friday',
    value: 'Friday',

  },
  {
    key: 6,
    text: 'Saturday',
    value: 'Saturday',

  },
  {
    key: 7,
    text: 'Sunday',
    value: 'Sunday',

  },

]


export default function MeetingFields(props) {


  const whatThreeRef = useRef(null);

  console.log('formTypeee')
  console.log(props.formType)
  console.log('formTypeeee')

  const
    { errors, touched, activeStep, formType, setFormType, setThreeWords, values }
      = props;

  useEffect(() => {

    if (whatThreeRef && whatThreeRef.current) {
      const autosuggest = window.document.querySelector('what3words-autosuggest')
      autosuggest.addEventListener('change', e => {
        const words = e.detail
        setThreeWords(words)
      })
      console.log("Created");
      return () => {
        console.log("Cleaned up");
        autosuggest.removeEventListener('change', e => { })
      };
    }
  }, [formType]);

  function onSubmissionTypeChangeAutofill(e, data, setFieldValue) {
    let title = props.values.title
    let type = formType
    let submission = data


    if (submission === 'existing') {
      axios.get(`/api/meetingautofill/?title=${title}&type=${type}`)
        .then(response => {

          let result = response.data.results[0]
          if (result) {
            setFieldValue('address', result.address ? result.address : '')
            setFieldValue('startTime', result.friendly_time)
            setFieldValue('endTime', result.friendly_end_time)
            setFieldValue('type', result.type)
            setFieldValue('postcode', result.postcode ? result.postcode : '')
            setFieldValue('intergroup', result.intergroup ? result.intergroup : '')
            setFieldValue('link', result.online_link ? result.online_link : '')
            setFieldValue('password', result.online_password ? result.online_password : '')
            setFieldValue('address', result.address ? result.address : '')
            setFieldValue('tradition7Details', result.tradition_7_details ? result.tradition_7_details : '')
            setFieldValue('whatThreeWords', result.what_three_words ? result.what_three_words : '')
            setFieldValue('description', result.description)
            setFieldValue('gsoOptOut', result.gso_opt_out)
            setFieldValue('days', result.days.map(day => day.value))

            let subTypes = result.sub_types.map(sub_type => sub_type.value)

            for (const subType of subTypes) {
              if (subType === "Child-Friendly") {
                setFieldValue('childFriendly', true)
              } else if (subType === "LGBTQ") {
                setFieldValue('lgbt', true)
              } else if (subType === "Location Temporarily Closed") {
                setFieldValue('temporaryClosure', true)
              } else if (subType === "Outdoor") {
                setFieldValue('outdoors', true)
              } else if (subType === "Wheelchair Access") {
                setFieldValue('wheelchair', true)
              } else if (subType === "British Sign Language") {
                setFieldValue('signed', true)
              } else if (subType === "Chits") {
                setFieldValue('chits', true)
              } else if (subType === "Creche") {
                setFieldValue('creche', true)
              } else if (subType === "Open") {
                setFieldValue('open', true)
              }
            }

          }


        });
    }

    console.log('onSubmissionTypeChangeAutofill')
  }


  return (
    <React.Fragment>
      <label htmlFor="notes">Meeting Type (Hybrid, Online or Face to Face)*</label>
      <Dropdown
        placeholder='Please choose meeting type'
        // fluid
        selection
        options={formTypes}
        icon='dropdown'
        value={props.formType}
        onChange={(e, data) => {

          setFormType(data.value)


        }}
        scrolling={false}
      />
      {formType &&
        <>
          <div className="form-group">
            <label htmlFor="title">Title*</label>
            <Field placeholder="Please supply your meeting name" name="title" type="text" className={'form-control' + (errors.title && touched.title ? ' is-invalid' : '')} />
            <ErrorMessage name="title" component="div" className="invalid-feedback" />
          </div>

          <div className="form-group">
            <label htmlFor="submission">Is this a new entry to AA-London.com, or an update to an existing entry?* </label>
            <SemanticField
              name="submission"
              component={Dropdown}
              options={submitOptions}
              onChange={onSubmissionTypeChangeAutofill}
              selection
              placeholder="Is this a new entry to AA-London.com?"
              id={"submission"}
              className={'form-control' + (errors.submission && touched.submission ? ' is-invalid' : '')}
            />

            <ErrorMessage name="submission" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="days">Days*</label>
            <SemanticField
              name="days"
              component={Dropdown}
              options={dayOptions}
              multiple
              selection
              placeholder="Please select day(s) of the week"
              id={"days"}
              value={[]}
              className={'form-control' + (errors.day && touched.day ? ' is-invalid' : '')}

            />

            <ErrorMessage name="days" component="div" className="invalid-feedback" />
          </div>


          <div className="form-group">
            <label htmlFor="intergroup">Intergroup</label>
            <SemanticField
              name="intergroup"
              component={Dropdown}
              options={intergroupOptions}
              selection
              placeholder="Intergroup - if any?"
              id={"intergroup"}
              className={'form-control' + (errors.intergroup && touched.intergroup ? ' is-invalid' : '')}
            />
            <ErrorMessage name="intergroup" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group form-group-time">
            <span><label htmlFor="startTime">Start Time*</label>
              <Field placeholder="e.g. 18:00" name="startTime" type="text" className={'form-control' + (errors.startTime && touched.startTime ? ' is-invalid' : '')} />
              <ErrorMessage name="startTime" component="div" className="invalid-feedback" /></span>
            <span><label htmlFor="endTime">End Time*</label>
              <Field placeholder="e.g. 19:00" name="endTime" type="text" className={'form-control' + (errors.endTime && touched.endTime ? ' is-invalid' : '')} />
              <ErrorMessage name="endTime" component="div" className="invalid-feedback" />
            </span>
          </div>

          {formType !== 'F2F' &&
            <><div className="form-group">
              <label htmlFor="link">Online Meeting Link*</label>
              <Field placeholder="Please enter online meeting link. Zoom, Skype etc" name="link" type="text" className={'form-control' + (errors.link && touched.link ? ' is-invalid' : '')} />
              <ErrorMessage name="link" component="div" className="invalid-feedback" />
            </div>

              <div className="form-group">
                <label htmlFor="password">Online Meeting Password</label>
                <Field placeholder="Please enter password" name="password" type="text" className={'form-control' + (errors.password && touched.password ? ' is-invalid' : '')} />
                <ErrorMessage name="password" component="password" className="invalid-feedback" />
              </div></>}
          {formType !== 'ONL' &&
            <>
            <div className="form-group">
              <label htmlFor="location">Location*</label>
              <Field name="location" placeholder="e.g. Hinde Street Methodist Church" type="text" className={'form-control' + (errors.location && touched.location ? ' is-invalid' : '')} />
              <ErrorMessage name="location" component="div" className="invalid-feedback" />
            </div>
            <div className="form-group">
              <label htmlFor="address">Address*</label>
              <Field name="address" placeholder="e.g. 19 Hinde Street" type="text" className={'form-control' + (errors.address && touched.address ? ' is-invalid' : '')} />
              <ErrorMessage name="address" component="div" className="invalid-feedback" />
            </div>
              <div className="form-group">
                <label htmlFor="postcode">Postcode*</label>
                <Field name="postcode" type="text" className={'form-control' + (errors.postcode && touched.postcode ? ' is-invalid' : '')} />
                <ErrorMessage name="postcode" component="div" className="invalid-feedback" />
              </div></>}
          <div className="form-group">
            <label htmlFor="tradition7Details">Payment Link</label>
            <Field placeholder="Paypal, Cashapp, Square... etc link" name="tradition7Details" type="text" className={'form-control' + (errors.paymentLink && touched.paymentLink ? ' is-invalid' : '')} />
            <ErrorMessage name="tradition7Details" component="div" className="invalid-feedback" />
          </div>
          {formType !== 'ONL' &&
            <div className="form-group">
              <label htmlFor="whatThreeWords">What3Words(<a target="_blank" href="https://what3words.com/">Click here</a>)</label>
              <Field placeholder="what3words from what3words.com" name="whatThreeWords" type="text" className={'form-control' + (errors.whatThreeWords && touched.whatThreeWords ? ' is-invalid' : '')} />
              <ErrorMessage name="whatThreeWords" component="div" className="invalid-feedback" />
            </div>}
          <div className="form-group">
            <label htmlFor="email">Email* (A valid email address is required to successfully list your meeting - used for admin purposes only)</label>
            <Field placeholder="Email Address" name="email" type="text" className={'form-control placeholder:text-[10px]' + (errors.email && touched.email ? ' is-invalid' : '')} />
            <ErrorMessage name="email" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <Field placeholder="These will be published on you meeting page" name="description" component="textarea" type="text" className={'form-control' + (errors.description && touched.description ? ' is-invalid' : '')} />
            <ErrorMessage name="description" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group">
            <label htmlFor="notes">Notes & Temporary Changes (e.g. Christmas closure dates, venue change, etc)</label>
            <Field placeholder="These will be published on your meeting page" name="notes" component="textarea" type="text" className={'form-control' + (errors.notes && touched.notes ? ' is-invalid' : '')} />
            <ErrorMessage name="notes" component="div" className="invalid-feedback" />
          </div>
          <div className="form-group gso-opt-out">
            <label htmlFor="gsoOptOut">By submitting this form your group agrees to have the listing information shared with the General Service Office (GSO) and the meeting details updated there. Tick to opt out</label>
            <SemanticField
              name="gsoOptOut"
              component={Checkbox}
            />
          </div>
          

          <div className="auto-grid" role="group" aria-labelledby="checkbox-group">
            {formType !== 'ONL' &&
              <>
                <div><span className="checkbox-title" htmlFor="open">Open</span>
                  <SemanticField
                    name="open"
                    component={Checkbox}
                  />
                </div>
                <div><span className="checkbox-title" htmlFor="wheelchair">Wheelchair accessible</span>
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

                </div></>}
            <div>
              <span className="checkbox-title" htmlFor="signed">Sign Language interpreted</span>
              <SemanticField
                name="signed"
                component={Checkbox}
              />

            </div>
            <div>
            <span className="checkbox-title" htmlFor="hearingLoop">Hearing Loop</span>
                  <SemanticField
                    name="hearingLoop"
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
            {formType !== 'ONL' &&
              <><div>
                <span className="checkbox-title" htmlFor="childFriendly">Child Friendly</span>
                <SemanticField
                  name="childFriendly"
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
                </>}
          </div>



        </>}
    </React.Fragment>
  );
}
