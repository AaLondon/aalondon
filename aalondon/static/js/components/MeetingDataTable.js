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
          console.log("componentDidMount");
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
              sorted={column === 'distance_from_client' ? direction : null}
              onClick={this.handleSort('distance_from_client')}
            >
              Distance(miles)
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {_.map(data, ({ code,friendly_time,title, distance_from_client,slug }) => (
            <Table.Row key={code}>
              <Table.Cell>{friendly_time}</Table.Cell>
              <Table.Cell><a href={'/meetings/' + slug}>{title}</a></Table.Cell>
              <Table.Cell>{distance_from_client}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    )
  }
}
