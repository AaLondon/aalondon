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
import Table from 'react-bootstrap/Table';
import MeetingTableData from './components/MeetingDataTable';
import Spinner from 'react-bootstrap/Spinner'


class MeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onPageChanged = this.onPageChanged.bind(this);
    this.onDayChange = this.onDayChange.bind(this);
 


    this.state = { totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, day: "Now",showSpinner: 1, intergroup: '', 
    clientLng: null, clientLat: null
     };
  }

  

  getPosition() {
    // Simple wrapper
    return new Promise((res, rej) => {
        navigator.geolocation.getCurrentPosition(res, rej);
    });
  }


  componentDidMount() {
    
    let day = new Date().toLocaleString('en-us', { weekday: 'long' });
    
    let queryString = 
    this.getPosition().then((position) => {
      // successMessage is whatever we passed in the resolve(...) function above.
      // It doesn't have to be a string, but if it is only a succeed message, it probably will be.
      //
      let lat = position.coords['latitude']
      let lng = position.coords['latitude']
      return `/api/meetingsearch/?day=${day}&now=1&clientLat=${lat}&clientLng=${lng}` 
      
    });

    
    console.log('xxx');
    console.log(queryString);
    console.log('xxx');
    
    this.setState({ currentPage: 1});

   console.log(queryString);
    axios.get(queryString)

      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;

        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages,showSpinner: 0  });
      });
    }
  
  getQueryString() {
    let intergroup = this.state.intergroup;
    let day = this.state.day;


    return `/api/meetingsearch/?intergroup=${intergroup}&day=${day}`;
  }


  onPageChanged = data => {
   // console.log('onPageChanged');


    const { currentPage, totalPages, } = data;
    const day = this.state.day;
    const intergroup = this.state.intergroup;
    let querystring = `/api/meetingsearch?page=${currentPage}&day=${day}`


    axios.get(querystring)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages });
      });
  }

  handleInputChange = data => {

    axios.get(`/api/meetingsearch?ordering=day&search=${data}`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages, value: data });
      });



  }

  onDayChange = data => {
    
    console.log('onDayCHange');
    console.log(data);
    let intergroup = this.state.intergroup;
    let query_day = data;
    if (data === 'All days') {
      query_day = '';
    } else {
      query_day = data
    }
    let currentPage = 1;
    let now = 0;
    if (data == 'Now') {
      query_day = new Date().toLocaleString('en-us', { weekday: 'long' });
      now = 1;
    }

    this.setState({ day: data,showSpinner: 1 });
    
    let queryString = `/api/meetingsearch/?intergroup=${intergroup}&day=${query_day}&now=${now}&clientLat=${this.state.clientLat}&clientLng=${this.state.clientLng}`;

    axios.get(queryString)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
      
        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages ,showSpinner: 0});
      });


  }




  render() {
  
    const { totalMeetings, currentMeetings, currentPage, totalPages, day,showSpinner } = this.state;
  
    console.log('render');
    console.log(day);
    if (showSpinner === 1 )
     return( <Container>
     <MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup} />
        <Row className="justify-content-center"><Col xs={2}> <Spinner size="lg" animation="border" role="status">
            <span className="sr-only">Loading...</span>
        </Spinner></Col></Row> 
     

    </Container>)
    
    
    
    if (totalMeetings === 0) return (

      <div>

        <Container>
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          <MeetingSearchForm value={day} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup} />
          <div>NO MEETINGS FOR THE REST OF THE DAY PLEASE CHECK TOMORROW</div>
         

        </Container>

      </div>

    );



    let firstCode = currentMeetings[0].code;


    return (

      <div>

        <Container>
       
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          <MeetingSearchForm value={this.state.day} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup} />
          <MeetingTableData key={firstCode} currentMeetings={this.state.currentMeetings} clientLat={this.state.clientLat} />

        </Container>

      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);