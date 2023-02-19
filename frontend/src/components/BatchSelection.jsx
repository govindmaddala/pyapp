import React from "react";
import Select from "react-select";
import '../App.css'

const BatchSelection = ({ setBatch }) => {
  const options = [
    { value: "1", label: "1" },
    { value: "2", label: "2" },
    { value: "3", label: "3" },
    { value: "4", label: "4" },
    { value: "5", label: "5" },
  ];

  var getOptions = async (e) => {
    var val = await e.slice(-1)[0].value;
    await setBatch((prev) => {
      return [...prev, val];
    });
  };
  return (
    <>
      <Select
        id="batch"
        styles={{ display: "inline" }}
        isMulti
        name="batch"
        options={options}
        closeMenuOnSelect={false}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={getOptions}
      />
    </>
  );
};

export default BatchSelection;
