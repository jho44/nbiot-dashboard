import React, { useState, useEffect } from "react";
import TableBody from "./TableBody";
import AggStats from "./AggStats";
import "./App.css";

function App() {
  let [blocksArr, setBlocksArr] = useState([]);
  let [blocksList, setBlocksList] = useState([]);
  let [smallestInd, setSmallestInd] = useState(0);
  let [greatestHSFNAndFNPair, setGreatestHSFNAndFNPair] = useState([0, 0]);
  let [smallestHSFNAndFNPair, setSmallestHSFNAndFNPair] = useState([0, 0]);
  let [start, setStart] = useState(0);
  let [end, setEnd] = useState(0);
  let [showEmpties, setShowEmpties] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/blocks")
      .then((response) => response.json())
      .then((data) => {
        setBlocksArr(data["blocks_arr"]);
        setBlocksList(data["blocks_list"]);
        setSmallestInd(data["smallest_idx"]);
        setGreatestHSFNAndFNPair(data["greatest_HSFN_and_FN_pair"]);
        setSmallestHSFNAndFNPair(data["smallest_HSFN_and_FN_pair"]);

        const smallest = data["smallest_HSFN_and_FN_pair"];
        const greatest = data["greatest_HSFN_and_FN_pair"];
        setStart(smallest[0] * 1024 + smallest[1]);
        setEnd(greatest[0] * 1024 + greatest[1]);
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    let startHsfn = e.target[0].value;
    let endHsfn = e.target[2].value;
    let startFn = e.target[1].value;
    let endFn = e.target[3].value;

    // check input
    if (
      !startHsfn.length ||
      !endHsfn.length ||
      !startFn.length ||
      !endFn.length
    ) {
      window.alert("One of the time range fields is empty.");
      return;
    }

    startHsfn = parseInt(startHsfn);
    endHsfn = parseInt(endHsfn);
    startFn = parseInt(startFn);
    endFn = parseInt(endFn);

    if (
      startHsfn * 1024 + startFn <
        smallestHSFNAndFNPair[0] * 1024 + smallestHSFNAndFNPair[1] ||
      endHsfn * 1024 + endFn >
        greatestHSFNAndFNPair[0] * 1024 + greatestHSFNAndFNPair[1]
    ) {
      // out of bounds
      window.alert(
        "Either the start or end (HSFN, FN) is out of bounds of this dataset."
      );
      return;
    }

    setStart(startHsfn * 1024 + startFn);
    setEnd(endHsfn * 1024 + endFn);
  };

  return (
    <div className="w3-container">
      <h2>NB-IoT Dashboard</h2>
      <p>Shows airtime of DL/UL Transport and DCI Samples/Records</p>

      <div id="toggle-btn">
        <p>
          Note: The min (HSFN, FN) pair value is ({smallestHSFNAndFNPair[0]},{" "}
          {smallestHSFNAndFNPair[1]}) and the max (HSFN, FN) pair value is (
          {greatestHSFNAndFNPair[0]}, {greatestHSFNAndFNPair[1]}).
        </p>
        <form onSubmit={handleSubmit} id="hsfn-fn-form">
          <div>
            <label>Start HSFN:</label>
            <input
              type="number"
              name="start-hsfn"
              max={greatestHSFNAndFNPair[0]}
              min={smallestHSFNAndFNPair[0]}
            />

            <label>Start FN:</label>
            <input type="number" name="start_fn" max={1023} min={0} />

            <label>End HSFN:</label>
            <input
              type="number"
              name="end-hsfn"
              max={greatestHSFNAndFNPair[0]}
              min={smallestHSFNAndFNPair[0]}
            />

            <label>End FN:</label>
            <input type="number" name="end_fn" max={1023} min={0} />
          </div>
          <button type="submit" id="update-time-range-btn">
            Update Time Range
          </button>
        </form>

        <button onClick={() => setShowEmpties(!showEmpties)}>{`Show ${
          showEmpties ? "only non-empty" : "all"
        } rows`}</button>

        <AggStats blocksList={blocksList} start={start} end={end} />
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
          blocks={
            showEmpties
              ? blocksArr.slice(start - smallestInd, end - smallestInd + 1)
              : blocksList.filter((block) => {
                  const fn = block.HSFN * 1024 + block.SFN;
                  return fn >= start && fn <= end;
                })
          }
          smallestInd={start}
          showEmpties={showEmpties}
        />
      </table>
    </div>
  );
}

export default App;
