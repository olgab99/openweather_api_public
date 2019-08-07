import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Units from './components/Units.js';
import CityCountry from './components/CityCountry.js';
import styles from './components/styles.module.css';
import {fetchDataFromServer} from './components/funcs.js';
import WeatherDisplay from './components/WeatherDisplay.js';
import CityInput from './components/CityInput.js'

const SERVER_URL = 'http://127.0.0.1:5000/api/';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      units: 'metric',
      screen: 'country-city',
      weather: [],
      city: '',
      cityId: 0,
      country: '',
      country_code: '',
      loading: false
    };
    this.onChangeUnits = this.onChangeUnits.bind(this);
    this.onShowWeather = this.onShowWeather.bind(this);
    this.populateWeather = this.populateWeather.bind(this);
    this.onCityInput = this.onCityInput.bind(this);
  }

  onChangeUnits(un) {   
    this.setState({
      units: un,
      loading: true
    }, () => {
         //re-populate weather 
        //either by country/city or city name   
        const url = SERVER_URL + 'weather?units=' + un;     
        if(this.state.cityId > 0 && this.state.country_code !== ''){
          fetchDataFromServer(url + '&id=' + this.state.cityId, this.populateWeather, this.state.country, this.state.city);     
        }
        else if(this.state.city !== ''){
          fetchDataFromServer(url + '&city=' + this.state.city, this.populateWeather, this.state.country, this.state.city);  
        }
    });   
  }
  
  populateWeather(data, country, city) {
    this.setState({
      weather: data,
      country: country,
      city: city,
      loading: false
    });    
    
  }

  onCityInput(city) {     
    this.setState({
      city: city,
      cityId: 0,
      country: '',
      country_code: ''
    });
    const url = SERVER_URL + 'weather?city=' + city + '&units=' + this.state.units;
    fetchDataFromServer(url, this.populateWeather, '', city);      
  }

  onShowWeather(params, country, city) {    
    const url = SERVER_URL + 'weather?' + params + '&units=' + this.state.units;
    fetchDataFromServer(url, this.populateWeather, country, city);      
  }

  render() {   
    return (
      <div className="App">  
        <h1>Weather App</h1>  
        <div className={styles.topDiv}>
          <Units 
            units={this.state.units}
            onUnitsChange = {this.onChangeUnits}
          />  
          <div>
          <div className={styles.selectBox}>
          <CityCountry 
            onShowWeather={this.onShowWeather}
            />
          </div>
          </div>
          <div className={styles.selectBox}>
            <CityInput
              onCityInput={this.onCityInput}
              city={''}
              />
          </div>
          <div className={styles.divider}></div>
        </div>         
        <div className={styles.weatherDisplay}>
          <WeatherDisplay
            entries={this.state.weather}
            city={this.state.city}
            country={this.state.country}
            loading={this.state.loading}
            />
        </div>        
      </div>
    );
  }
}

export default App;
