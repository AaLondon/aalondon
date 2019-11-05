import React from 'react';
import PropTypes from 'prop-types';







const Meeting = props => {
  const { code=null,title = null, time = null  } = props.meeting || {};
  
  return (
    <div className="col-sm-6 col-md-4 meeting-info">
      <div>
          {props.title}
      </div>
      <div>{props.time}</div>
    </div>
  )
}

Meeting.propTypes = {
    title: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired
  };

export default Meeting;