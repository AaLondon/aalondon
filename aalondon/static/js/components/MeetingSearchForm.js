import React from 'react';
import Nav from 'react-bootstrap/Nav'
import _ from 'lodash'

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
    this.handleTimeChange = this.handleTimeChange.bind(this);
    this.handleAccessChange = this.handleAccessChange.bind(this);
    this.handleClearFilters = this.handleClearFilters.bind(this);
    

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
     
      this.props.onSearchEnter(e.target.value);
  } }

  handleTimeChange(eventKey,e) {
    console.log(e);
    this.props.onTimeChange(e.value);
  } 

  handleAccessChange(eventKey,e) {
    console.log(e);
    this.props.onAccessChange(e.value);
  } 
  handleClearFilters() {
    
    this.props.onClearFilters();
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
    let timeBand = this.props.timeBand;
    let access = this.props.access;
    const weekDays = ["Now", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    const accesses = [{
      key: 'wheelchair',
      text: 'Wheelchair',
      value: 'wheelchair',
      
    },
    {
      key: 'hearing',
      text: 'Hearing',
      value: 'hearing',
      
    }]
    const timeBands = [{
      key: 'morning',
      text: 'Morning',
      value: 'morning',
      
    },
    {
      key: 'afternoon',
      text: 'Afternoon',
      value: 'afternoon',
      
    },
    {
      key: 'evening',
      text: 'Evening',
      value: 'evening',
      
    },]
    const dayOptions = [
      {
        key: 'now',
        text: 'Now',
        value: 'now',
        
      },
      {
        key: 'All',
        text: 'All',
        value: 'All',
        
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




    return (

      <div className={'meeting-search-form'}>
        <Input icon='search' placeholder='Search...' onChange={this.handleSearchChange} onKeyDown={this.handleSearchKeyDown} value={search}/>
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
          <Dropdown
            placeholder='Time'
           // fluid
            selection
            options={timeBands}
           icon='dropdown'
           onChange={this.handleTimeChange}
           value = {timeBand}
           scrolling={false}
  />
          <Dropdown
            placeholder='Accessibility'
           // fluid
            selection
            options={accesses}
           icon='dropdown'
           onChange={this.handleAccessChange}
           value = {access}
           scrolling={false}
  />
  <a className="clear-filters" onClick={this.handleClearFilters}>Clear Filters</a>
       
      </div>
    );
  }
}



export default MeetingSearchForm;
