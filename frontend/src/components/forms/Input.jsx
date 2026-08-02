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


    return (

        <div className={`form-group ${className}`}>


            {
                label && (

                    <label htmlFor={id || name}>

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

                id={id || name}

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