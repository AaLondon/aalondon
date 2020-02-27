import _ from 'lodash'
import React, { Component } from 'react'
import { Table } from 'semantic-ui-react'


const tableData = [
  { name: 'John', age: 15, gender: 'Male' },
  { name: 'Amber', age: 40, gender: 'Female' },
  { name: 'Leslie', age: 25, gender: 'Other' },
  { name: 'Ben', age: 70, gender: 'Male' },
]

export default class MeetingDataTable extends Component {
  constructor(props) {
    super(props);


    this.state = {
      data: this.props.currentMeetings,
      column: null,
      direction: null,

    };
  }

  componentDidMount() {
    console.log("MeetingDataTable componentDidMount");
  }

  handleSort = (clickedColumn) => () => {
    const { column, data, direction } = this.state

    if (column !== clickedColumn) {
      this.setState({
        column: clickedColumn,
        data: _.sortBy(data, [clickedColumn]),
        direction: 'ascending',
      })

      return
    }

    this.setState({
      data: data.reverse(),
      direction: direction === 'ascending' ? 'descending' : 'ascending',
    })
  }

  render() {
    const { column, data, direction } = this.state
    let thirdColumnHeader = "Distance(miles)";
    let showPostcode = this.props.showPostcode;
   

    let tbl = _.map(data, ({ code, friendly_time, title, distance_from_client, slug, postcode_prefix }) => {
      
      if ((showPostcode === 1) || (distance_from_client >= this.props.minMiles && distance_from_client <= this.props.maxMiles))
      {
        console.log(typeof distance_from_client);
     return (
        <Table.Row key={code}>
          <Table.Cell>{friendly_time}</Table.Cell>
          <Table.Cell><a href={'/meetings/' + slug + '/#meetingmap'}>{title}</a></Table.Cell>
          <Table.Cell>{showPostcode === 0 ? distance_from_client : postcode_prefix}</Table.Cell>
        </Table.Row>
      )
    }
    })

    let third_column_field = showPostcode === 0 ? 'distance_from_client' : 'postcode_prefix';

    return (
      <Table sortable celled fixed unstackable>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell
              sorted={column === 'friendly_time' ? direction : null}
              onClick={this.handleSort('friendly_time')}
            >
              Time
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'title' ? direction : null}
              onClick={this.handleSort('title')}
            >
              Title
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === third_column_field ? direction : null}
              onClick={this.handleSort(third_column_field)}
            >
              {showPostcode === 0 ? "Distance(miles)" : "Postcode"}
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {tbl}
        </Table.Body>
      </Table>
    )
  }
}
