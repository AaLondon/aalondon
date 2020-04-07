import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Nav from 'react-bootstrap/Nav'
import RangeSlider from './RangeSlider'

class OnlineMeetingSearchForm extends React.Component {
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

    let day = this.props.day;
    

    const weekDays = ["Now","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    let activeIndex = weekDays.findIndex(element => element.includes(day));
    console.log("MeetingSearchForm Render");
   

    let weekDayNav =  weekDays.map((value, index) => 
    <Nav.Item key={index}>
    <Nav.Link onSelect={this.handleDayChange} eventKey={index}>{value}</Nav.Link>
  </Nav.Item>
  )
    
    return (
      
      <form onSubmit={this.handleSubmit}>
        <Row className="justify-content-center ">
          <Col className="days" xs={10}>
          <Row><Nav fill variant="pills" activeKey={activeIndex} defaultActiveKey="0" >
         {weekDayNav} 
          

</Nav></Row></Col></Row>
        <Row>  
        <Col>
       
        </Col> 
        </Row>
        
      </form>
    );
  }
}



export default OnlineMeetingSearchForm;