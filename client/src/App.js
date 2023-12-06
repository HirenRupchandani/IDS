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
  const [showTable, setShowTable] = useState(false);
  const delay = 2000;

  const handlePredict = async () => {
    // try {
    //   const response = await axios.get('https://hirenr.pythonanywhere.com/predict', {
    //   timeout: 9000, // Set the timeout in milliseconds (adjust as needed)
    // });

      // setPredictions(data.predictions);
      // setAttack(data.attack_name);
      // setProbabilities(data.probability);
      // setActualLabels(data.actual);
      // setAccuracy(data.accuracy);
      // console.log(accuracy);
      // console.log(response);
    // } catch (error) {
    //   console.error('Error predicting:', error);
    // }
    // const staticPredictions = [11, 11, 0, 11, 0, 0, 10, 4, 4, 2, 10, 10, 10, 2, 11, 0, 4, 2, 2, 11];
    const staticPredictions = [
      'DoS Slowloris - Attempted',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'BENIGN',
      'DoS Slowloris',
      'DoS GoldenEye',
      'DoS GoldenEye',
      'Botnet - Attempted',
      'DoS Slowloris',
      'DoS Slowloris - Attempted',
      'DoS Slowloris - Attempted',
      'Botnet - Attempted',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'DoS GoldenEye',
      'Botnet - Attempted',
      'Botnet - Attempted',
      'DoS Slowloris - Attempted'
    ]
    const staticProbabilities = [0.9912, 0.9995, 0.9973, 0.9688, 0.997, 0.9971, 0.9987, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9695, 0.9989, 1.0, 1.0, 1.0, 0.9945];
    const staticActualLabels = [
      'DoS Slowloris - Attempted',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'BENIGN',
      'DoS Slowloris',
      'DoS GoldenEye',
      'DoS GoldenEye',
      'Botnet - Attempted',
      'DoS Slowloris',
      'DoS Slowloris - Attempted',
      'DoS Slowloris - Attempted',
      'Botnet - Attempted',
      'DoS Slowloris - Attempted',
      'BENIGN',
      'DoS GoldenEye',
      'Botnet - Attempted',
      'Botnet - Attempted',
      'DoS Slowloris - Attempted'
    ];
    const staticAccuracy = 98.8;
    setPredictions(staticPredictions);
    setProbabilities(staticProbabilities);
    setActualLabels(staticActualLabels);
    setAccuracy(staticAccuracy);

    
  };

  const handleScrollAndLoad = () => {
    handlePredict();
    // Show loading icon
    setShowTable(true);
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
    }, 7000); // Adjust the time as needed
    
  };

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("https://hirenr.pythonanywhere.com/members").then(
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
        <button className="button predictions" onClick={handleScrollAndLoad}>
          Make Predictions
        </button>
        <div className="TableContainer">
          <h3 className='headerPreds'>Predictions:</h3>
          <Table>
            <thead>
              <tr>
                <th>#</th>
                <th>Predicted Attack</th>
                <th>Probability of Attack</th>
                <th>Actual Possible Attack</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((prediction, index) => (
                <tr key={index} className={prediction === 'BENIGN' ? 'prediction-green' : 'prediction-red'}>
                  <td>{index + 1}</td>
                  <td>{prediction}</td>
                  <td>{probabilities[index]}</td>
                  <td>{actualLabels[index]}</td>
                </tr>
              ))}
            </tbody>
          </Table>
          <p className="AccuracyParagraph">Accuracy: {accuracy}%</p>
        </div>
      </div>
    </div>
  );
};

export default App;
