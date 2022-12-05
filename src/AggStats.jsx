import React, { useCallback } from "react";
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

function AggStats({ blocksList, start, end }) {
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
    <>
      <h3>Aggregate Statistics</h3>
      <p>Number of Sub-FNs used for DL Data: {getNumSubFNsForDLData()}</p>
      <p>
        Total number of bits transmitted in DL Data:{" "}
        {getNumBitsTransmittedInDLData()}
      </p>
    </>
  );
}

export default AggStats;
