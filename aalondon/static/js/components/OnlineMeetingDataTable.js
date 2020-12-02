import _ from "lodash";
import React, { useState } from "react";
import { Table } from "semantic-ui-react";

function MeetingDataTable({currentMeetings}) {
  const [data, setData] = useState(currentMeetings);
  const [column, setColumn] = useState(null);
  const [direction, setDirection] = useState(null);

  const handleSort = (clickedColumn) => () => {
    if (column !== clickedColumn) {
      setColumn(clickedColumn);
      setData(_.sortBy(data, [clickedColumn]));
      setDirection("ascending");

      return;
    }

    setData(data.reverse());
    setDirection(direction === "ascending" ? "descending" : "ascending");
  };

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
            onClick={handleSort("friendly_time")}
            textAlign="center"
          >
            Time
          </Table.HeaderCell>
          <Table.HeaderCell
            sorted={column === "title" ? direction : null}
            onClick={handleSort("title")}
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

export default MeetingDataTable;








