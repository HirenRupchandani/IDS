import React, {useState, useEffect} from 'react';
import Plot from 'react-plotly.js';
import { useMediaQuery } from "react-responsive";
import Toggle from "react-toggle";
import axios from 'axios';
// import 'https://cdn.plot.ly/plotly-latest.min.js';

// import Plotly from 'plotly.js';
var layout={width: 640, height: 480, title: 'Distriburion of various intrusions in the network',}
var dark_layout={width: 640, height: 480, title: 'Distriburion of various intrusions in the network', plot_bgcolor:'grey', paper_bgcolor:'#000000'}
function PlotsnGraphs() {
    const [barplot, setBarplot] = useState(0);
    const [pieplot, setPieplot] = useState(0);
    const [binarypie, setBinarypie] = useState(0);
    const [binaryBar, setBinaryBar] = useState(0);
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
      // Get the item from localStorage
      const darkMode = localStorage.getItem('darkMode');
  
      // Do something with the retrieved item
      console.log('darkMode:', darkMode);
  
      // Set dark mode state
      setIsDarkMode(darkMode === 'true');
      console.log('dark mode stats:', isDarkMode, darkMode);
    }, []); 
    
    useEffect(() => {
      fetch('https://hirenr.pythonanywhere.com/plot-bar').then(res => res.json()).then(data => {setBarplot(data);});}, []);
      // console.log(barplot)

      useEffect(() => {
      fetch('https://hirenr.pythonanywhere.com/pie-chart-data').then(res => res.json()).then(data => {setPieplot(data);});}, []);
      // console.log(pieplot)
    
      useEffect(() => {
        fetch('https://hirenr.pythonanywhere.com/pie-binary').then(res => res.json()).then(data => {setBinarypie(data);});}, []);
        // console.log(binarypie)
  
      useEffect(() => {
      fetch('https://hirenr.pythonanywhere.com/bar-binary').then(res => res.json()).then(data => {setBinaryBar(data);});}, []);

    return (
      
      <div className='content'>
      <div className="container">
      {/* {/* <div className="box"><Plot data={barplot.data} layout={isDarkMode ? {dark_layout} : {layout}} /> </div> */}
      { <div className="box"><Plot data={barplot.data} layout={{width: 640, height: 480, title: 'Distriburion of various intrusions in the network'}} /> </div> }
      <div className="box"><Plot data={pieplot.data} layout={{width: 640, height: 480, title: 'Distriburion of various intrusions in the network'}} /></div>
      </div>
      <div className="container">
      <div className="box"><Plot data={binaryBar.data} layout={{width: 640, height: 480, title: 'Comparison of Safe v/s Harmful devices in the network', template: "plotly_dark",}} /> </div>
      <div className="box"><Plot data={binarypie.data} layout={{width: 640, height: 480, title: 'Comparison of Safe v/s Harmful devices in the network', template: "plotly_dark",}} /> </div>
      </div>
      </div>
    );
}

export default PlotsnGraphs
