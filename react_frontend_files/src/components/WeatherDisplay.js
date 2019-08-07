import React from 'react';
import LoadingOverlay from 'react-loading-overlay';
import styles from './styles.module.css';

const WeatherFields = (props) => {
    return (
        <div>            
        {props.records.map((record, index) => 
            <div className={styles.padLeft} key={index}>
            <span className={styles.titleTxt}>{record.title}</span>
        : {record.value}<br /></div>
            )}
        </div>
        
    );
};

const WeatherDisplay = (props) => {
    return(
        <div>
            <LoadingOverlay
                    active={props.loading}
                    spinner
                    text='Loading'
                    >
            <div>
            <span className={styles.titleTxt}>City: {props.city}</span><br />
            <span className={styles.titleTxt}>Country: {props.country}</span>
            </div>
        {props.entries.map((record, index) => 
            <div key={index}>
                <h4>{record.category_title}</h4>
                <WeatherFields
                    records={record.data}
                    />  
            </div>       
        )}
        </LoadingOverlay>      
        </div>
    );

};

export default WeatherDisplay;