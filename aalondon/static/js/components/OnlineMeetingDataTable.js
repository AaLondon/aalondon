import _ from "lodash";
import React, { Component } from "react";
import { Table } from "semantic-ui-react";

export default class MeetingDataTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: this.props.currentMeetings,
      column: null,
      direction: null,
    };
  }

  handleSort = (clickedColumn) => () => {
    const { column, data, direction } = this.state;

    if (column !== clickedColumn) {
      this.setState({
        column: clickedColumn,
        data: _.sortBy(data, [clickedColumn]),
        direction: "ascending",
      });

      return;
    }

    this.setState({
      data: data.reverse(),
      direction: direction === "ascending" ? "descending" : "ascending",
    });
  };

  render() {
    const { column, data, direction } = this.state;
    let tbl = _.map(
      data,
      ({ id, title, link, slug, friendly_time, zoom_password, platform, type }) => {
        let santa = '/static/images/santa.png';
        let santaImg= <></>
        let zoomImg = '/static/images/zoom.png';
        let physicalImg = '/static/images/building-location-pin.png'
        let meetingUrlPath = '/onlinemeetings/' + slug
        let img = <div><img src={zoomImg}></img></div>
        if (type === 'ONL') {
          img = <><div><img src={zoomImg}></img></div>{santaImg}</>
        }else if(type === 'F2F')
        {
          img = <><div><img src={physicalImg}></img></div>{santaImg}</>
          meetingUrlPath = '/meetings/' + slug + "/"
        }else{
          img = <><div><img src={zoomImg}></img>+<img src={physicalImg}></img></div>{santaImg}</>
          meetingUrlPath = '/meetings/' + slug +"/"
        }
          


        return (
          <Table.Row key={id}>
            <Table.Cell textAlign="center">{friendly_time}</Table.Cell>
            <Table.Cell textAlign="center">
              <div>
                <a href={meetingUrlPath}>{title} </a>
              </div>
            </Table.Cell>
            <Table.Cell textAlign="center" className="meeting-cell">
                {img}
            </Table.Cell>
          </Table.Row>
        );
      }
    );

    return (
      <Table sortable celled>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell
              sorted={column === "friendly_time" ? direction : null}
              onClick={this.handleSort("friendly_time")}
              textAlign="center"
            >
              Time
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === "title" ? direction : null}
              onClick={this.handleSort("title")}
              textAlign="center"
            >
              Meeting
            </Table.HeaderCell>
            <Table.HeaderCell textAlign="center">Platform</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>{tbl}</Table.Body>
      </Table>
    );
  }
}
