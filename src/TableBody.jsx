// https://www.bekk.christmas/post/2021/2/how-to-lazy-render-large-blocks-tables-to-up-performance
import React from "react";
import throttle from "lodash.throttle";

import Modal from "./Modal";

const itemRowHeight = 32; // same height as each row (32px, see styles.css)
const screenHeight = Math.max(
  document.documentElement.clientHeight,
  window.innerHeight || 0
); // get the height of the screen
const offset = screenHeight; // We want to render more than we see, or else we will see nothing when scrolling fast
const rowsToRender = Math.floor((screenHeight + offset) / itemRowHeight);

const TableBody = ({ blocks, smallestInd, showEmpties }) => {
  const [displayStart, setDisplayStart] = React.useState(0);
  const [displayEnd, setDisplayEnd] = React.useState(0);
  const [scrollPosition, setScrollPosition] = React.useState(0);

  const setDisplayPositions = React.useCallback(
    (scroll) => {
      // we want to start rendering a bit above the visible screen
      const scrollWithOffset = Math.floor(scroll - rowsToRender - offset / 2);
      // start position should never be less than 0
      const displayStartPosition = Math.round(
        Math.max(0, Math.floor(scrollWithOffset / itemRowHeight))
      );

      // end position should never be larger than our blocks array
      const displayEndPosition = Math.round(
        Math.min(displayStartPosition + rowsToRender, blocks.length)
      );

      setDisplayStart(displayStartPosition);
      setDisplayEnd(displayEndPosition);
    },
    [blocks.length]
  );

  // We want to set the display positions on renering
  React.useEffect(() => {
    setDisplayPositions(scrollPosition);
  }, [scrollPosition, setDisplayPositions]);

  // add event listeners so we can change the scroll position, and alter what rows to display
  React.useEffect(() => {
    const onScroll = throttle(() => {
      const scrollTop = window.scrollY;
      if (blocks.length !== 0) {
        setScrollPosition(scrollTop);
        setDisplayPositions(scrollTop);
      }
    }, 100);

    window.addEventListener("scroll", onScroll);

    return () => {
      window.removeEventListener("scroll", onScroll);
    };
  }, [setDisplayPositions, blocks.length]);

  const rows = [];

  React.useEffect(() => {
    // for simplicity, scroll back to top of page when toggle b/t showing empty rows
    window.scrollTo({
      top: 0,
      behavior: "auto",
    });
    setScrollPosition(0);
    setDisplayStart(0);
  }, [showEmpties, blocks.length]);

  // add a filler row at the top. The further down we scroll the taller this will be
  rows.push(
    <tr
      key="startRowFiller"
      style={{ height: displayStart * itemRowHeight }}
    ></tr>
  );

  // add the rows to actually render
  for (let i = displayStart; i < displayEnd; ++i) {
    const row = blocks[i];
    let blockStart = null;

    if (showEmpties) {
      const hsfn = Math.floor((smallestInd + i) / 1024);
      const sfn = (smallestInd + i) % 1024;

      if (row) {
        let lastBlock = null;
        rows.push(
          <tr key={i}>
            <td>{hsfn}</td>
            <td>{sfn}</td>
            {row.map((block, j) => {
              blockStart = blockStart > 0 && blockStart - 1;
              if (block !== null) {
                lastBlock = block;
                blockStart = block["airtime"];
                return <Modal ind={j} key={j} block={block} />;
              } else if (blockStart) {
                return <Modal ind={j} key={j} block={lastBlock} />;
              } else {
                return <td key={j}></td>;
              }
            })}
          </tr>
        );
      }
    } else {
      let j = 0;
      if (row) {
        rows.push(
          <tr key={i}>
            <td>{row["HSFN"]}</td>
            <td>{row["SFN"]}</td>
            {Array.apply(null, Array(10)).map((_, k) => {
              blockStart = blockStart > 0 && blockStart - 1;
              if (j >= row["blocks"].length) {
                // there's no more blocks in this row but the remaining ones must either be pink (for remaining airtime) or empty
                if (blockStart)
                  return <Modal ind={k} key={k} block={row["blocks"][j - 1]} />;
                else return <td key={k}></td>;
              }

              const block = row["blocks"][j];

              if (k === block["Sub-FN"]) {
                blockStart = block["airtime"];
                j += 1;
                return <Modal ind={k} key={k} block={block} />;
              } else if (blockStart) {
                return <Modal ind={k} key={k} block={row["blocks"][j - 1]} />;
              } else {
                return <td key={k}></td>;
              }
            })}
          </tr>
        );
      }
    }
  }

  // add a filler row at the end. The further up we scroll the taller this will be
  rows.push(
    <tr
      key="endRowFiller"
      style={{ height: (blocks.length - displayEnd) * itemRowHeight }}
    ></tr>
  );

  return <tbody>{rows}</tbody>;
};

export default TableBody;
