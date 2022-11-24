import React, { useState, useEffect } from "react";
import TableBody from "./TableBody";
import "./App.css";

function App() {
  let [blocksArr, setBlocksArr] = useState([]);
  let [blocksList, setBlocksList] = useState([]);
  let [smallestInd, setSmallestInd] = useState([0, 0]);
  let [showEmpties, setShowEmpties] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/blocks")
      .then((response) => response.json())
      .then((data) => {
        setBlocksArr(data["blocks_arr"]);
        setBlocksList(data["blocks_list"]);
        setSmallestInd(data["smallest_idx"]);
      });
  }, []);

  return (
    <div className="w3-container">
      <h2>NB-IoT Dashboard</h2>
      <p>Shows airtime of DL/UL Transport and DCI Samples/Records</p>

      <div id="toggle-btn">
        <button onClick={() => setShowEmpties(!showEmpties)}>{`Show ${
          showEmpties ? "only non-empty" : "all"
        } rows`}</button>
      </div>
      <table className="w3-table w3-hoverable w3-bordered w3-border w3-centered">
        <thead>
          <tr>
            <th>HSFN</th>
            <th>FN</th>
            <th>Sub-FN</th>
            {Array.apply(null, Array(9)).map((_, i) => (
              <th key={i}></th>
            ))}
          </tr>
          <tr id="hdr-btm-row">
            {["", "", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((colContent, i) => (
              <th key={i}>{colContent}</th>
            ))}
          </tr>
        </thead>
        <TableBody
          blocks={showEmpties ? blocksArr : blocksList}
          smallestInd={smallestInd}
          showEmpties={showEmpties}
        />
      </table>
    </div>
  );
}

export default App;
