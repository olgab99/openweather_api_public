import React from 'react';
import LoadingOverlay from 'react-loading-overlay';
import styles from './styles.module.css';
import {fetchDataFromServer} from './funcs.js'

const SERVER_URL = 'http://127.0.0.1:5000/api/';

class CityCountry extends React.Component {
    constructor(props) {
        super(props);
        this.showWeather = props.onShowWeather;
        this.state = {
            countries: [],
            cities: [],
            country: '',
            countryCode: 'default',
            city: '',
            cityId: 0,
            loading: true
        }
      
        this.populateCountries = this.populateCountries.bind(this);       
        this.getCities = this.getCities.bind(this);
        this.populateCities = this.populateCities.bind(this);
        this.fetchData = this.fetchData.bind(this);
        this.onSelectChange = this.onSelectChange.bind(this);
    }

    componentDidMount() {
        this.fetchData('countries', this.populateCountries);        

    }

    populateCountries(countries){
        this.setState({
            countries: countries,
            country: '',
            countryCode: 'default',
            loading: false
        });
    }

    getCities(countryCode) {
        this.setState({
            loading: true
        }, () => {
            this.fetchData('cities?country=' + countryCode, this.populateCities);
        })
        
    }
    populateCities(cities) {
        this.setState({
            cities: cities,
            city: '',
            cityId: 0,
            loading: false
        })
    }

    fetchData(postfix, callback){
        const url = SERVER_URL + postfix;
        fetchDataFromServer(url, callback);        
    }

  
    onSelectChange(e) {
        var id = e.nativeEvent.target.selectedIndex;
        var txt = e.nativeEvent.target[id].text;
        var val = e.target.value;       
        if(e.target.name === 'countrySelect'){
            this.setState({
                country: txt,
                countryCode: val,
                cityId: 0,
                city: ''
    
            });        
            this.getCities(val);
        }
        else{
            this.setState({
                city: txt,
                cityId: val
            });
            this.showWeather('id=' + val, this.state.country, txt);
        }
    }

    render() {
        return (
            <div>   
                <LoadingOverlay
                    active={this.state.loading}
                    spinner
                    text='Loading'
                    >
                <select value={this.state.countryCode} placeholder={'Select country'}
                    className={styles.selectCtrl} name="countrySelect"
                    onChange={(e) => this.onSelectChange(e)}>
                        <option value={'default'} disabled>Select Country</option> 
                
                {this.state.countries.map((country) => 
                    <option key={country.code} value={country.code}>{country.country}</option>)}
                </select>
           
                <select value={this.state.cityId} className={styles.selectCtrl}
                    name="citySelect"
                    onChange={(e) => this.onSelectChange(e)}>
                <option value={0} disabled selected>Select City</option>
                {this.state.cities.map((city) => 
                    <option key={city.id} value={city.id}>{city.city}</option>)}
                </select>
                </LoadingOverlay>             
        </div>
        )
    }
}

export default CityCountry
