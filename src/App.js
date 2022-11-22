import React, { useState, useEffect } from 'react';
import './App.css';

function App() {

  let [blocks, setBlocks] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:5000/blocks')
    .then(response => response.json())
    .then(data => setBlocks(data))
  }, []);

  return (
    <div className='w3-container'>
      <h2>NB-IoT Dashboard</h2>
      <p>Shows airtime of DL/UL Transport and DCI Samples/Records</p>

      <table className='w3-table w3-hoverable w3-striped w3-border w3-bordered w3-centered'>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>FN</th>
            <th>Sub-FN</th>
            {Array.apply(null, Array(9)).map((_, i) => (
              <th key={i}></th>
            ))}
          </tr>
          <tr>
          {['', '', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((colContent, i) => (
            <th key={i}>{colContent}</th>
          ))}
          </tr>
        </thead>
        <tbody>
          {blocks && blocks.map((block, i) => {
            let blockStart = null;
            return (
              <tr key={i}>
                <td>{block['timestamp']}</td>
                <td>{block['FN']}</td>
                {
                  Array.apply(null, Array(10)).map((_, j) => {
                    blockStart = blockStart > 0 && blockStart - 1;
                    if (j === block['Sub-FN']) {
                      blockStart = block['airtime'];
                      return (<td key={j} style={{ backgroundColor: blockStart && "pink", borderRight: blockStart ? "none" : "1px solid #ccc" }}>{block['type']}</td>);
                    }
                    else {
                      return (<td key={j} style={{ backgroundColor: blockStart && "pink", borderRight: blockStart ? "none" : "1px solid #ccc" }}></td>);
                    }
                  })
                }
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default App;
