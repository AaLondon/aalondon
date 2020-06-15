import React from 'react';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Nav from 'react-bootstrap/Nav'
import RangeSlider from './RangeSlider'
import { Dropdown, Input } from 'semantic-ui-react'

const ENTER_KEY = 13;

class MeetingSearchForm extends React.Component {
  constructor(props) {
    super(props);


    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDayChange = this.handleDayChange.bind(this);
    this.handleIntergroupChange = this.handleIntergroupChange.bind(this);
    this.handleSliderChange = this.handleSliderChange.bind(this);
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.handleSearchKeyDown = this.handleSearchKeyDown.bind(this);

    this.state = {search:props.search}

  }

  handleSliderChange(e) {
    console.log("handleSliderChange");
    this.props.onSliderChange(e);

  }
  handleChange(e) {
    this.props.onInputChange(e.target.value);
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }
  handleDayChange(eventKey, e) {
      this.props.onDayChange(e.value);
  }
  handleIntergroupChange(eventKey, e) {
    this.props.onIntergroupChange(e.target.innerText);
  }
  
  handleSearchChange(e) {
    console.log(e);
    this.setState({ search: e.target.value });
 }

  handleSearchKeyDown(e){
    if (e.keyCode === ENTER_KEY) {
      console.log('SEARCH DATA A: '+ e.target.value);
      console.log(e.target.value);
      console.log(this.props);
      this.props.onSearchEnter(e.target.value);
  }
    
   
    
    
  }

  render() {

    let igs = {
      117: "City Of London", 36: "East London", 123: "Chelsea", 124: "Chelsea & Fulham", 118: "London North East", 51: "London North", 64: "London North Middlesex",
      63: "London North West", 62: "London South Middlesex", 119: "London West End", 120: "London Westway", 75: "London Croydon Epsom & Sutton", 55: "London North Kent",
      122: "London South East (East)", 121: "London South East (West)", 77: "London South", 42: "London South West"
    };
    let day = null;
    if (this.props.day !== null){
      console.log('ZZZZZ{}'+this.props.day)
      day = this.props.day;
    } 
    let search = this.state.search;

    const weekDays = ["Now", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    const dayOptions = [
      {
        key: 'Now',
        text: 'Now',
        value: 'Now',
        
      },
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

    let activeIndex = weekDays.findIndex(element => element.includes(day));


    let weekDayNav = weekDays.map((value, index) =>
      <Nav.Item key={index}>
        <Nav.Link onSelect={this.handleDayChange} eventKey={index}>{value}</Nav.Link>
      </Nav.Item>
    )

    return (

      <div >
        <Row className="justify-content-center">
        <Input icon='search' placeholder='Search...' onChange={this.handleSearchChange} onKeyDown={this.handleSearchKeyDown} value={search}/>
          </Row>
        <Row>
          <Col>
          <Dropdown
            placeholder='Day'
           // fluid
            selection
            options={dayOptions}
           icon='dropdown'
           onChange={this.handleDayChange}
           value = {day}
           scrolling={false}
  />
          </Col>
        </Row>
       
      </div>
    );
  }
}



export default MeetingSearchForm;
