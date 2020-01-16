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

  state = { totalMeetings: 0, currentMeetings: [], currentPage: 1, totalPages: null, currenyDay: null }

  componentDidMount() {
    const currentPage = 1;
    

    //this.setState({ allMeetings, currentPage });
    axios.get(`/api/meetings2?twentyfour=1&page=${currentPage}`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;

        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages });
      });
  }

  onPageChanged = data => {
    const { currentPage, totalPages, } = data;

    axios.get(`/api/meetings2?twentyfour=1&page=${currentPage}`)
      .then(response => {
        const currentMeetings = response.data.results;
        this.setState({ currentPage, currentMeetings, totalPages });
      });
  }

  render() {

    const { totalMeetings, currentMeetings, currentPage, totalPages } = this.state;

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
              {'Meetings : ' + totalMeetings}
            </Col>
          </Row>
          {currentMeetings.map((meeting, i) => {
            // Return the element. Also pass key
            console.log(meeting.day_rank);
            if (meeting.day_rank === 1 || i === 0) {
              return (<Row><Col><Row><Col>{meeting.day}</Col></Row><Row><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row></Col></Row>)
            }else {
              return (<Row><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row>)
            }
          })}
          {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
          

          {/* Columns are always 50% wide, on mobile and desktop */}

        </Container>







      </div>








    );

  }

}


ReactDOM.render(<MeetingApp />, window.react_mount);