import React from "react";
import ReactDOM from "react-dom";
import ChatBot from "react-simple-chatbot";
import "../css/bot.css";


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
    component: (
      <div>
        {" "}
        This is a example component with <a href="some_link">link_text</a>{" "}
      </div>
    ),
    asMessage: true,
    end: true,
  },
  {
    id: "4",
    message:
      "Great. Let’s help you to get what you need from our AA-London site.",
    trigger: "5",
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
      id:"6",
      message:
      "Ok. How about these?",
    trigger: "7",

  },
  {
      id:"7",
      options: [
        { value: 1, label: "I might have a drinking problem and want to speak with someone.", trigger: "8" },
        { value: 2, label: "Existing Member", trigger: "9" },
      ],
  },
  {
      id:"8",
      message:"Sure. You can do that in different ways...",
      trigger:"9"

  },
  {
      id:"9",
      options: [
        { value: 1, label: "Live Chat", trigger: "8" },
        { value: 2, label: "Send AA an email", trigger: "9" },
        { value: 3, label: "Call the AA helpline 0800 9177 650", trigger: "9" },
        

      ],

  }
];

ReactDOM.render(
  <div>
    <ChatBot steps={steps} />
  </div>,
  document.getElementById("root")
);
