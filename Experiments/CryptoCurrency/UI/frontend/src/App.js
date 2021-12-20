import React, { Component } from 'react';
import './App.css';
import Status from './components/status'
import Send from './components/send'
import Transactions from './components/transactions'
import axios from 'axios';

const endpoint = 'http://127.0.0.1:4041/block'
class App extends Component {
  constructor(props){
    super(props);
  }
  componentWillMount() {
    axios.get(endpoint)
  }
  render(){
  return (
    <div className="App">
    <Status/>
    <Send/>
    <Transactions/>
    </div>
    );
  }
}

export default App;
