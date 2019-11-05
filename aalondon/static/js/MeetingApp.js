import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import Pagination from './components/Pagination';
import Meeting from './components/Meeting';

class MeetingApp extends Component {

  state = { allMeetings: [], currentMeetings: [], currentPage: null, totalPages: null }

  componentDidMount() {
    const { data: allMeetings = [] } =[];
    this.setState({ allMeetings });
  }

  onPageChanged = data => {
    const { currentPage, totalPages } = data;
   
    axios.get(`/api/meetings?page=${currentPage}`)
      .then(response => {
        const currentMeetings = response.data.Meetings;
        this.setState({ currentPage, currentMeetings, totalPages });
      });
   }

  render() {

    const { allMeetings, currentMeetings, currentPage, totalPages } = this.state;
    const totalMeetings = allMeetings.length;

    if (totalMeetings === 0) return null;

    const headerClass = ['text-dark py-2 pr-4 m-0', currentPage ? 'border-gray border-right' : ''].join(' ').trim();

    return (
      <div className="container mb-5">
        <div className="row d-flex flex-row py-5">

          <div className="w-100 px-4 py-5 d-flex flex-row flex-wrap align-items-center justify-content-between">
            <div className="d-flex flex-row align-items-center">

              <h2 className={headerClass}>
                <strong className="text-secondary">{totalMeetings}</strong> Meetings
              </h2>

              { currentPage && (
                <span className="current-page d-inline-block h-100 pl-4 text-secondary">
                  Page <span className="font-weight-bold">{ currentPage }</span> / <span className="font-weight-bold">{ totalPages }</span>
                </span>
              ) }

            </div>

            <div className="d-flex flex-row py-4 align-items-center">
              <Pagination totalRecords={totalMeetings} pageLimit={18} pageNeighbours={1} onPageChanged={this.onPageChanged} />
            </div>
          </div>

          { currentMeetings.map(meeting => <Meeting key={meeting.code} title={meeting.title} time={meeting.time} />) }

        </div>
      </div>
    );

  }
   
}


ReactDOM.render(<MeetingApp />, window.react_mount);