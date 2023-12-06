import React, {useState, useEffect} from 'react';
import Plot from 'react-plotly.js';
import { useMediaQuery } from "react-responsive";
import Toggle from "react-toggle";
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import PlotsnGraphs from './components/PlotsnGraphs';
import MakePredictions from './components/MakePredictions';
import ScrollAndLoad from './ScrollAndLoad';
import axios from 'axios';
import { Table } from 'react-bootstrap';


function App() {

  const [isLoading, setIsLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);
  const [probabilities, setProbabilities] = useState([]);
  const [actualLabels, setActualLabels] = useState([]);
  const [accuracy, setAccuracy] = useState(null);
  const [attack, setAttack] = useState([]);
  const delay = 2000;

  const handlePredict = async () => {
    try {
      const response = await axios.get('/predict', {
      timeout: 9000, // Set the timeout in milliseconds (adjust as needed)
    });

      setPredictions(response.data.prediction);
      setAttack(response.data.attack_name);
      setProbabilities(response.data.probability);
      setActualLabels(response.data.actual);
      setAccuracy(response.data.accuracy);
      console.log(accuracy);
      console.log(response);
    } catch (error) {
      console.error('Error predicting:', error);
    }
  };

  const handleScrollAndLoad = () => {
    handlePredict();
    // Show loading icon
    setIsLoading(true);

    // Scroll to the bottom
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth',
    });

    // Simulate loading delay (replace this with your actual loading logic)
    setTimeout(() => {
      // Hide loading icon after the loading is done
      setIsLoading(false);
    }, 2000); // Adjust the time as needed
    
  };

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div className='content'>
      <div>
        <Header />
      </div>
      <div>
        <Dashboard />
      </div>
      
      <div>
        <button className="button predictions" onClick={handleScrollAndLoad}>Make Predictions</button>
        <div className="TableContainer">
          <h3 className='headerPreds'>Predictions:</h3>
          <Table>
            <thead>
              <tr>
                <th>#</th>
                <th>Prediction</th>
                <th>Probability</th>
                <th>Actual</th>
              </tr>
            </thead>
            <tbody>
              {(predictions ?? []).map((prediction, index) => (
                <tr key={index} className={prediction === 0 ? 'prediction-green' : 'prediction-red'}>
                  <td>{index + 1}</td>
                  <td>{prediction}</td>
                  <td>{probabilities[index]}</td>
                  <td>{actualLabels[index]}</td>
                </tr>
              ))}
            </tbody>
          </Table>
          
          <p className="AccuracyParagraph">Accuracy: {accuracy}</p>
        </div>
      </div>
    </div>
  );
};

export default App;
