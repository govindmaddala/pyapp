import React from "react";
import Select from "react-select";
import '../App.css'

const ProductNameSelection = ({ setProductName }) => {
  const options = [
    { value: "para", label: "para" },
    { value: "omez", label: "omez" },
    { value: "Nise", label: "Nise" },
    { value: "Razo", label: "Razo" },
  ];

  var getOptions = async (e) => {
    var val = await e.slice(-1)[0].value;
    await setProductName((prev) => {
      return [...prev, val];
    });
  };
  return (
    <>
      <Select
      id="productName"
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

export default ProductNameSelection;
