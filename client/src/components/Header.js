import React from 'react';
import {useState, useEffect} from 'react';
import Toggle from 'react-toggle';
import { FaSun, FaMoon } from 'react-icons/fa';
import Switch from 'react-switch';
import { IoSunnySharp } from "react-icons/io5";
import DarkModeToggle from './DarkModeToggle';
function Header() {
        // State to track the current mode (dark or light)
        return (
          <div className="header">
            
          
          <div className="buttons-container">
            {/* <button className="button analytics">Advanced Analytics</button> 
            */}
            <h1 >Anomaly Finder</h1>
          </div>
          <div>
            <DarkModeToggle />
          </div>
        </div>
        )
      };
    
export default Header
