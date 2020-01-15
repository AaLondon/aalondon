import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Nav from 'react-bootstrap/Nav'

class MeetingSearchForm extends React.Component {
  constructor(props) {
    super(props);


    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDayChange = this.handleDayChange.bind(this);
    this.handleIntergroupChange = this.handleIntergroupChange.bind(this);
    
  }


  handleChange(e) {
    this.props.onInputChange(e.target.value);
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }
  handleDayChange(eventKey,e) {
    this.props.onDayChange(e.target.innerText);
  }
  handleIntergroupChange(eventKey,e) {
    this.props.onIntergroupChange(e.target.innerText);
  }
  render() {
   let igs = {117:"City Of London",36:"East London",123:"Chelsea",124:"Chelsea & Fulham",118:"London North East",51:"London North",64:"London North Middlesex",
        63:"London North West",62:"London South Middlesex",119:"London West End",120:"London Westway",75:"London Croydon Epsom & Sutton",55:"London North Kent",
        122:"London South East (East)",121:"London South East (West)",77:"London South",42:"London South West"} ;
    let day = this.props.day;
    console.log('day');
    console.log(day);
      
    return (
      
      <form onSubmit={this.handleSubmit}>
        <Row><Nav variant="pills" defaultActiveKey="/home">
  <Nav.Item>
    <Nav.Link eventKey="link-1">Active</Nav.Link>
  </Nav.Item>
  <Nav.Item>
    <Nav.Link eventKey="link-2">Option 2</Nav.Link>
  </Nav.Item>

</Nav></Row>
        <Row>  
         <Col>
        <Dropdown focusFirstItemOnShow={true}>
          <Dropdown.Toggle variant="success" id="dropdown-basic">
            {this.props.day ? this.props.day : "All days"}
        </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item onSelect={this.handleDayChange}>All days</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Monday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Tuesday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Wednesday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Thursday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Friday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Saturday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Sunday</Dropdown.Item>


          </Dropdown.Menu>
        </Dropdown>
        </Col> 
        <Col>
        <Dropdown focusFirstItemOnShow={true}>
          <Dropdown.Toggle variant="success" id="dropdown-basic">
          {this.props.intergroup ? this.props.intergroup : "All Intergroups"}
        </Dropdown.Toggle>

          <Dropdown.Menu>
          <Dropdown.Item key={0} onSelect={this.handleIntergroupChange}>{'All Intergroups'}</Dropdown.Item>
          {Object.keys(igs).map((key, index) => ( 
          <Dropdown.Item key={key} onSelect={this.handleIntergroupChange}>{igs[key]}</Dropdown.Item>
         
        ))}





           
           
          

          </Dropdown.Menu>
        </Dropdown>
        </Col> 
        </Row>  
      </form>
    );
  }
}



export default MeetingSearchForm;