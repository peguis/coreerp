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





            <select

                id={id || name}

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