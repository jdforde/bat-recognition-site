import React from 'react';
import './VideoUpload.css';
import banner from '../../util/banner.jpeg';

import {Link } from "react-router-dom";


class VideoUpload extends React.Component {

  constructor(props : any) {
    super(props);
    this.state = {
    	rec_date: '', 
    	start_time: '',
    	stop_time: '',
    	sunset: '',
    	total_time: '',
    	new_moon: '',
    	days_from_nm: '',
    	expert: 'Debbie Lagenfeld',
    	recorder: '',
    	observers: '',
    	equipment: '',
    	temp_ss: '',
    	temp_end: '',
    	rel_humidity_ss: '',
    	rel_humidity_end: '',
    	cloud_cover_ss: '',
    	cloud_cover_end: '',
    	precip_ss: '',
    	precip_end: '',
    	wind_ss: '',
    	wind_end: '',
    	battery_start: '',
    	battery_end: '',
    	first_sight: '',
    	bats_seen: ''    	
    };

	this.handleChange = this.handleChange.bind(this);
    this.handleFile = this.handleFile.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  
  handleChange(event : any) {
		this.setState({[event.target.id] : event.target.value});
		console.log(event.target.id + " was set to " + event.target.value);
  }

  async handleFile(event : any) {
    const data = new FormData();
	data.append('file', event.target.files![0]);
    
	await fetch("http://localhost:5000/upload", {
	    method: 'POST',
        body: data
    }).then(res => {
        console.log(res);
	    console.log(res.status)
    });
    
    console.log("new file handled");
  }
  

  async handleSubmit(event : any) {
    event.preventDefault();
    alert('Form was submitted');
  }
  
  
  render() {

  return (
    <div id="c">
    	<div id="header">
        	<img src={banner} alt="McDowell Sonoran Conversancy" id="banner" width="100%" height ="220px"></img><br />
        	<div id="links2">
        	<Link to="/submission"> Upload Video </Link>
        	<Link to="/email-results"> Get Email Results </Link>
        	<Link to="/"> Previous Results </Link>
        	<a href="https://www.mcdowellsonoran.org/">Conservancy Home</a>
        	</div>
        </div><br /><br />
        
		<div id="wrapper2">
        	<div id="main2">
        		<form onSubmit={this.handleSubmit}>
        		    <h3><b>Camera 1 Video</b></h3>
        		<input onChange={this.handleFile} type="file" id="filename1"></input><br /><br />
				<input onChange={this.handleFile} type="file" id="filename2"></input><br /><br />
				
        			<h3><b>Camera 2 Video</b></h3>
        		<input onChange={this.handleFile} type="file" id="filename3"></input><br /><br />
				<input onChange={this.handleFile} type="file" id="filename4"></input><br /><br />
        		
        			<label>Date recorded</label> <input type="date" id="rec_date" onChange={this.handleChange}></input><br />
        			<label>Time start</label> <input type="time" id="start_time" onChange={this.handleChange}></input><br />
        			<label>Time stop</label> <input type="time" id="stop_time" onChange={this.handleChange}></input><br /><br />
        			<label>Time sunset</label> <input type="time" id="sunset" onChange={this.handleChange}></input><br />
        			<label>Time total</label> <input type="time" id="total_time" onChange={this.handleChange}></input><br />	<br />
        			
        			<label>New Moon</label> <input type="date" id="new_moon" onChange={this.handleChange}></input><br /> 
        			<label>Days from New Moon</label><input type="number" min="-10" max="10" id="days_from_nm" onChange={this.handleChange}></input><br /><br />
        			
        			<label>Expert</label> 
        				<select name="expert" id="expert" onChange={this.handleChange}>
        					<option value="Debbie Lagenfeld">Debbie Lagenfeld</option>
        					<option value="Marianne Moore">Marianne Moore, ASU</option>
        					<option value="Tiffany Sprague">Tiffany Sprague</option>
        					<option value="other">Other</option>
        				</select><br />
        			
        			<label>Recorder</label> <input type="text" className="longtext" id="recorder" onChange={this.handleChange}></input><br />
        			<label>Observers</label> <input type="text" className="longtext" id="observers" onChange={this.handleChange} ></input><br /><br />
        			
        			<label>Equipment</label><br />
        				 <input type="checkbox" id="IR video camera" defaultChecked></input>
        				 <h5>2 IR video camera</h5><br />
        				 <input type="checkbox" id="IR lights" defaultChecked></input>
        				 <h5>2 large IR lights</h5><br />
        				 <input type="checkbox" id="acoustic recorder" defaultChecked></input>
        				 <h5>acoustic recorder</h5><br /> 
        				 <input type="checkbox" id="battery pack" defaultChecked></input>
        				 <h5>12V battery pack with power cords and mini USB ports</h5><br /><br />
        				 
    
        			<label>Temp. sunset (C)</label><input type="text" id="temp_ss" onChange={this.handleChange}></input><br />
        			<label>Temp. end</label><input type="text" id="temp_end" onChange={this.handleChange}></input><br /><br />
        			<label>Relative humidity sunset (%)</label><input type="number" min="0" max="100" id="rel_humidity_ss" onChange={this.handleChange}></input><br />
        			<label>Relative humidity end</label><input type="number" min="0" max="100" id="rel_humidity_end" onChange={this.handleChange}></input><br /><br />
        			<label>Cloud cover sunset ( /3)</label><input type="number" defaultValue="0" min="0" max="3" id="cloud_cover_ss" onChange={this.handleChange}></input><br />
        			<label>Cloud cover end</label><input type="number" defaultValue="0" min="0" max="3" id="cloud_cover_end" onChange={this.handleChange}></input><br /><br />
        			
        			<label>Precipitation sunset</label>
        				<select name="precip_sunset" id="precip_ss" onChange={this.handleChange}>
        					<option value="none">None</option>
        					<option value="fog">Fog</option>
        					<option value="light rain">Light rain</option>
        					<option value="hard rain">Hard rain</option>
        					<option value="hail">Hail</option>
        					<option value="snow">Snow</option>
        					<option value="past">In past 24 hours</option>
        				</select><br />
        			<label>Precipitation end</label>        				
        			<select name="precip_end" id="precip_end" onChange={this.handleChange}>
        					<option value="none">None</option>
        					<option value="fog">Fog</option>
        					<option value="light rain">Light rain</option>
        					<option value="hard rain">Hard rain</option>
        					<option value="hail">Hail</option>
        					<option value="snow">Snow</option>
        					<option value="past">In past 24 hours</option>
        				</select><br /><br />
        			
        			<label>Wind sunset (km/hr)</label><input type="text" defaultValue="0.0" id="wind_ss" onChange={this.handleChange}></input><br />
        			<label>Wind end</label><input type="text" defaultValue="0.0" id="wind_end" onChange={this.handleChange}></input><br /><br />
        			
        			<label>Battery start</label><input type="number" defaultValue="100" min="0" max="100" id="battery_start" onChange={this.handleChange}></input><br />
        			<label>Battery end</label><input type="number" min="0" max="100" id="battery_end" onChange={this.handleChange}></input><br /><br />
        			
        			<label>1st sight</label><input type="time" id="first_sight" onChange={this.handleChange}></input><br />
        			<label>Number of bats seen</label><input type="number" min="0" max="100" id="bats_seen" onChange={this.handleChange}></input><br />
        			
        			
        			<br /><br /><button type="submit"> Process Video(s) </button>
				</form>
			</div>
        </div>
        <br /><br />
    </div>
  );
  
  }
  
}

export default VideoUpload;
