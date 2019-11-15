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



class MeetingSearch extends Component {
  constructor(props) {
    super(props);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.state = { totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, value: '' };
    //this.state = {temperature: '', scale: 'c'};
    console.log('constructor');
  }

 

  componentDidMount() {
    const currentPage = 1;
    console.log("this.componentDidMount MeetingApp");

    
    this.setState({ currentPage: currentPage });

    axios.get(`/api/meetingsearch?ordering=time`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages });
      });
      //console.log(this.state);
  }

  onPageChanged = data => {
    const { currentPage, totalPages, } = data;
    
    console.log(data);
    console.log(this.state);
   
    console.log(`/api/meetingsearch?ordering=time&day=Thursday&page=${currentPage}`)
    axios.get(`/api/meetingsearch?ordering=time&day=Thursday&page=${currentPage}`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        console.log('onPageChanged response');
        console.log(response);
        this.setState({ totalMeetings,currentMeetings,currentPage,totalPages });
      });
  }

  handleInputChange = data =>{

    axios.get(`/api/meetingsearch?ordering=time&day=Monday&search=${data}`)
    .then(response => {
      const totalMeetings = response.data.count;
      const currentMeetings = response.data.results;
      const totalPages = response.data.count / 10;
      console.log(response);
      this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages,value: data });
    });
    


  }
  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages } = this.state;

    if (totalMeetings === 0) return null;

  

    return (

      <div>
       
        <Container>
  {/* Stack the columns on mobile by making one full-width and the other half-width */}
  <Row><MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} /></Row>
  <Row>
    <Col xs={12} md={8}>
    <Pagination totalRecords={totalMeetings} pageLimit={10} pageNeighbours={1} onPageChanged={this.onPageChanged} />
    </Col>
    <Col xs={12} md={12}>
      {'Meetings : '+totalMeetings}
    </Col>
  </Row>

  {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
  {currentMeetings.map(meeting => <Meeting key={meeting.code} title={meeting.title} time={meeting.time} code={meeting.code} day={meeting.day} postcode={meeting.postcode} slug={meeting.slug} dayRank={meeting.day_rank} />)}
       
  {/* Columns are always 50% wide, on mobile and desktop */}
  
</Container>
       
      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);