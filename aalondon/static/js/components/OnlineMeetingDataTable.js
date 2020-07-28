import sortBy from 'lodash/sortBy'
import map from 'lodash/map'
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
        data: sortBy(data, [clickedColumn]),
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
   

    let tbl = map(data, ({ id, title, time, day, link, description,slug,friendly_time,zoom_password,platform }) => {
      
      
        console.log('ZOOM meeting:'+platform);
        let img='/static/images/zoom.png';
        if (platform === 'Skype'){
          img = '/static/images/skype.png'
        }
        if (zoom_password === 1){
            title = <b>{title+'*'}</b>;
        }
     return (
        <Table.Row key={id}>
          <Table.Cell textAlign="center" >{friendly_time}</Table.Cell>
          <Table.Cell textAlign="center"><div><a href={'/onlinemeetings/' + slug + '/'} >{title} </a></div></Table.Cell>
          <Table.Cell textAlign="center" className='meeting-cell'><img src={img}></img></Table.Cell>
        </Table.Row>
      )
    
    })

    let third_column_field = showPostcode === 0 ? 'distance_from_client' : 'postcode_prefix';

    return (
      <Table sortable celled>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell
              sorted={column === 'friendly_time' ? direction : null}
              onClick={this.handleSort('friendly_time')}
              textAlign="center"
            >
              Time
            </Table.HeaderCell>
            <Table.HeaderCell
              sorted={column === 'title' ? direction : null}
              onClick={this.handleSort('title')}
              textAlign="center"
            >
              Meeting 
            </Table.HeaderCell>
            <Table.HeaderCell textAlign="center">
              Platform 
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
