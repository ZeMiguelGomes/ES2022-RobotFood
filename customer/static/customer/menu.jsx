//import React from 'react';
//import ReactDOM from 'react-dom';
//import {Container, Row,Table, Button } from 'reactstrap';
//import 'bootstrap/dist/css/bootstrap.css';



class MyPage extends React.Component {
  constructor(props) {
      super(props)
      this.state = {
          items: [],
          alertMessage: "",
      }
      this.textreference = React.createRef();
      this.setAlertMessage = this.setAlertMessage.bind(this);
      
  }

  updateState() {
    fetch('/customer/menu/')
        .then(res => res.json())
        .then((data) => {
          this.setState({
            items: data
          })
        })
        .catch(error => this.setAlertMessage(error.message));
  }

  componentDidMount() {
    this.updateState();
  }

  setAlertMessage(message) {
      this.setState({ alertMessage: message });
  }

  render() {
      return (
<<<<<<< Updated upstream
          <div>
            <Alert message={this.state.alertMessage} />
            <table>
              <tbody>
                {!this.state.items || this.state.items.length <= 0 ? (
                <tr>
                  <td colSpan="6" align="center">
                  <b>Ops, no food here yet</b>
                  </td>
                </tr>) : 
                (
                  this.state.items.map(item => (
                    <tr colSpan="6" align="center" key={item.food_id.N}>
                      <td>{item.name.S}</td>
                      <td>{item.description.S}</td>
                      <td>{item.calories.N}</td>
                      <td>{item.price.N}</td>
                    </tr>)
                    
                  )
                  )
                  }
              </tbody>
            </table>
        </div>
=======
            <Reactstrap.Container style={{ marginTop: "20px" }}>
              <Alert message={this.state.alertMessage} />
              <Reactstrap.Table dark>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Calories</th>
                    <th>Price</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {!this.state.items || this.state.items.length <= 0 ? (
                  <tr>
                    <td colSpan="6" align="center">
                    <b>Ops, no food here yet</b>
                    </td>
                  </tr>) : 
                  (
                    this.state.items.map(item => (
                      <tr colSpan="6" align="center" key={item.food_id}>
                        <td>{item.name}</td>
                        <td>{item.description}</td>
                        <td>{item.calories}</td>
                        <td>{item.price}</td>
                      </tr>)
                    )
                  )}
                </tbody>
              </Reactstrap.Table>            
          </Reactstrap.Container>
>>>>>>> Stashed changes
      );
  }

  

}

class Alert extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    if (!this.props.message) return "";
    return <div id="alert">{this.props.message}</div>;
  }
}


ReactDOM.render(<MyPage/>, document.getElementById('reacthere'))