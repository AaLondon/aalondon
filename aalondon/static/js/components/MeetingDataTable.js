import _ from "lodash";
import React, { useState } from "react";
import { Table } from "semantic-ui-react";

function MeetingDataTable({currentMeetings, showPostcode, minMiles, maxMiles}) {
  const [data, setData] = useState(currentMeetings);
  const [column, setColumn] = useState(null);
  const [direction, setDirection] = useState(null);

  const handleSort = (clickedColumn) => () => {
    if (column !== clickedColumn) {
      setColumn(clickedColumn);
      setData(_.sortBy(data, [clickedColumn, "day_number"]));
      setDirection("ascending");

      return;
    }

    setData(data.reverse());
    setDirection(direction === "ascending" ? "descending" : "ascending");
  };

  let tbl = _.map(
    data,
    ({
      code,
      friendly_time,
      title,
      distance_from_client,
      link,
      slug,
      postcode_prefix,
      day,
      covid_open_status,
      place,
    }) => {
      let placeText = "";
      let img = "/static/images/zoom.png";
      let meetingUrlPath = "/onlinemeetings/";
      if (place !== "zoom") {
        placeText = place;
        meetingUrlPath = "/meetings/";
        img = "/static/images/building-location-pin.png";
      }

      if (
        showPostcode === 1 ||
        (distance_from_client >= minMiles &&
          distance_from_client <= maxMiles)
      ) {
        return (
          <Table.Row key={code}>
            <Table.Cell textAlign="center">{day}</Table.Cell>
            <Table.Cell textAlign="center">{friendly_time}</Table.Cell>
            <Table.Cell textAlign="center">
              <a href={meetingUrlPath + slug}>{title}</a>
            </Table.Cell>
            <Table.Cell textAlign="center" className="meeting-cell">
              {" "}
              <div>
                <a href={link}>
                  <img src={img} alt=""></img>
                </a>
              </div>
              <div>{placeText}</div>
            </Table.Cell>
            <Table.Cell textAlign="center">
              {covid_open_status === 0 ? "Inactive" : "Active"}
            </Table.Cell>
          </Table.Row>
        );
      }
    }
  );

  return (
    <Table sortable celled fixed>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell
            sorted={column === "day" ? direction : null}
            onClick={handleSort("day")}
          >
            Day
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "friendly_time" ? direction : null}
            onClick={handleSort("friendly_time")}
          >
            Time
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "title" ? direction : null}
            onClick={handleSort("title")}
          >
            Title
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "place" ? direction : null}
            onClick={handleSort("place")}
          >
            Place
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "covid_open_status" ? direction : null}
            onClick={handleSort("covid_open_status")}
          >
            Covid Open Status
          </Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      <Table.Body>{tbl}</Table.Body>
    </Table>
  );
}

export default MeetingDataTable;