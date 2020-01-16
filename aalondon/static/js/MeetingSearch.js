import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import Pagination from './components/Pagination';
import Meeting from './components/Meeting';
import axios from 'axios';
import MeetingSearchForm from './components/MeetingSearchForm';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import * as geolib from 'geolib';



class MeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onPageChanged = this.onPageChanged.bind(this);
    this.onDayChange = this.onDayChange.bind(this);
    this.onIntergroupChange = this.onIntergroupChange.bind(this);

    
    
    this.state = { totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, day: '',intergroup : '' };
  }

 

  componentDidMount() {

    /*  Geo play    */
    navigator.geolocation.getCurrentPosition(
      function(position) {
          console.log("position.coords");       
          console.log(position.coords);       
          let lngA = position.coords.longitude;
          let latA = position.coords.latitude;

          console.log(
              'You are ',
              geolib.getDistance({latitude:latA,longitude:lngA}, {
                  latitude: 51.525,
                  longitude: 7.4575,
              }),
              'meters away from 51.525, 7.4575'
          );
      },
      () => {
          alert('Position could not be determined.');
      }
  );
    const currentPage = 1;
    
    this.setState({ currentPage: currentPage });

    axios.get(`/api/meetingsearch/`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages});
      });
  }

  getQueryString()
  {
    let intergroup=this.state.intergroup;
    let day = this.state.day;

    
    return `/api/meetingsearch/?intergroup=${intergroup}&day=${day}`;
  }

 
  onPageChanged = data => {
    console.log('B'); 

    const { currentPage, totalPages, } = data;
    const day = this.state.day;
    const intergroup = this.state.intergroup;
    let querystring = `/api/meetingsearch?page=${currentPage}&day=${day}&intergroup=${intergroup}`
    
     
    axios.get(querystring)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        console.log('totalPages');
        console.log(totalPages);
        this.setState({ totalMeetings,currentMeetings,currentPage,totalPages });
      });
  }

  handleInputChange = data =>{

    axios.get(`/api/meetingsearch?ordering=day&search=${data}`)
    .then(response => {
      const totalMeetings = response.data.count;
      const currentMeetings = response.data.results;
      const totalPages = response.data.count / 10;
      console.log(response);
      this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages,value: data });
    });
    


  }

  onDayChange = data =>{
    let intergroup=this.state.intergroup;
    let day;
    if (data === 'All days'){
       day = '';
    }else
    {
      day = data
    }
    let currentPage = 1;
    console.log('onDayCHange');
    this.setState({day : day});
    let queryString = `/api/meetingsearch/?intergroup=${intergroup}&day=${day}`;
    axios.get(queryString)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings,currentMeetings,currentPage,totalPages });
      });
  }

  


  
  onIntergroupChange = data =>{
    let day = this.state.day;
    let intergroup;
    if (data === 'All Intergroups'){
      intergroup = '';
    }else
    {
      intergroup = data
    }
    let currentPage = this.state.currentPage;
    console.log('C');
    this.setState({intergroup : intergroup});

    let queryString = `/api/meetingsearch/?intergroup=${intergroup}&day=${day}`;
    console.log(queryString);
    axios.get(queryString)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings,currentMeetings,currentPage,totalPages });
      });
    
  }
  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages,day } = this.state;
    console.log('tmeets');
    console.log(totalMeetings);
    
    if (totalMeetings === 0) return null;

  

    return (

      <div>
       
       <Container>
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          <MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup} />
          
          {currentMeetings.map((meeting, i) => {
            // Return the element. Also pass key
            
          //  if (meeting.day_rank === 1 || i === 0) {
            //  return (<Row key={i} ><Col><Row><Col><h2>{meeting.day}</h2></Col></Row><Row><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row></Col></Row>)
            //}else {
              return (<Row key={i}><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row>)
            //}
          })}
          {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
          

          {/* Columns are always 50% wide, on mobile and desktop */}
          <Row>
              <Col xs={12} md={12}>
              <Pagination totalRecords={totalMeetings} pageLimit={10} pageNeighbours={1} onPageChanged={this.onPageChanged}  />
            </Col>
           
          </Row>
        </Container>
       
      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);