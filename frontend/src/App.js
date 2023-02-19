import React, { useEffect, useState } from 'react';
import DjangoCSRFToken from 'django-react-csrftoken'
import axios from 'axios'
import Cookies from 'js-cookie';
import BatchSelection from './components/BatchSelection'
import MarketSelection from './components/MarketSelection';
import NameSelection from './components/NameSelection';
import ProductNameSelection from './components/ProductNameSelection';
import SpecificationSelection from './components/SpecificationIdSelection.jsx'
import './App.css'

function App() {
  const [batch, setBatch] = useState([])
  const [market, setMarket] = useState([])
  const [names, setNames] = useState([])
  const [productName, setProductName] = useState([])
  const [specificationID, setSpecificationID] = useState([])

  var optionsData = {
    "names": names,
    "market": market,
    "batch": batch,
    "productName": productName,
    "specificationID": specificationID
  }

  useEffect(() => {
    axios.get('setCookie/')
  }, [])

  const handleSubmit = (event) => {
    const csrftoken = Cookies.get('csrftoken');
    event.preventDefault();
    console.log(optionsData);
    if (names.length !== 0 && market.length !== 0 && batch.length !== 0 && productName.length !== 0 && specificationID.length !== 0) {
      fetch('getDataImage/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(optionsData)
      }).then((resp) => {
        resp.json();
      }).then((resp) => { console.log(resp); })
    } else {
      alert('Atleast one value should be selected for each selection')
    }
  };

  return (
    <>
      <h1 id='heading'>Data Analaysis</h1>
      <form method="post" onSubmit={handleSubmit} id='formData'>
        <DjangoCSRFToken />
        <label htmlFor="batch">Batch No.</label>
        <BatchSelection setBatch={setBatch} />
        <label htmlFor="">Market</label>
        <MarketSelection setMarket={setMarket} />
        <label htmlFor="">Name</label>
        <NameSelection setNames={setNames} />
        <label htmlFor="">Product Name</label>
        <ProductNameSelection setProductName={setProductName} />
        <label htmlFor="">Specification ID: </label>
        <SpecificationSelection setSpecificationID={setSpecificationID} />
        <button id='submitButton'>Get Analysis Plot</button>
      </form>
      <button id='resetButton' onClick={() => { document.location.reload() }}>Reset</button>
    </>
  );
}

export default App;
