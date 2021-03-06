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
      ({ id, title, link, slug, friendly_time, zoom_password, platform }) => {
        let img = "/static/images/zoom.png";
        if (platform === "Skype") {
          img = "/static/images/skype.png";
        }
        if (zoom_password === 1) {
          title = <b>{title + "*"}</b>;
        }
        return (
          <Table.Row key={id}>
            <Table.Cell textAlign="center">{friendly_time}</Table.Cell>
            <Table.Cell textAlign="center">
              <div>
                <a href={"/onlinemeetings/" + slug + "/"}>{title} </a>
              </div>
            </Table.Cell>
            <Table.Cell textAlign="center" className="meeting-cell">
              <a href={link}>
                <img src={img} alt="Go to meeting"></img>
              </a>
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
