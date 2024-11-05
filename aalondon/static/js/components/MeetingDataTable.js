import _ from 'lodash'
import React, { Component } from 'react'
import { Table } from 'semantic-ui-react'

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
        data: _.sortBy(data, [clickedColumn, 'day_number']),
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
    let tbl = _.map(data, ({ code, friendly_time, title, distance_from_client, link, slug, postcode_prefix, day, place,type, temporary_changes, temporary_changes_visible }) => {
      let placeText = '';
      let zoomImg = '/static/images/zoom.png';
      let santa = '/static/images/santa.png';
      let physicalImg = '/static/images/building-location-pin.png'
      let meetingUrlPath = '/onlinemeetings/'
      let img = <img src={zoomImg}></img>
      let santaImg= <></>
      if (type === 'ONL') {
        img = <><div><img src={zoomImg}></img></div>{santaImg}</>
      }else if(type === 'F2F')
      {
        img = <><div><img src={physicalImg}></img></div>{santaImg}</>
        meetingUrlPath = '/meetings/'
      }else{
        img = <><div><img src={zoomImg}></img>+<img src={physicalImg}></img></div>{santaImg}</>
        meetingUrlPath = '/meetings/'
      }
        



    

        return (
          <Table.Row key={code} className='p-10'>
            <Table.Cell textAlign="center">{day}</Table.Cell>
            <Table.Cell textAlign="center">{friendly_time}</Table.Cell>
            <Table.Cell textAlign="center"><a href={meetingUrlPath + slug}>{title}
            {temporary_changes_visible}
            { temporary_changes_visible == false ? '' :
                <div>
                  <span className="text-center text-sm">*Temporary changes - Click to view</span>
                </div>
              }
              </a></Table.Cell>

            <Table.Cell textAlign="center" className='meeting-cell'> {img}</Table.Cell>
            <Table.Cell textAlign="center">{postcode_prefix}</Table.Cell>
          </Table.Row>
        )
    
    })


    let third_column_field = showPostcode === 0 ? 'distance_from_client' : 'postcode_prefix';

    return (
      <Table sortable celled  >
        <Table.Header>
          <Table.Row textAlign='center'>
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
              sorted={column === 'postcode' ? direction : null}
              onClick={this.handleSort('postcode')}
            >
              Postcode
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
