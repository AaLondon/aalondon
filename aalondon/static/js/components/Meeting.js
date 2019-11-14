import React from 'react';
import PropTypes from 'prop-types';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'







const Meeting = props => {
  const { code=null,title = null, time = null ,day = null,slug = null } = props.meeting || {};
  
  return (
    <Row>
    <Col xs={4} md={4}><a href={'/meetings/'+props.slug}>{props.title}
              </a></Col>
  
    <Col xs={4} md={4} >{props.day}</Col>
    <Col>{props.time}</Col>

  </Row>
  )
}

Meeting.propTypes = {
    title: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired
  };

export default Meeting;