import React from 'react';
import PropTypes from 'prop-types';







const Meeting = props => {
  const { title = null, time = null  } = props.meeting || {};

  return (
    <div className="col-sm-6 col-md-4 meeting-info">
      <div>
          {title}
      </div>
      <div>{time}</div>
    </div>
  )
}

Meeting.propTypes = {
  meeting: PropTypes.shape({
    title: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired
  }).isRequired
};

export default Meeting;