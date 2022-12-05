// https://codepen.io/joykureel/pen/RXKRqv?editors=0110
import React, { useState } from "react";
import "./App.css";

function Modal({ ind, block }) {
  const [content, setContent] = useState(null);

  function renderModal() {
    if (block["type"] === "DL-DCI")
      return (
        <div className="modal-list">
          {Object.entries(block).map(([key, value], i) => {
            if (
              key !== "SFN" &&
              key !== "Sub-FN" &&
              key !== "HSFN" &&
              key !== "airtime" &&
              key !== "type"
            )
              return (
                <div key={i}>
                  {key}: {value}
                </div>
              );
          })}
        </div>
      );
    else
      return (
        <div className="modal-list">
          {Object.entries(block).map(([key, value], i) => {
            if (key !== "Mac Hdr + CE" && key !== "airtime" && key !== "type")
              return (
                <div key={i}>
                  {key}: {value}
                </div>
              );
          })}
        </div>
      );
  }
  const handleLeave = () => {
    return setContent(null);
  };

  const handleHover = () => {
    return setContent(renderModal());
  };

  function determineColor() {
    // DCI block
    if (block["tx-success"] === undefined) return "pink";

    if (block["tx-success"]) return "#ffe8bf"; // biege
    return "brown";
  }

  function type() {
    if (ind === block["Sub-FN"]) {
      if (ind === 0) return `${block["type"]} | BC`;
      else return block["type"];
    }
  }

  return (
    <td
      style={{
        backgroundColor: determineColor(),
        borderRight: "none",
        color: determineColor() === "brown" && "white",
      }}
      className="modal-relevance"
      onMouseOver={handleHover}
      onMouseLeave={handleLeave}
    >
      {type()}
      {content}
    </td>
  );
}

export default Modal;
