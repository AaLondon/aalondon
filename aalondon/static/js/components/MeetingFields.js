import React, { useEffect, useState ,useRef} from 'react';
import { Field, ErrorMessage } from 'formik';
import SemanticField from './SemanticField'
import { Dropdown, TextArea, Checkbox } from 'semantic-ui-react'
import getCookie from './getCookie';




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

  const
  { errors, touched,activeStep, formType , setFormType,setThreeWords}
    = props;

  useEffect(() => {
    
    if (whatThreeRef && whatThreeRef.current){
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
  }}, [formType]);

   
  return (
    <React.Fragment>
      <label htmlFor="notes">Meeting Type(Hybrid,Online or Face to Face)</label>
      <Dropdown
        placeholder='Please choose meeting type'
        // fluid
        selection
        options={formTypes}
        icon='dropdown'
        onChange={(e, data) => {
      
          setFormType(data.value)
       

        }}
        scrolling={false}
      />
      { formType &&
      <>
      <div className="form-group">
        <label htmlFor="title">Title</label>
        <Field placeholder="Please supply your meeting name" name="title" type="text" className={'form-control' + (errors.title && touched.title ? ' is-invalid' : '')} />
        <ErrorMessage name="title" component="div" className="invalid-feedback" />
      </div>
      <div className="form-group">
        <label htmlFor="days">Days</label>
        <SemanticField
          name="days"
          component={Dropdown}
          options={dayOptions}
          multiple
          selection
          placeholder="Please select day of week"
          id={"days"}
          value={[]}
          className={'form-control' + (errors.day && touched.day ? ' is-invalid' : '')}

        />

        <ErrorMessage name="days" component="div" className="invalid-feedback" />
      </div>
      
      <div className="form-group">
        <label htmlFor="submission">Is this a new entry to AALondon, or an update to an existing entry?</label>
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
      {formType !== 'F2F' &&
        <><div className="form-group">
          <label htmlFor="link">Online Meeting Link</label>
          <Field placeholder="Please enter online meeting link. Zoom,Skype etc" name="link" type="text" className={'form-control' + (errors.link && touched.link ? ' is-invalid' : '')} />
          <ErrorMessage name="link" component="div" className="invalid-feedback" />
        </div>

          <div className="form-group">
            <label htmlFor="password">Online Meeting Password</label>
            <Field placeholder="Please enter password" name="password" type="text" className={'form-control' + (errors.password && touched.password ? ' is-invalid' : '')} />
            <ErrorMessage name="password" component="password" className="invalid-feedback" />
          </div></>}
      {formType !== 'ONL' &&
        <><div className="form-group">
          <label htmlFor="address">Address</label>
          <Field name="address" type="text" className={'form-control' + (errors.address && touched.address ? ' is-invalid' : '')} />
          <ErrorMessage name="address" component="div" className="invalid-feedback" />
        </div>
          <div className="form-group">
            <label htmlFor="postcode">Postcode</label>
            <Field name="postcode" type="text" className={'form-control' + (errors.postcode && touched.postcode ? ' is-invalid' : '')} />
            <ErrorMessage name="postcode" component="div" className="invalid-feedback" />
          </div></>}
      <div className="form-group">
        <label htmlFor="paymentLink">Payment Link</label>
        <Field placeholder="Paypal,Cashapp,Square... etc link" name="paymentLink" type="text" className={'form-control' + (errors.paymentLink && touched.paymentLink ? ' is-invalid' : '')} />
        <ErrorMessage name="paymentLink" component="div" className="invalid-feedback" />
      </div>
      {formType !== 'ONL' &&
        <div className="form-group">
          <label htmlFor="3wa">What Three Words(<a target="_blank" href="https://what3words.com/">Click here</a>)</label>
          <what3words-autosuggest ref={whatThreeRef}
            id="autosuggest"
            placeholder="What three words tells us precisely where you are. Click above for info." />
          <ErrorMessage name="3wa" component="div" className="invalid-feedback" />
        </div>}
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
        {formType !== 'ONL' &&
          <><div><span className="checkbox-title" htmlFor="wheelchair">Wheelchair accessible</span>
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
        {formType !== 'ONL' &&
          <><div>
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

            </div></>}
      </div>

   

      </>}
    </React.Fragment>
  );
}
