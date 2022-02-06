import React from 'react';
import './VideoUpload.css';
import banner from './banner.png';

import {Link } from "react-router-dom";


function VideoUpload() {

  return (
    <div id ="c">
    	<div id="header">
        	<img src={banner} alt="McDowell Sonoran Conversancy" id="banner" width="100%" height ="220px"></img><br />
        	<div id="links2">
        	<Link to="/">Main Page</Link>
        	<Link to="/submission"> Upload Video </Link>
        	<Link to="/email-results"> Get Email Results </Link>
        	<Link to="/"> Previous Results </Link>
        	<a href="https://www.mcdowellsonoran.org/">Conservancy Home</a>
        	</div>
        </div><br /><br />
        
		<div id="wrapper2">
        	<div id="main2">
        		<form>
        			<label>Date recorded</label> <input type="date" id="filedate"></input><br />
        			<h3>Camera 1 Video</h3>
        			<label>Choose a file</label><input type="file" id="filename"></input><br /><br />
        			<h3>Camera 2 Video</h3>
        			<label>Choose a file</label><input type="file" id="filename"></input><br /><br />
        			<label>Enter additional information?</label><br />
        				<input type="radio" value="yes"></input><h5>yes</h5>
        				<input type="radio" value="no"></input><h5>no</h5><br />
        			<button type="submit"> UPLOAD VIDEO </button>
				</form>

			</div>
        </div>
    </div>
  );
}

export default VideoUpload;
