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
            if (
              key !== "Mac Hdr + CE" &&
              key !== "airtime" &&
              key !== "type" &&
              key !== "tx-success"
            )
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
      else if (ind === 5) return `${block["type"]} | NPSS`;
      else if (ind === 9 && block["SFN"] % 2 === 1)
        return `${block["type"]} | NSSS`;
      else return block["type"];
    }
  }

  return (
    <td
      style={{
        backgroundColor: determineColor(),
        borderRight: "none",
      }}
      className="modal-relevance"
      onMouseOver={handleHover}
      onMouseLeave={handleLeave}
    >
      <p style={{ color: determineColor() === "brown" && "white", margin: 0 }}>
        {type()}
      </p>
      {content}
    </td>
  );
}

export default Modal;
