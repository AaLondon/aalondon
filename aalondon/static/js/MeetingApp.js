import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import Pagination from './components/Pagination';
import Meeting from './components/Meeting';
import axios from 'axios';

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
        const totalPages = 5;
        console.log(response);
        this.setState({ totalMeetings: totalMeetings, currentMeetings: currentMeetings, currentPage: 1, totalPages: totalPages });
      });
  }

  onPageChanged = data => {
    const { currentPage, totalPages, } = data;
    console.log("this.componentDidMount");
    console.log("xxx");
    console.log(data);
    console.log(currentPage);
    console.log(totalPages);
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



      <div className="table-responsive">
        <table className="table table-sm table-striped">
      

          <tbody>
            <tr><td><Pagination totalRecords={totalMeetings} pageLimit={18} pageNeighbours={1} onPageChanged={this.onPageChanged} /></td>
              <td className="text-right"><strong>{totalMeetings}</strong> Meetings</td>
              </tr>
            {currentMeetings.map(meeting => <Meeting key={meeting.code} title={meeting.title} time={meeting.time} code={meeting.code} day={meeting.day} />)}
          </tbody>
        </table>


      </div>








    );

  }

}


ReactDOM.render(<MeetingApp />, window.react_mount);