import React from 'react';
import './App.css';
import banner from '../util/banner.jpeg';

import {Link } from "react-router-dom";


function App() {

  return (
    <div className="image">
    	    	<div id="header">
        	<img src={banner} alt="McDowell Sonoran Conversancy" id="banner" width="100%" height ="220px"></img><br />
        	<div id="links2">
        	<Link to="/">Home Page</Link>
        	<Link to="/submission"> Upload Video </Link>
        	<Link to="/email-results"> Get Email Results </Link>
        	<Link to="/results"> Previous Results </Link>
        	<a href="https://www.mcdowellsonoran.org/">Conservancy Home</a>
        	</div>
        </div><br /><br />
        
		<div id="wrapper">
        	<div id="main">

        </div></div>
    </div>
  );
}

export default App;
