import React, { Component } from 'react';
import ReactDOM from 'react-dom';
/*import Meetings from 'Meetings-api';*/
import Pagination from './components/Pagination';
import Meeting from './components/Meeting';
import axios from 'axios';
import MeetingSearchForm from './components/MeetingSearchForm';



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

   

  

    return (

      <div>
        <MeetingSearchForm value={this.state.value} onInputChange={this.handleInputChange} />
        <div className="table-responsive">
          <table className="table table-sm table-striped">


            <tbody>

              <tr><td><Pagination totalRecords={totalMeetings} pageLimit={10} pageNeighbours={1} onPageChanged={this.onPageChanged} /></td>
                <td className="text-right"><strong>{totalMeetings}</strong> Meetings</td>
              </tr>
              {currentMeetings.map(meeting => <Meeting key={meeting.code} title={meeting.title} time={meeting.time} code={meeting.code} day={meeting.day} slug={meeting.slug}/>)}
            </tbody>
          </table>


        </div>
      </div>








    );

  }

}


ReactDOM.render(<MeetingSearch />, window.react_mount);