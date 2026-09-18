import { useId } from "react";

import "./Textarea.css";


export default function Textarea({

    label,

    value,

    onChange,

    placeholder = "",

    name,

    id,

    rows = 4,

    required = false,

    disabled = false,

    error = "",

    className = ""

}) {

    const generatedId = useId();
    const textareaId = id || name || generatedId;


    return (

        <div className={`form-group ${className}`}>


            {
                label && (

                    <label htmlFor={textareaId}>

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



            <textarea

                id={textareaId}

                name={name}

                value={value}

                onChange={onChange}

                placeholder={placeholder}

                rows={rows}

                disabled={disabled}

                required={required}

                className={
                    error
                        ? "textarea-error"
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
