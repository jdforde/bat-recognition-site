import React from 'react';
import logo from './logo.svg';
import './App.css';

//Design from last year's students
const App = () => {
  return (
    <div className ="background1">
        <div className="maincontainer">
          <div className="w3-animate-right fixspeed textportion">
              <h1>Bat Recognition Engine</h1>
              <div>
                  <input type="file" name="video" className = "filepond"/>
              </div>
              <form method = "POST" action = "/submit/">
                  <input type="submit" className="btn btn-primary"/>
              </form>
          </div>
        </div>
    </div>
  );
}

export default App;
