import React from "react";
import ReactDOM from "react-dom";
import ChatBot from "react-simple-chatbot";
import "../css/bot.css";

async function GoToUrl(props) {
  let url = props.url
  let label = props.label
  window.open(url, "_self");
  return label
}


const steps = [
  {
    id: "1",
    message:
      "Welcome. My name is ChAAt. I’m here to help you navigate this site. Are you…?",
    trigger: "2",
  },
  {
    id: "2",
    options: [
      { value: 1, label: "New to AA", trigger: "4" },
      { value: 2, label: "Existing Member", trigger: "3" },
    ],
  },
  {
    id: "3",
    message:
      "Great. Here are some options for you",
    trigger: "13",
  },
  {
    id: "5",
    options: [
      {
        value: 1,
        label: "Am I an alcoholic? Take the short quiz",
        trigger: "4",
      },
      { value: 2, label: "Do you need some AA literature?", trigger: "3" },
      { value: 3, label: "Find your next AA zoom meeting", trigger: "3" },
      { value: 4, label: "Show me more options please", trigger: "6" },
    ],
  },
  {
    id: "6",
    message:
      "Ok. How about these?",
    trigger: "7",

  },
  {
    id: "7",
    options: [
      { value: 1, label: "I want to speak to someone", trigger: "8" },
      { value: 2, label: "I'm helping someone else", trigger: "10" },
    ],
  },
  {
    id: "8",
    message: "Sure. You can do that in different ways...",
    trigger: "9"

  },
  {
    id: "9",
    options: [
      { value: 1, label: "Live Chat(opens in a new window)", trigger: "8" },
      { value: 2, label: "Send AA an email", trigger: "9" },
      { value: 3, label: "Call the AA helpline 0800 9177 650", trigger: "12" },


    ],

  },
  {
    id: "10",
    message: "Sure. Here are some options...",
    trigger: "11"

  },
  {
    id: "11",
    options: [
      
      { value: 1, label: "AA Informational Videos" },
      { value: 2, label: "Call the AA helpline 0800 9177 650" },


    ],

  },
  {
    id: '12',
    component: <GoToUrl url={'/meetingsearch'} label={'Taking you to our meeting finder'} />,
    asMessage: true,
    end: true
  },
  {
    id: "4",
    message:
      "Great. Let’s help you to get what you need from our AA-London site.",
    trigger: "13",
  },
  {
    id: "13",
    options: [
      { value: 1, label: "Find a meeting", trigger: "14" },
      { value: 2, label: "Learn about Service", trigger: "15" },
      { value: 3, label: "Practicing Tradition 7", trigger: "16" },
      { value: 4, label: "Upcoming Events", trigger: "17" },
      { value: 5, label: "Update my meeting details", trigger: "18" },
      { value: 6, label: "I'm helping someone else", trigger: "19" },
    ],
  },
  {
    id: '14',
    component: <GoToUrl url={'/meetingsearch'} label={'Taking you to our meeting finder...'} />,
    asMessage: true,
    end: true
  },
  {
    id: '15',
    component: <GoToUrl url={'/service'} label={'Taking you to our Service page...'} />,
    asMessage: true,
    end: true
  },
  {
    id: '16',
    component: <GoToUrl url={'/resources/tradition-7-online/'} label={'Taking you to our Tradition 7 info....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '17',
    component: <GoToUrl url={'/events'} label={'Taking you to our Events....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '18',
    component: <GoToUrl url={'/update'} label={'Lets get your meeting updated....'} />,
    asMessage: true,
    end: true
  },
  {
    id: "19",
    message: "Sure. Here are some options...",
    trigger: "20"

  },
  {
    id: "20",
    options: [
      
      { value: 1, label: "AA Literature" },
      { value: 2, label: "AA Infomational Videos" },
      { value: 3, label: "Phone the AA UK helpline 0800 9177 650" },


    ],

  },
  

];

ReactDOM.render(
  <div>
    <ChatBot steps={steps} />
  </div>,
  document.getElementById("root")
);
