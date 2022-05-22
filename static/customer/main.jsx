//import React from 'react';
//import ReactDOM from 'react-dom';
//import {Container, Row,Table, Button } from 'reactstrap';
//import 'bootstrap/dist/css/bootstrap.css';

class MyPage extends React.Component {

  Client() {
    window.location.replace('/customer/')
  }

  kitchenStaff(){
    window.location.replace('/kitchen/')
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
            </div>
          </div> 
          </div>                  
      );
  }
}



ReactDOM.render(<MyPage/>, document.getElementById('reacthere'))