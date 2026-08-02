import "./DashboardSkeleton.css";



export default function DashboardSkeleton() {


    return (

        <div className="dashboard-skeleton">


            <div className="skeleton-header">

                <div className="skeleton-line title"></div>

                <div className="skeleton-line subtitle"></div>

            </div>



            <div className="skeleton-cards">

                {
                    Array.from({
                        length: 6
                    }).map((_, i) => (

                        <div
                            key={i}
                            className="skeleton-card"
                        />

                    ))
                }

            </div>




            <div className="skeleton-sections">

                {
                    Array.from({
                        length: 4
                    }).map((_, i) => (

                        <div
                            key={i}
                            className="skeleton-box"
                        />

                    ))
                }

            </div>



        </div>

    );

}