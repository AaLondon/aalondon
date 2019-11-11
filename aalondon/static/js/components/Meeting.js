import React from 'react';
import PropTypes from 'prop-types';







const Meeting = props => {
  const { code=null,title = null, time = null ,day = null,slug = null } = props.meeting || {};
  
  return (
    <tr>
    <td><a href={'/meetings/'+props.slug}>{props.title}
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