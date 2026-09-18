import { useId } from "react";

import "./Input.css";


export default function Input({

    label,

    type = "text",

    value,

    onChange,

    placeholder = "",

    name,

    id,

    required = false,

    disabled = false,

    error = "",

    min,

    max,

    step,

    className = ""

}) {

    const generatedId = useId();
    const inputId = id || name || generatedId;


    return (

        <div className={`form-group ${className}`}>


            {
                label && (

                    <label htmlFor={inputId}>

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



            <input

                id={inputId}

                name={name}

                type={type}

                value={value}

                onChange={onChange}

                placeholder={placeholder}

                disabled={disabled}

                required={required}

                min={min}

                max={max}

                step={step}

                className={
                    error
                        ? "input-error"
                        : ""
                }

            />



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
