import React from "react";
import ReactDOM from "react-dom";
import ChatBot from "react-simple-chatbot";
import "../css/bot.css";



function GoToUrl(props) {
  let target = "_self"
  let url = props.url
  let label = props.label
  if (props.target) {
    target = "_blank"
  }

  window.open(url, target);
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
        trigger: "21",
      },
      { value: 2, label: "Do you need some AA literature?", trigger: "22" },
      { value: 3, label: "Find your next AA meeting", trigger: "14" },
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
      { value: 1, label: "Live Chat(opens in a new window)", trigger: "24" },
      { value: 2, label: "Send AA an email", trigger: "25" },
      { value: 3, label: "Call the AA helpline 0800 9177 650", trigger: "23" },


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

      { value: 1, label: "AA Informational Videos", trigger: "26" },
      { value: 2, label: "Call the AA helpline 0800 9177 650", trigger: "23" },


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
    trigger: "5",
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

      { value: 1, label: "AA Literature", trigger: "22" },
      { value: 2, label: "AA Infomational Videos", trigger: "26" },
      { value: 3, label: "Phone the AA UK helpline 0800 9177 650" },


    ],

  },
  {
    id: '21',
    component: <GoToUrl url={'/new-to-aa/are-you-alcoholic/'} label={'Taking you to quiz....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '22',
    component: <GoToUrl url={'/resources/aa-literature/'} label={'Taking you to literature....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '23',
    component: <GoToUrl url={'tel:08009177650'} label={'Calling AA....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '24',
    component: <GoToUrl target="_blank" url={'https://www.alcoholics-anonymous.org.uk/Home'} label={'Taking you to chat on the national website....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '25',
    component: <GoToUrl url={'mailto:help@aamail.org'} label={'Emailing AA....'} />,
    asMessage: true,
    end: true
  },
  {
    id: '26',
    component: <GoToUrl url={'/videos'} label={'AA Videso'} />,
    asMessage: true,
    end: true
  },


];

ReactDOM.render(
  <div>
    <ChatBot steps={steps} headerTitle="Navigate the menu below" botAvatar="/static/images/Chatbot_bot-icon.svg"
      userAvatar="/static/images/Chatbot_smiles-icon.svg" />
  </div>,
  document.getElementById("root")
);
