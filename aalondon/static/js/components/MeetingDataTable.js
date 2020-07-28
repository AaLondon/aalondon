import map from 'lodash/map'
import sortBy from 'lodash/sortBy'
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
  
  }

  handleSort = (clickedColumn) => () => {
    const { column, data, direction } = this.state

    if (column !== clickedColumn) {
      this.setState({
        column: clickedColumn,
        data: sortBy(data, [clickedColumn,'day_number']),
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


    let tbl = map(data, ({ code, friendly_time, title, distance_from_client, slug, postcode_prefix, day,covid_open_status,place }) => {
      let placeText = '';
      let img='/static/images/zoom.png';
      let meetingUrlPath = '/onlinemeetings/'
      if (place !== 'zoom'){
        placeText = place;
        meetingUrlPath = '/meetings/'
        img = '/static/images/zoomAA-location-pin.png'
      }



      if ((showPostcode === 1) || (distance_from_client >= this.props.minMiles && distance_from_client <= this.props.maxMiles))
      {

       
     return (
        <Table.Row key={code}>
          <Table.Cell textAlign="center">{day}</Table.Cell>
          <Table.Cell textAlign="center">{friendly_time}</Table.Cell>
          <Table.Cell textAlign="center"><a href={meetingUrlPath + slug }>{title}</a></Table.Cell>
          <Table.Cell textAlign="center" className='meeting-cell'> <div><img src={img}></img></div><div>{placeText}</div></Table.Cell>
          <Table.Cell textAlign="center">{covid_open_status === 0 ? 'Inactive':'Active'}</Table.Cell>
          
        </Table.Row>
      )
    }
    })

    let third_column_field = showPostcode === 0 ? 'distance_from_client' : 'postcode_prefix';

    return (
      <Table sortable celled fixed >
        <Table.Header>
          <Table.Row>
          <Table.HeaderCell
              sorted={column === 'day' ? direction : null}
              onClick={this.handleSort('day')}
            >
              Day
            </Table.HeaderCell>
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
              sorted={column === 'place' ? direction : null}
              onClick={this.handleSort('place')}
            >
              Place
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'covid_open_status' ? direction : null}
              onClick={this.handleSort('covid_open_status')}
            >
              Covid Open Status
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
