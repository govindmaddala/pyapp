import React from "react";
import Select from "react-select";
import '../App.css'

const SpecificationIdSelection = ({ setSpecificationID }) => {
  const options = [
    { value: "s1", label: "s1" },
    { value: "s2", label: "s2" },
    { value: "s3", label: "3s" },
    { value: "s4", label: "4s" },
  ];

  var getOptions = async (e) => {
    var val = await e.slice(-1)[0].value;
    await setSpecificationID((prev) => {
      return [...prev, val];
    });
  };
  return (
    <>
      <Select
        isMulti
        id="specificationID"
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

export default SpecificationIdSelection;
