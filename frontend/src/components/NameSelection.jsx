import React from "react";
import Select from "react-select";
import '../App.css'

const NameSelection = ({ setNames }) => {
  const options = [
    { value: "a", label: "a" },
    { value: "b", label: "b" },
    { value: "c", label: "c" },
    { value: "d", label: "d" },
  ];

  var getOptions = async (e) => {
    var val = await e.slice(-1)[0].value;
    await setNames((prev) => {
      return [...prev, val];
    });
  };
  return (
    <>
      <Select
        isMulti
        id="names"
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

export default NameSelection;
