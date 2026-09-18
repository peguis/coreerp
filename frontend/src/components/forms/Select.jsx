import { useId } from "react";

import "./Select.css";


export default function Select({

    label,

    value,

    onChange,

    options = [],

    placeholder = "Selecione",

    name,

    id,

    required = false,

    disabled = false,

    error = "",

    className = ""

}) {

    const generatedId = useId();
    const selectId = id || name || generatedId;


    return (

        <div className={`form-group ${className}`}>


            {
                label && (

                    <label htmlFor={selectId}>

                        {label}


                        {
                            required && (

                                <span className="required">

                                    *

                                </span>

                            )
                        }


                    </label>

                )
            }





            <select

                id={selectId}

                name={name}

                value={value}

                onChange={onChange}

                disabled={disabled}

                required={required}

                className={

                    error

                        ? "select-error"

                        : ""

                }

            >



                <option value="">

                    {placeholder}

                </option>





                {

                    options.map((option) => (


                        <option

                            key={option.value}

                            value={option.value}

                        >

                            {option.label}


                        </option>


                    ))

                }



            </select>







            {

                error && (


                    <span className="field-error">


                        {error}


                    </span>


                )

            }



        </div>

    );

}
