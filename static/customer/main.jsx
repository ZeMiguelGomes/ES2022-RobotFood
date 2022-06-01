//import React from 'react';
//import ReactDOM from 'react-dom';
const { Table, Form,FormGroup, Label, Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } = Reactstrap;
//import 'bootstrap/dist/css/bootstrap.css';

class MyPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      locationTag: "",
  }
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  Client() {
    window.location.replace('/customer/')
  }

  kitchenStaff(){
    window.location.replace('/kitchen/')
  }

  handleInputChange(event) {
    event.preventDefault();
    const target = event.target;
    let name = target.name;
    let value = target.value;
    this.setState({
        [name]: value
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    // Reset the alert to empty
    
    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            locationTag: this.state.locationTag
        })
    };
    fetch('/retrieveorder/', requestOptions)
        .then(response => response.json()
        .then(data => {
          this.setState({ price: data });
          console.log(data)
        })
        );
  }

  render() {
      return (
        <div>
          <div className="Main">
            <h2>Welcome to our Robot restaurant</h2>
            <h5>Chose your profile</h5>
            <div class="row">
            <div class="d-flex justify-content-around">
              <button id="btnClient" class="btn btn-primary btn-lg center-block" onClick={this.Client} >Client</button>
              <button id="btnKitchen" class="btn btn-secondary btn-lg center-block" onClick={this.kitchenStaff} >Kitchen Staff</button>
            </div>
            <br /><br />
            <h6>Retrieve your order</h6>
            <Form className="form" onSubmit={this.handleSubmit}>
            <Label>
            Location tag:
            <Input  type="number" 
                    min="0" 
                    name="locationTag" 
                    value={this.state.locationTag} 
                    onChange={(e) => {this.handleInputChange(e);}}
            />
            </Label>
            <Button as="input" type="submit" variant="primary" data-toggle="modal" data-target="#exampleModal"> Submit</Button>
            </Form>

            </div>
          </div> 
          </div>                  
      );
  }
}



ReactDOM.render(<MyPage/>, document.getElementById('reacthere'))