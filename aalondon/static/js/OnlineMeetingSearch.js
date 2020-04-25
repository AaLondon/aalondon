import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import axios from 'axios';
import OnlineMeetingSearchForm from './components/OnlineMeetingSearchForm';
import OnlineMeetingTableData from './components/OnlineMeetingDataTable';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Spinner from 'react-bootstrap/Spinner'


class OnlineMeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onPageChanged = this.onPageChanged.bind(this);
    this.onDayChange = this.onDayChange.bind(this);
    



    this.state = {
      totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, day: "Now", showSpinner: 1, intergroup: '',
      clientLng: null, clientLat: null, showPostcode: 0,minMiles: 0, maxMiles: 1000000, geoFail : 0
    };
  }



  getPosition() {
    // Simple wrapper
    return new Promise((res, rej) => {
      navigator.geolocation.getCurrentPosition(res, rej);
    });
  }


  componentDidMount() {
    console.log('window.topRecords'+window.topRecords);
    let top = window.topRecords || 0;
    let day = new Date().toLocaleString('en-us', { weekday: 'long' });

    let queryString = "";
    queryString = `/api/onlinemeetingsearch/?day=${day}&now=1&top=${top}`
    this.setState({ showPostcode: 1 })

    axios.get(queryString)

      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
     


        this.setState({
          totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1,
          totalPages: totalPages, showSpinner: 0, currentPage: 1, top: top
        });
      


      });







  }

  getQueryString() {
    let intergroup = this.state.intergroup;
    let day = this.state.day;
    let top = this.state.top;


    return `/api/onlinemeetingsearch/?intergroup=${intergroup}&day=${day}&top=${top}`;
  }


  onPageChanged = data => {



    const { currentPage, totalPages, } = data;
    const day = this.state.day;
    const intergroup = this.state.intergroup;
    let top = this.state.top;
    let querystring = `/api/onlinemeetingsearch?page=${currentPage}&day=${day}&top=${top}`;


    axios.get(querystring)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages });
      });
  }

  handleInputChange = data => {

    axios.get(`/api/onlinemeetingsearch?ordering=day&search=${data}`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages, value: data });
      });



  }

 
  onDayChange = data => {

  
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
  
    this.setState({  showSpinner: 1 });

    let queryString = `/api/onlinemeetingsearch/?day=${query_day}&now=${now}`;
    if (this.state.clientLat) {
      queryString = `/api/onlinemeetingsearch/?day=${query_day}&now=${now}&clientLat=${this.state.clientLat}&clientLng=${this.state.clientLng}`;
      this.setState({ showPostcode: 0 })
    }
    console.log("DayChange:"+queryString);
    axios.get(queryString)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;



        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages, showSpinner: 0,day: data });
      });


  }




  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages, day, showSpinner,top } = this.state;
    let geoFail = this.state.geoFail;
    let geoFailRow = <Row className="justify-content-center"></Row>;

    if (geoFail === 1){
      geoFailRow = <Row className="justify-content-center">We have been unable to retrieve your location. Please check your browser settings.</Row>

    }

    let dayForm = <OnlineMeetingSearchForm value={this.state.day} onInputChange={this.handleInputChange}  onDayChange={this.onDayChange}  day={this.state.day}  /> ;
    console.log('top:'+top);
    if (top !== 0){
      dayForm = null;
    }
    if (showSpinner === 1)
      return (
        <div>
        <OnlineMeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} day={this.state.day}  />
        <Row className="justify-content-center"><Col xs={2}> <Spinner size="lg" animation="border" role="status">
          <span className="sr-only">Loading...</span>
        </Spinner></Col></Row>
        </div>

      )


    
    if (totalMeetings === 0) return (

      <div>

       
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
           {dayForm}      
          <div>NO MEETINGS FOR THE REST OF THE DAY PLEASE CHECK TOMORROW</div>


       

      </div>

    );


   
    let firstCode = currentMeetings[0].code +currentMeetings[0].distance_from_client  ;
    


    return (

      <div>

        
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          
          {dayForm} 
          <OnlineMeetingTableData showPostcode={this.state.showPostcode} key={firstCode} currentMeetings={currentMeetings}  />
          
        

      </div>








    );

  }

}


ReactDOM.render(<OnlineMeetingSearch />, window.react_mount);
