import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

const useStyles = makeStyles({
  root: {
    width: 300,
  },
});

const marks = [
    {
      value: 0,
      label: '0 mi',
    },
    {
      value: 15,
      label: '15 mi',
    },
   
    {
      value: 5,
      label: '5 mi',
    },
    {
      value: 10,
      label: '10 mi',
    },
   
  ];

function valuetext(value) {
  return `${value}°C`;
}

function RangeSlider({onSliderChange}) {
  const classes = useStyles();
  const [value, setValue] = React.useState(15);

  const handleChange = (event, newValue) => {
    setValue(newValue);
    onSliderChange(newValue);
};

  return (
    <div className={classes.root}>
      <Typography id="discrete-slider" gutterBottom>
        Distance Filter
      </Typography>
      <Slider 
      max={15}
        value={value}
        marks={marks}
        onChange={handleChange}
        valueLabelDisplay="auto"
        aria-labelledby="discrete-slider"
        getAriaValueText={valuetext}
      />
    </div>
  );
}

export default RangeSlider;