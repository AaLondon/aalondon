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
  }

 

  componentDidMount() {
    const currentPage = 1;
    
    this.setState({ currentPage: currentPage });

    axios.get(`/api/meetingsearch/?twentyfour=1`)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
        
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages, day : '' });
      });
  }

  onPageChanged = data => {
    const { currentPage, totalPages, } = data;
    const day = this.state.day;
    let querystring = `/api/meetingsearch?page=${currentPage}&day=${day}`
    

    
     
    axios.get(querystring)
      .then(response => {
        const totalMeetings = response.data.count;
        const currentMeetings = response.data.results;
        const totalPages = response.data.count / 10;
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
    const currentPage = 1;
    this.setState({day: data});
    
    let queryString;
    if (data === ''){
      queryString= `/api/meetingsearch?twentyfour=1`
    }
    else
    {
      queryString= `/api/meetingsearch?ordering=time&day=${data}`
    }
    

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

    if (totalMeetings === 0) return null;

  

    return (

      <div>
       
       <Container>
          {/* Stack the columns on mobile by making one full-width and the other half-width */}
          <Row><MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} onDayChange={this.onDayChange} day={this.state.day}/></Row>
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
            
            if (meeting.day_rank === 1 || i === 0) {
              return (<Row key={i} ><Col><Row><Col>{meeting.day}</Col></Row><Row><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row></Col></Row>)
            }else {
              return (<Row key={i}><Col><Meeting key={meeting.code} title={meeting.title} time={meeting.friendly_time} code={meeting.code} day={meeting.day} postcode={meeting.postcode_prefix} slug={meeting.slug} dayRank={meeting.day_rank} /></Col></Row>)
            }
          })}
          {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
          

          {/* Columns are always 50% wide, on mobile and desktop */}

        </Container>
       
      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);