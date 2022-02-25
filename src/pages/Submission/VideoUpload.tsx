import React from 'react';
import './VideoUpload.css';
import banner from '../../util/banner.jpeg';

import {Link } from "react-router-dom";


class VideoUpload extends React.Component<{}, { value: string }>  {

  constructor(props : any) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event : any) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event : any) {
    alert('Form was submitted');
    event.preventDefault();
  }
  
  render() {

  return (
    <div id="c">
    	<div id="header">
        	<img src={banner} alt="McDowell Sonoran Conversancy" id="banner" width="100%" height ="220px"></img><br />
        	<div id="links2">
        	<Link to="/">Home Page</Link>
        	<Link to="/submission"> Upload Video </Link>
        	<Link to="/email-results"> Get Email Results </Link>
        	<Link to="/"> Previous Results </Link>
        	<a href="https://www.mcdowellsonoran.org/">Conservancy Home</a>
        	</div>
        </div><br /><br />
        
		<div id="wrapper2">
        	<div id="main2">
        		<form onSubmit={this.handleSubmit}>
        			<label>Date recorded</label> <input type="date" id="filedate"></input><br />
        			<label>Time start</label> <input type="text"></input>
        			<label>Time stop</label> <input type="text"></input><br /><br />
        			<label>Time sunset</label> <input type="text"></input><br />
        			<label>Time total</label> <input type="text"></input><br />	<br />
        			
        			<label>New Moon</label> <input type="date" id="filedate"></input><br /> 
        			<label>Days from New Moon</label><input type="number" id="days_nm" min="-10" max="10"></input><br /><br />
        			
        			<label>Expert</label> 
        				<select name="expert">
        					<option value="Debbie Lagenfeld">Debbie Lagenfeld</option>
        					<option value="Marianne Moore">Marianne Moore, ASU</option>
        					<option value="Tiffany Sprague">Tiffany Sprague</option>
        					<option value="other">Other</option>
        				</select><br />
        			
        			<label>Recorder</label> <input type="text" id="longtext"></input><br />
        			<label>Observers</label> <input type="text" id="longtext"></input><br /><br />
        			
        			<label>Equipment</label><br />
        				 <input type="checkbox" id="IR video camera" defaultChecked></input>
        				 <h5>2 IR video camera</h5><br />
        				 <input type="checkbox" id="IR lights" defaultChecked></input>
        				 <h5>2 large IR lights</h5><br />
        				 <input type="checkbox" id="acoustic recorder" defaultChecked></input>
        				 <h5>acoustic recorder</h5><br /> 
        				 <input type="checkbox" id="battery pack" defaultChecked></input>
        				 <h5>12V battery pack with power cords and mini USB ports</h5><br /><br />
        				 
    
        			<label>Temp. sunset (C)</label><input type="text"></input><br />
        			<label>Temp. end</label><input type="text"></input><br /><br />
        			<label>Relative humidity sunset (%)</label><input type="number" min="0" max="100"></input><br />
        			<label>Relative humidity end</label><input type="number" min="0" max="100"></input><br /><br />
        			<label>Cloud cover sunset ( /3)</label><input type="number" defaultValue="0" min="0" max="3"></input><br />
        			<label>Cloud cover end</label><input type="number" defaultValue="0" min="0" max="3"></input><br /><br />
        			
        			<label>Precipitation sunset</label>
        				<select name="precip_sunset">
        					<option value="none">None</option>
        					<option value="fog">Fog</option>
        					<option value="light rain">Light rain</option>
        					<option value="hard rain">Hard rain</option>
        					<option value="hail">Hail</option>
        					<option value="snow">Snow</option>
        					<option value="past">In past 24 hours</option>
        				</select><br />
        			<label>Precipitation end</label>        				
        			<select name="precip_end">
        					<option value="none">None</option>
        					<option value="fog">Fog</option>
        					<option value="light rain">Light rain</option>
        					<option value="hard rain">Hard rain</option>
        					<option value="hail">Hail</option>
        					<option value="snow">Snow</option>
        					<option value="past">In past 24 hours</option>
        				</select><br /><br />
        			
        			<label>Wind sunset (km/hr)</label><input type="text" defaultValue="0.0"></input><br />
        			<label>Wind end</label><input type="text" defaultValue="0.0"></input><br /><br />
        			
        			<label>Battery start</label><input type="number" defaultValue="100" min="0" max="100"></input><br />
        			<label>Battery end</label><input type="number" min="0" max="100"></input><br /><br />
        			
        			<label>1st sight</label><input type="text"></input><br />
        			<label>Bats seen</label><input type="number" min="0" max="100"></input><br /><br /><br />
        				 
        			<h3>Camera 1 Video</h3>
        			<label>Choose file #1</label><input type="file" id="filename"></input><br /><br />
				<label>Choose file #2</label><input type="file" id="filename"></input><br /><br />
        			<h3>Camera 2 Video</h3>
        			<label>Choose file #1</label><input type="file" id="filename"></input><br /><br />
				<label>Choose file #2</label><input type="file" id="filename"></input><br /><br />
        			
        			
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
