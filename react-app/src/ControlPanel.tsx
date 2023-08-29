import "./ControlPanel.css";

function ControlPanel() {
    return (
        <div className='control-panel'>
            <div className="severity-control">
                Slight: <input type="checkbox" id="slightCheck" /> <br/>
                Serious: <input type="checkbox" id="seriousCheck" /> <br/>
                Fatal: <input type="checkbox" id="fatalCheck" /> <br/>
            </div>

            <div className="vehicle-type-control">
                All Vehicles: <input type="checkbox" id="allvehiclesCheck" /> <br/> <br/>
                Cycles: <input type="checkbox" id="cyclesCheck" />     
                Two-wheeled motor vehicles: <input type="checkbox" id="2wheeledCheck" />    
                Cars: <input type="checkbox" id="carsCheck" />
                Buses/Coaches: <input type="checkbox" id="BusesCheck" />
                LGVs: <input type="checkbox" id="lgvsCheck" />
                HGVs: <input type="checkbox" id="hgvsCheck" />
            </div>

            <div className="year-control">
                <input type="range" min="2005" max="2022" id="slider" />
                <h1><text id="currentYear">2010</text></h1>
            </div>

        </div>
    )

    // TO DO: Column styling for div components in CSS... with background colours 
    // TO DO: OnClick event handling which calls a get data function call to API (checking what is ticked and what is not)

    
}

export default ControlPanel 