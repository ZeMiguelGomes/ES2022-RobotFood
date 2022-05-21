//import React from 'react';
//import ReactDOM from 'react-dom';
//import {Container, Row,Table, Button } from 'reactstrap';
//import 'bootstrap/dist/css/bootstrap.css';
class MyPage extends React.Component {
  constructor(props) {
      super(props)
      this.state = {
          items: [],
          selectedCategory: "Appetizer",
          order: [],
          locationTag: "",
          price: "",
          alertMessage: "",
      }
      this.textreference = React.createRef();
      this.setCategory = this.setCategory.bind(this);
      this.addItem = this.addItem.bind(this);
      this.removeItem = this.removeItem.bind(this);
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
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
    console.log("updateState");
  }

  setAlertMessage(message) {
      this.setState({ alertMessage: message });
  }

  setCategory(category) {
    this.setState({selectedCategory: category});
  }

  addItem(item) {
    let array = this.state.order;
    let name = item.name.S;
    let price = item.price.N;
    let newItem = {name, price};
    array.push(newItem);
    this.setState({order: array});
    console.log(this.state.order);
  }

  removeItem(item) {
    let array = this.state.order;

    let index = array.indexOf(item);
    if (index !== -1) {
      array.splice(index, 1);
    }

    this.setState({order: array});
    console.log(this.state.order);
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
    this.setAlertMessage();
    
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            order: this.state.order,
        })
    };
    fetch('/customer/orderprice/', requestOptions)
        .then(response => response.json()
        .then(data => {
          this.setState({ price: data.price });
          console.log(data)
        })
        ).catch(error => this.setAlertMessage(error.message));
  }

  render() {
    return (
      <div>
        <h3>Menu</h3>
        <Reactstrap.ListGroup>
          <Reactstrap.ListGroupItem tag="button" onClick={() => this.setCategory("Appetizer")} action>Appetizers</Reactstrap.ListGroupItem>
          <Reactstrap.ListGroupItem tag="button" onClick={() => this.setCategory("Soup")} action>Soups</Reactstrap.ListGroupItem>
          <Reactstrap.ListGroupItem tag="button" onClick={() => this.setCategory("Main Course")} action>Main Courses</Reactstrap.ListGroupItem>
          <Reactstrap.ListGroupItem tag="button" onClick={() => this.setCategory("Drink")} action>Drinks</Reactstrap.ListGroupItem>
          <Reactstrap.ListGroupItem tag="button" onClick={() => this.setCategory("Dessert")} action>Desserts</Reactstrap.ListGroupItem>
        </Reactstrap.ListGroup>
              
        {this.renderCategory()}

        <h3>Order</h3>
        {this.renderOrder()}

        <form onSubmit={this.handleSubmit}>
          <label>
            Location tag:
            <input type="number" min="0" name="locationTag" value={this.state.locationTag} onChange={(e) => {
                this.handleInputChange(e);
              }}/>
          </label>
          <input type="submit" value="Submit"/>
        </form>
      </div>
    );
  }

  renderCategory() {
    return(<table>
      <thead>
        <tr>
          <th>Item</th>
          <th>Description</th>
          <th>Calories</th>
          <th>€</th>
        </tr>
      </thead>
      <tbody>
        {!this.state.items || this.state.items.length <= 0 ? (
          <tr>
            <td colSpan="6" align="center">
            <b>Oops, no food here yet</b>
            </td>
          </tr>) : 
            (this.state.items.map(item => (
            item.category.S == this.state.selectedCategory ?
              <tr colSpan="6" align="center" key={item.food_id.N}>
                <td>{item.name.S}</td>
                <td>{item.description.S}</td>
                <td>{item.calories.N}</td>
                <td>{item.price.N}</td>
                <Reactstrap.Button onClick={() => this.addItem(item)}>Add</Reactstrap.Button>
              </tr> :
                null)
              )
            )
          }
        </tbody>
    </table>);
  }

  renderOrder() {
    return(
    <table>
      <tbody>
        {!this.state.order || this.state.order.length <= 0 ? (
          <tr>
            <td colSpan="6" align="center">
            <b>You haven't added any food items yet.</b>
            </td>
          </tr>) : 
            (this.state.order.map(item => (
              <tr colSpan="6" align="center">
                <td>{item.name}</td>
                <td>{item.price}</td>
                <Reactstrap.Button onClick={() => this.removeItem(item)}>Remove</Reactstrap.Button>
              </tr>
              )
            )
          )
        }
      </tbody>
    </table>);
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