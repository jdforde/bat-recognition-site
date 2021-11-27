import React from 'react';
import './App.css';
import logo from './graph.png';

function App() {
	function handleClick() {
    	console.log('You clicked submit.');
  	}

  return (
    <div className ="container" id ="c">
    	<div id="header">
        	<h1> McDowell Sonoran Conservancy Bat Recording Upload </h1>
        	<h2> Upload a video to receive bat entry/exit counts</h2>
        	</div><br /><br />
        <div id="main">
        <form>
        	<label>File name</label><input type="text" id="filename"></input><br />
        	<label>Date recorded</label> <input type="date" id="filedate"></input><br />
        	<label>Choose a file</label><input type="file" id="filename"></input><br /><br />
        	<button type="submit" onClick={handleClick}> SUBMIT </button>
		</form>
		
		<img src={logo} alt="Results" id="results" width="450" height="420"></img>
        </div>
    </div>
  );
}

export default App;

