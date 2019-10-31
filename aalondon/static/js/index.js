import React from "react";
import ReactDOM from "react-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";


class Test extends React.Component {
  render() {
    var list = window.props;
    console.log(window);
    var total_data = window.total_data;
    var suspended_data = window.suspended_data;
    var signup_url = window.signup;
    console.log(signup_url);
    return (
      <Container>
        <Row><Col className="text-center py-4"><h1>We are defending residents of Camden against the burning injustice of suspended bay parking fines</h1></Col></Row>
        <Row><Col className="text-center"><h3>Average number of suspended bay penalty charge notices per year : 10000+</h3></Col></Row>
        <Row><Col className="text-center"><h3>Approximate revenue of suspended bay penalty charge notices per year : £500000+</h3></Col></Row>
<Row><Col className="text-center"><h3>It is the goal of this website to make that amount £0</h3></Col></Row>
        <Row>

          <Col>
            <Bar
              data={total_data}
              width={100}
              height={500}
              options={{ maintainAspectRatio: false,scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            } }}
            />
          </Col>
        </Row>
        <Row><Col className="text-center"><h3>Let me help you avoid these forever!</h3></Col></Row>
        <Row><Col className="text-center"><Button href={signup_url} size="lg">Sign Up</Button></Col></Row>
        
        
      </Container>



    );
  }
}


ReactDOM.render(<Test />, window.react_mount);
