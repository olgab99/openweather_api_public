import React from 'react'
import styles from './styles.module.css';

class CityInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: props.city      
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {    
    event.preventDefault();
    this.props.onCityInput(this.state.value);
  }

    render() {
      return(
        <form onSubmit={this.handleSubmit}>
        <label>
          City Name:
          <input type="text" value={this.state.value} onChange={this.handleChange} className={styles.input}/>
        </label>
        <input type="submit" value="Get Weather" className={styles.button} />
      </form>
      )
    }
}

export default CityInput;