import React from 'react';
import './App.css';
import logo from './graph.png';
import banner from './banner.png';

import {Link } from "react-router-dom";


function App() {

  return (
    <div id ="c">
    	<div id="header">
        	<img src={banner} alt="McDowell Sonoran Conversancy" id="banner" width="100%" height ="220px"></img><br /><br /><br />
        </div><br /><br />
        
		<div id="wrapper">
        	<div id="main">
        		<div id="link" className="link1"><Link to="/submission"> Upload Video </Link>
        			<div className="desc1">Upload survey videos to analyze and record data to Sheets. </div></div>
        		<div className="link2"><Link to="/email-results"> Get Email Results </Link>
        			<div className="desc2">Upload one video at a time for a wait-free email with results when processing is complete.</div></div>
        		<div className="link3"><Link to="/"> Previous Results </Link>
        			<div className="desc3">View previous results, graphs, and other visual displays of the data. </div></div>
        		<div id="link" className="link4"><a href="https://www.mcdowellsonoran.org/">Conservancy Home</a>
					<div className="desc4">Visit the McDowell Sonoran Conservancy's homepage. </div></div>
			</div>
        </div>
    </div>
  );
}

export default App;
