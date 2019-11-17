import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

class MeetingSearchForm extends React.Component {
  constructor(props) {
    super(props);


    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDayChange = this.handleDayChange.bind(this);
    
  }


  handleChange(e) {
    this.props.onInputChange(e.target.value);
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }
  handleDayChange(eventKey,e) {
    this.props.onDayChange(e.target.innerText);
  }

  render() {
    
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Postcode:
            <input type="text" value={this.props.value} onChange={this.handleChange} />
        </label>
        <Dropdown >
          <Dropdown.Toggle variant="success" id="dropdown-basic">
            {this.props.day ? this.props.day : "All"}
        </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item onSelect={this.handleDayChange}>All</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Monday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Tuesday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Wednesday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Thursday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Friday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Saturday</Dropdown.Item>
            <Dropdown.Item onSelect={this.handleDayChange}>Sunday</Dropdown.Item>


          </Dropdown.Menu>
        </Dropdown>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}



export default MeetingSearchForm;