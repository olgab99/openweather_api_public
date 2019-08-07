import React from 'react';
import ReactDOM from 'react-dom';
import styles from './styles.module.css';

const Units = (props) => {     
        return (
        <div className={styles.units} onChange={event => props.onUnitsChange(event.target.value)}>
            <h3>Units</h3>
            <div >
                <label>
                <input type="radio" id="metric" name="units" value="metric" 
                    defaultChecked={props.units==='metric'? true: false} />
                Metric</label>
            </div>
            <div>
                <label>
                <input type="radio" id="imperial" name="units" 
                    value="imperial" defaultChecked={props.units==='metric'? false : true} />
                Imperial</label>
            </div>
        </div>
        );     
}

export default Units;