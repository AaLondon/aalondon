import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import axios from 'axios';
import MeetingSearchForm from './components/MeetingSearchForm';

import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import MeetingTableData from './components/MeetingDataTable';
import Spinner from 'react-bootstrap/Spinner'
import includes from 'lodash/includes'
import cloneDeep from 'lodash/cloneDeep'
import sortBy from 'lodash/sortBy'



class MeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onPageChanged = this.onPageChanged.bind(this);
    this.onDayChange = this.onDayChange.bind(this);
    this.onSliderChange = this.onSliderChange.bind(this);
    this.onSearchEnter = this.onSearchEnter.bind(this);
    this.onAccessChange = this.onAccessChange.bind(this);
    this.onCovidChange = this.onCovidChange.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onSearchChange = this.onSearchChange.bind(this);
    this.onMeetingTypeChange = this.onMeetingTypeChange.bind(this);


    this.state = {
      totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, day: 'all', showSpinner: 1, intergroup: '',
      clientLng: null, clientLat: null, showPostcode: 1, minMiles: 0, maxMiles: 1000000, geoFail: 0, search: '', 
      timeBand: 'all', access: '', covid: '', meetingType: ''
    };
  }



  getPosition() {
    // Simple wrapper
    return new Promise((res, rej) => {
      navigator.geolocation.getCurrentPosition(res, rej);
    });
  }



  getResults(day, search, timeBand, access, isSearchChange, covid, meetingType) {

    let timeBandSend = timeBand === 'all' ? '' : timeBand
    let daySend = day === 'all' ? '' : day
    let meetingTypeSend = meetingType === 'all' ? '' : meetingType

    let queryString = `/api/meetingsearch/?search=${search}&day=${daySend}&time_band=${timeBandSend}`;
    if (access === 'wheelchair') {
      queryString += '&wheelchair=1'

    } else if (access === 'hearing') {
      queryString += '&hearing=1'
    }

    if (covid == 'active') {
      queryString += '&covid_open_status=true'
    } else if (covid == 'inactive') {
      queryString += '&covid_open_status=false'
    }

    let currentPage = 1
    var strr = [];
    let onlineQueryString = `/api/onlinemeetingsearch/?search=${search}&day=${daySend}&time_band=${timeBandSend}`

    const onlineMeetingRequest = axios.get(onlineQueryString);
    const physicalMeetingRequest = axios.get(queryString);
    console.log(onlineQueryString)
    console.log(queryString)


    axios.all([onlineMeetingRequest, physicalMeetingRequest]).then(axios.spread((...responses) => {
   
      let onlineMeetings = responses[0].data.results;
      let physicalMeetings = responses[1].data.results;
      let currentMeetings = [];
      
    
      
      //get online meetings that are ""all""
      let onlineMeetingsAll = onlineMeetings.filter(v => includes(['All'], v.day));
      let onlineMeetingsExcludesAll = onlineMeetings.filter(v => !includes(['All'], v.day));
      //iterate over the all onlineMeetingsall 
      for (var value of onlineMeetingsAll) {
        let currentCode = value['code'];
        if (day === 'all') {
          for (const [i, dayName] of ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].entries()) {
            var newMeeting = cloneDeep(value);
            newMeeting['day'] = dayName;
            newMeeting['code'] = currentCode + '_' + dayName;
            newMeeting['day_number'] = i;
            onlineMeetingsExcludesAll.push(newMeeting);
          }
        } else {
          let weekDays = { "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6 }
          var newMeeting = cloneDeep(value);
          newMeeting['day'] = day;
          newMeeting['code'] = currentCode + '_' + day;
          newMeeting['day_number'] = weekDays[day];
          onlineMeetingsExcludesAll.push(newMeeting);
        }
      }

    
      if (meetingType === 'faceToFace'){
        currentMeetings = physicalMeetings
        
      } else if (meetingType === 'online')
      {
        currentMeetings = onlineMeetingsExcludesAll
        
      }else{
        currentMeetings = physicalMeetings.concat(onlineMeetingsExcludesAll);
      }

      
      currentMeetings = sortBy(currentMeetings, ['day_number', 'time', 'title']);
     
      const totalMeetings = currentMeetings.length;
      const totalPages = currentMeetings.length / 10;

      if ((isSearchChange === 1 && currentMeetings.length > 0) || isSearchChange === 0) {

        

        this.setState({ totalMeetings, currentMeetings, currentPage, totalPages, showSpinner: 0, day: day, search: search, 
          meetingType: meetingType });
      }

      
    }))




  }

  componentDidMount() {


    //let day = new Date().toLocaleString('en-us', { weekday: 'long' });

    //this.setState({ showPostcode: 1 })
    //day, search, timeBand, access, isSearchChange, covid
    this.getResults(this.state.day, this.state.search, this.state.timeBand, this.state.access, 0, this.state.covid);



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
    let now = 0;

    if (day === "Now") {

      day = new Date().toLocaleString('en-us', { weekday: 'long' });
      now = 1;
    }

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

      if (lat === null) {
        showPostcode = 1;
      }

      axios.get(queryString)

        .then(response => {
          const totalMeetings = response.data.count;
          const currentMeetings = response.data.results;
          const totalPages = response.data.count / 10;

          this.setState({
            totalMeetings: totalMeetings, currentMeetings: currentMeetings,
            totalPages: totalPages, showSpinner: 0, currentPage: 1, clientLat: lat, clientLng: lng, 
            showPostcode: showPostcode, minMiles: minMiles, maxMiles: maxMiles, geoFail: geoFail
          });

        });
    });



  }
  onDayChange = data => {

    this.setState({ showSpinner: 1, day: data });
    this.getResults(data, this.state.search, this.state.timeBand, this.state.access, 0, this.state.covid, this.state.meetingType);

  }

  onSearchEnter = data => {




    this.setState({ showSpinner: 1, search: data });

    this.getResults(this.state.day, data, this.state.timeBand, this.state.access, 0, this.state.meetingType);

  }
  onSearchChange = data => {




    this.setState({ showSpinner: 0, search: data });

    this.getResults(this.state.day, data, this.state.timeBand, this.state.access, 1, this.state.meetingType, this.state.meetingType);

  }
  onTimeChange = data => {

    this.setState({ showSpinner: 1, timeBand: data });
    this.getResults(this.state.day, this.state.search, data, this.state.access, 0, this.state.covid, this.state.meetingType);

  }

  onAccessChange = data => {

    this.setState({ showSpinner: 1, access: data });
    this.getResults(this.state.day, this.state.search, this.state.timeBand, data, 0, this.state.covid, this.state.meetingType);

  }
  onCovidChange = data => {

    this.setState({ showSpinner: 1, covid: data });
    this.getResults(this.state.day, this.state.search, this.state.timeBand, this.state.access, 0, data, this.state.meetingType );

  }

  onClearFilters = () => {
    this.setState({ showSpinner: 1, day: 'all', search: '', timeBand: 'all', access: '', coivid: 'all' })
    this.getResults('all', '', 'all', '', 0, 'all');
  }

  onMeetingTypeChange = data => {

    this.setState({ showSpinner: 1, meetingType: data });
    this.getResults(this.state.day, this.state.search, this.state.timeBand, this.state.access, 0, this.state.covid ,data);

  }


  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages, day, showSpinner } = this.state;
    let geoFail = this.state.geoFail;
    let geoFailRow = <Row className="justify-content-center"></Row>;

    if (geoFail === 1) {
      geoFailRow = <Row className="justify-content-center">We have been unable to retrieve your location. Please check your browser settings.</Row>

    }

    let slider = <MeetingSearchForm value={this.state.day}
      onInputChange={this.handleInputChange} onSliderChange={this.onSliderChange}
      onDayChange={this.onDayChange} onSearchEnter={this.onSearchEnter} onSearchChange={this.onSearchChange}
      onTimeChange={this.onTimeChange}
      onAccessChange={this.onAccessChange}
      onCovidChange={this.onCovidChange}
      onClearFilters={this.onClearFilters}
      onMeetingTypeChange={this.onMeetingTypeChange}
      onIntergroupChange={this.onIntergroupChange}
      day={this.state.day} intergroup={this.state.intergroup} search={this.state.search} access={this.state.access}
      timeBand={this.state.timeBand} covid={this.state.covid} meetingType={this.state.meetingType}
    />;
    if (showSpinner === 1)
      return (<Container>
        <MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange}
          onDayChange={this.onDayChange} onSearchEnter={this.onSearchEnter} onSearchChange={this.onSearchChange}
          onTimeChange={this.onTimeChange}
          onSliderChange={this.onSliderChange}
          onAccessChange={this.onAccessChange}
          onCovidChange={this.onCovidChange}
          onClearFilters={this.onClearFilters}
          onMeetingTypeChange={this.onMeetingTypeChange}
          onIntergroupChange={this.onIntergroupChange} day={this.state.day} intergroup={this.state.intergroup}
          search={this.state.search} timeBand={this.state.timeBand} access={this.state.access} covid={this.state.covid} 
          meetingType={this.state.meetingType}/>
        <Row className="justify-content-center"><Col xs={2}> <Spinner size="lg" animation="border" role="status">
          <span className="sr-only">Loading...</span>
        </Spinner></Col></Row>
      </Container>)
    if (totalMeetings === 0) return (

      <div>

        <Container>
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          {slider}
          <h2><b>Unfortunately no meetings found have matched your search criteria. Please clear filters and try again</b></h2>


        </Container>

      </div>

    );



    let firstCode = currentMeetings[0].code + currentMeetings.length;
    


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
