import React from 'react';
import PropTypes from 'prop-types';







const Meeting = props => {
  const { code=null,title = null, time = null ,day = null } = props.meeting || {};
  
  return (
    <tr>
    <td><a href="https://aa-edinburgh.org.uk/meetings/holy-corner-2/">{props.title}
              </a></td>
  
    <td>{props.day}</td>
    <td >{props.time}</td>

  </tr>
  )
}

Meeting.propTypes = {
    title: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired
  };

export default Meeting;