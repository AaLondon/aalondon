import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import Pagination from './components/Pagination';
import Meeting from './components/Meeting';
import axios from 'axios';
<link
  rel="stylesheet"
  href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
  integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
  crossorigin="anonymous"
/>
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'



class MeetingApp extends Component {

  state = { totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null }

  componentDidMount() {
    const currentPage = 1;
    console.log("this.componentDidMount MeetingApp");

    //this.setState({ allMeetings, currentPage });
    axios.get(`/api/meetings2?twentyfour=1&page=${currentPage}`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count /10 ;
        console.log(response);
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages });
      });
  }

  onPageChanged = data => {
    const { currentPage, totalPages, } = data;
    console.log("this.OnPageChanged");
    axios.get(`/api/meetings2?twentyfour=1&page=${currentPage}`)
      .then(response => {
        const currentMeetings = response.data.results;
        this.setState({ currentPage, currentMeetings, totalPages });
      });
  }

  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages } = this.state;
    console.log(totalMeetings);
    console.log('currentMeetings');
    console.log(currentMeetings);
    console.log('currentPage');
    console.log(currentPage);
    console.log('totalMeetings');
    console.log(totalMeetings);
    if (totalMeetings === 0) return null;

    const headerClass = ['text-dark py-2 pr-4 m-0', currentPage ? 'border-gray border-right' : ''].join(' ').trim();

    return (



      <div className="container-responsive">
    <Container>
  {/* Stack the columns on mobile by making one full-width and the other half-width */}
  <Row>
    <Col xs={12} md={8}>
    <Pagination totalRecords={totalMeetings} pageLimit={10} pageNeighbours={1} onPageChanged={this.onPageChanged} />
    </Col>
    <Col xs={12} md={12}>
      {'Meetings : '+totalMeetings}
    </Col>
  </Row>

  {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
  {currentMeetings.map(meeting => <Meeting key={meeting.code} title={meeting.title} time={meeting.time} code={meeting.code} day={meeting.day} />)}
       
  {/* Columns are always 50% wide, on mobile and desktop */}
  
</Container>
       
           
       
       
       


      </div>








    );

  }

}


ReactDOM.render(<MeetingApp />, window.react_mount);