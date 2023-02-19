import React from "react";
import Select from "react-select";
import '../App.css'

const MarketSelection = ({ setMarket }) => {
  const options = [
    { value: "USA", label: "USA" },
    { value: "Russia", label: "Russia" },
    { value: "India", label: "India" },
    { value: "Canada", label: "Canada" },
  ];

  var getOptions = async (e) => {
    var val = await e.slice(-1)[0].value;
    await setMarket((prev) => {
      return [...prev, val];
    });
  };

  return (
    <>
      <Select
        id="market"
        isMulti
        name="colors"
        options={options}
        closeMenuOnSelect={false}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={getOptions}
      />
    </>
  );
};

export default MarketSelection;
