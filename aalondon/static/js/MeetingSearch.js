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
import _ from 'lodash'


class MeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onPageChanged = this.onPageChanged.bind(this);
    this.onDayChange = this.onDayChange.bind(this);
    this.onSliderChange = this.onSliderChange.bind(this);
    this.onSearchEnter = this.onSearchEnter.bind(this);
    this.onAccessChange = this.onAccessChange.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);



    this.state = {
      totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, day: 'all', showSpinner: 1, intergroup: '',
      clientLng: null, clientLat: null, showPostcode: 0,minMiles: 0, maxMiles: 1000000, geoFail : 0,search:'',timeBand: 'all',access:''
    };
  }



  getPosition() {
    // Simple wrapper
    return new Promise((res, rej) => {
      navigator.geolocation.getCurrentPosition(res, rej);
    });
  }

  getResults(day,search,timeBand,access){
    
    let timeBandSend = timeBand === 'all' ? '' :timeBand
    let daySend = day === 'all' ? '' :day
      
    let queryString = `/api/meetingsearch/?search=${search}&day=${daySend}&time_band=${timeBandSend}`;
    if (access === 'wheelchair'){
      queryString+='&wheelchair=1'
    }else if(access === 'hearing'){
      queryString+='&hearing=1'
    }

    let currentPage = 1
   
    axios.get(queryString)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = _.sortBy(response.data.results, ['day_number','time']);
        const totalPages = response.data.count / 10;



        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages, showSpinner: 0,day: day,search:search });
      });
  }

  componentDidMount() {

    //let day = new Date().toLocaleString('en-us', { weekday: 'long' });

    this.setState({ showPostcode: 1})
    this.getResults(this.state.day,this.state.search,this.state.timeBand,this.state.access);



  }

  getQueryString() {
    let intergroup = this.state.intergroup;
    let day = this.state.day;


    return `/api/meetingsearch/?intergroup=${intergroup}&day=${day}`;
  }

  onPageChanged = data => {



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

  onSliderChange = data => {

  
    let day = this.state.day;
    console.log("DAY: "+day);
    let now = 0;
    console.log("now0:"+ now);
    if (day === "Now")
    {
      console.log("Im her");
      day = new Date().toLocaleString('en-us', { weekday: 'long' });
      now = 1;
    }
    console.log("nowA:"+ now);
      
    let minMiles = 0;
    let maxMiles = data;
    let queryString = "";
    let lat = null;
    let lng = null;
    let showPostcode = 0;
    let geoFail = 0;
    this.getPosition().then((position) => {
      // successMessage is whatever we passed in the resolve(...) function above.
      // It doesn't have to be a string, but if it is only a succeed message, it probably will be.
      //

      lat = position.coords['latitude']
      lng = position.coords['longitude']
      //this.setState({clientLat:lat,clientLng:lng});
      queryString = `/api/meetingsearch/?day=${day}&now=${now}&clientLat=${lat}&clientLng=${lng}`
      geoFail = 0;
      return queryString

    }
      ,
      () => {
        //TODO WHEN GEO CANT BE FOUNG
   
        geoFail = 1;

        return `/api/meetingsearch/?day=${day}&now=${now}`

      }

    ).then((queryString) => {

      if(lat === null){
        showPostcode = 1;
      }
      console.log("nowB:"+ now);
      console.log("SliderChange:"+queryString);
      axios.get(queryString)

        .then(response => {
          const totalMeetings = response.data.count;
          const currentMeetings = response.data.results;
          const totalPages = response.data.count / 10;
 
          this.setState({
            totalMeetings: totalMeetings, currentMeetings: currentMeetings,
            totalPages: totalPages, showSpinner: 0, currentPage: 1, clientLat: lat, clientLng: lng, showPostcode : showPostcode ,minMiles:minMiles,maxMiles:maxMiles,geoFail : geoFail
          });

        });
    });



  }
  onDayChange = data => {

    this.setState({ showSpinner: 1, day: data });
    this.getResults(data,this.state.search,this.state.timeBand,this.state.access);

  }

onSearchEnter = data =>{
 
      
    console.log('data:'+data);
  
    this.setState({ showSpinner: 1, search: data });
    
    this.getResults(this.state.day,data,this.state.timeBand,this.state.access);
    
}

onTimeChange = data => {

  this.setState({ showSpinner: 1, timeBand: data });
  this.getResults(this.state.day,this.state.search,data,this.state.access);

}

onAccessChange = data => {

  this.setState({ showSpinner: 1, access: data });
  this.getResults(this.state.day,this.state.search,this.state.timeBand,data);

}
onClearFilters = () =>  {
  this.setState({showSpinner: 1,day: 'all', search:'',timeBand:'all', access:''})
  this.getResults('all','','all','');  
}

  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages, day, showSpinner } = this.state;
    let geoFail = this.state.geoFail;
    let geoFailRow = <Row className="justify-content-center"></Row>;

    if (geoFail === 1){
      geoFailRow = <Row className="justify-content-center">We have been unable to retrieve your location. Please check your browser settings.</Row>

    }
 
    let slider = <MeetingSearchForm value={this.state.day} 
    onInputChange={this.handleInputChange} onSliderChange={this.onSliderChange} 
    onDayChange={this.onDayChange} onSearchEnter={this.onSearchEnter}  onTimeChange={this.onTimeChange} onAccessChange={this.onAccessChange}
    onClearFilters={this.onClearFilters}
    onIntergroupChange={this.onIntergroupChange}  
    day={this.state.day} intergroup={this.state.intergroup} search={this.state.search} access={this.state.access}
    timeBand={this.state.timeBand}
    />;
    if (showSpinner === 1)
      return (<Container>
        <MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} 
        onDayChange={this.onDayChange} onSearchEnter={this.onSearchEnter} onTimeChange={this.onTimeChange} 
        onSliderChange={this.onSliderChange} onAccessChange={this.onAccessChange} onClearFilters={this.onClearFilters}
        onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup} 
        search={this.state.search} timeBand={this.state.timeBand} access={this.state.access} />
        <Row className="justify-content-center"><Col xs={2}> <Spinner size="lg" animation="border" role="status">
          <span className="sr-only">Loading...</span>
        </Spinner></Col></Row>
      </Container>)
    if (totalMeetings === 0) return (

      <div>

        <Container>
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          {slider}
          <div>NO MEETINGS FOR THE REST OF THE DAY PLEASE CHECK TOMORROW</div>


        </Container>

      </div>

    );


   
    let firstCode = currentMeetings[0].code +currentMeetings[0].distance_from_client  ;
    


    return (

      <div>

        <Container>

          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          {slider}
          {geoFailRow}
          <MeetingTableData showPostcode={this.state.showPostcode} key={firstCode} currentMeetings={currentMeetings} minMiles={this.state.minMiles} maxMiles={this.state.maxMiles} />
          
        </Container>

      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);
