import React from 'react';


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
    this.handleCovidChange = this.handleCovidChange.bind(this);
    this.handleClearFilters = this.handleClearFilters.bind(this);
    this.handleMeetingTypeChange = this.handleMeetingTypeChange.bind(this);
    

    this.state = {search:props.search}

  }

  handleSliderChange(e) {
    
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
   

   let lastSearchLength = this.state.search.length;
    let currentSearchLength = e.target.value.length;
    
    this.setState({ search: e.target.value });
    if (e.target.value.length > 2 || (lastSearchLength - currentSearchLength === lastSearchLength && currentSearchLength === 0) ){
      this.props.onSearchChange(e.target.value);
    }

    

 }

  handleSearchKeyDown(e){
    
    if (e.keyCode === ENTER_KEY) {
     
      this.props.onSearchEnter(e.target.value);
  } }

  handleTimeChange(eventKey,e) {
   
    this.props.onTimeChange(e.value);
  } 

  handleAccessChange(eventKey,e) {
  
    this.props.onAccessChange(e.value);
  } 
  handleCovidChange(eventKey,e) {
  
    this.props.onCovidChange(e.value);
  } 

  handleClearFilters() {
    
    this.props.onClearFilters();
  } 

  handleMeetingTypeChange(eventKey,e){
   this.props.onMeetingTypeChange(e.value);
  }
  render() {

    let igs = {
      117: "City Of London", 36: "East London", 123: "Chelsea", 124: "Chelsea & Fulham", 118: "London North East", 51: "London North", 64: "London North Middlesex",
      63: "London North West", 62: "London South Middlesex", 119: "London West End", 120: "London Westway", 75: "London Croydon Epsom & Sutton", 55: "London North Kent",
      122: "London South East (East)", 121: "London South East (West)", 77: "London South", 42: "London South West"
    };
    
    let search = this.state.search;
    let timeBand = this.props.timeBand;
    let access = this.props.access;
    let day = this.props.day;
    let covid = this.props.covid;
    let meetingType = this.props.meetingType;
    
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
      key: 'all',
      text: 'Anytime',
      value: 'all',
      
    },{
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
        key: 'all',
        text: 'Any day',
        value: 'all',
        
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
    const covids = [
    {
      key: 'active',
      text: 'Active',
      value: 'active',
      
    },
    {
      key: 'inactive',
      text: 'Inactive',
      value: 'inactive',
      
    }]
    const meetingTypes = [
      {
        key: 'online',
        text: 'Online',
        value: 'online',
        
      },
      {
        key: 'faceToFace',
        text: 'Face to Face',
        value: 'faceToFace',
        
      }]
      let zoomImg='/static/images/zoom.png';
      let  physicalImg = '/static/images/zoomAA-location-pin.png'
      


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
    <Dropdown
            placeholder='Covid status'
           // fluid
            selection
            options={covids}
           icon='dropdown'
           onChange={this.handleCovidChange}
           value = {covid}
           scrolling={false}
  />
    <Dropdown
            placeholder='Meeting Type'
           // fluid
            selection
            options={meetingTypes}
           icon='dropdown'
           onChange={this.handleMeetingTypeChange}
           value = {meetingType}
           scrolling={false}
  />
    
  <div><a className="clear-filters" onClick={this.handleClearFilters}>Clear Filters</a></div>
  <div className='meeting-key'><span><img src={zoomImg}></img></span><span> = Zoom</span></div>
  <div className='meeting-key'><img src={physicalImg}></img><span> = Face To Face</span></div>
  
       
      </div>
    );
  }
}



export default MeetingSearchForm;
