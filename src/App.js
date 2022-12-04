import React, { useState, useEffect, useCallback } from "react";
import TableBody from "./TableBody";
import "./App.css";

const TBS_TABLE = [
  [16, 32, 56, 88, 120, 152, 208, 256],
  [24, 56, 88, 144, 176, 208, 256, 344],
  [32, 72, 144, 176, 208, 256, 328, 424],
  [40, 104, 176, 208, 256, 328, 440, 568],
  [56, 120, 208, 256, 328, 408, 552, 680],
  [72, 144, 224, 328, 424, 504, 680, 872],
  [88, 176, 256, 392, 504, 600, 808, 1032],
  [104, 224, 328, 472, 584, 680, 968, 1224],
  [120, 256, 392, 536, 680, 808, 1096, 1352],
  [136, 296, 456, 616, 776, 936, 1256, 1544],
  [144, 328, 504, 680, 872, 1032, 1384, 1736],
  [176, 376, 584, 776, 1000, 1192, 1608, 2024],
  [208, 440, 680, 904, 1128, 1352, 1800, 2280],
  [224, 488, 744, 1128, 1256, 1544, 2024, 2536],
];

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

  const getNumSubFNsForDLData = useCallback(() => {
    const actualBlocksRendered = blocksList.filter((block) => {
      const fn = block.HSFN * 1024 + block.SFN;
      return fn >= start && fn <= end;
    });

    let ctr = 0;
    actualBlocksRendered.forEach((hyperblock) => {
      hyperblock.blocks.forEach((block) => {
        if (block["type"] === "DL-DATA") {
          ctr += block["airtime"];
        }
      });
    });
    return ctr;
  }, [start, end, blocksList]);

  const getNumBitsTransmittedInDLData = useCallback(() => {
    const actualBlocksRendered = blocksList.filter((block) => {
      const fn = block.HSFN * 1024 + block.SFN;
      return fn >= start && fn <= end;
    });

    let ctr = 0;
    actualBlocksRendered.forEach((hyperblock) => {
      hyperblock.blocks.forEach((block) => {
        if (
          block["type"] === "DL-DCI" &&
          block["DL Grant Present"] === "True"
        ) {
          ctr += TBS_TABLE[block["MCS"]][block["Resource Assignment"]];
        }
      });
    });
    return ctr;
  }, [start, end, blocksList]);

  return (
    <div className="w3-container">
      <h2>NB-IoT Dashboard</h2>
      <p>Shows airtime of DL/UL Transport and DCI Samples/Records</p>

      <div id="toggle-btn">
        <p>
          Note: The max (HSFN, FN) pair value is ({greatestHSFNAndFNPair[0]},{" "}
          {greatestHSFNAndFNPair[1]}) and the min (HSFN, FN) pair value is (
          {smallestHSFNAndFNPair[0]}, {smallestHSFNAndFNPair[1]}).
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

        <h3>Aggregated Statistics</h3>
        <p>Number of Sub-FNs used for DL Data: {getNumSubFNsForDLData()}</p>
        <p>
          Total number of bits transmitted in DL Data:{" "}
          {getNumBitsTransmittedInDLData()}
        </p>
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
