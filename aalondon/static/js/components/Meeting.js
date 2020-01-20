import React from 'react';
import PropTypes from 'prop-types';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'







const Meeting = props => {
  const { code = null, title = null, time = null, day = null, slug = null, distance = null, dayRank = null } = props.meeting || {};
  let weekdayRow;
  weekdayRow = <Row>{props.day}</Row>
  return (
   
    <tr className="meeting-row">
      <td xs={3} md={3}>{props.time}</td>
      <td xs={5} md={6}><a href={'/meetings/' + props.slug}>{props.title}</a></td>
      <td xs={3} md={3}>{props.distance}</td>
      
    </tr>
  )
}

Meeting.propTypes = {
  title: PropTypes.string.isRequired,
  time: PropTypes.string.isRequired
};

export default Meeting;