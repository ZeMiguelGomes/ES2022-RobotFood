const { useState } = React;
const { Table, Form,FormGroup, Label, Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } = Reactstrap;



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
          seePopup: false,
          picturePreview: "",
          pictureAsFile: ""
      }
      this.textreference = React.createRef();
      this.setCategory = this.setCategory.bind(this);
      this.addItem = this.addItem.bind(this);
      this.removeItem = this.removeItem.bind(this);
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.setAlertMessage = this.setAlertMessage.bind(this);
      this.setPopupVisible = this.setPopupVisible.bind(this);
      this.submitOrder = this.submitOrder.bind(this);
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

  setPopupVisible(){
    this.setState({seePopup: true});
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
            order: this.state.order
        })
    };
    fetch('/customer/orderprice/', requestOptions)
        .then(response => response.json()
        .then(data => {
          this.setState({ price: data });
          console.log(data)
        })
        ).catch(error => this.setAlertMessage(error.message));
    this.setPopupVisible();
  }

  uploadPicture = (e) => {
    this.setState({
        picturePreview : URL.createObjectURL(e.target.files[0]),
        pictureAsFile : e.target.files[0]
    })
};

  validateInputs = () => {
    if(this.state.order.length > 0 && this.state.locationTag != "" && this.state.pictureAsFile != "") {
      this.submitOrder();
    }
    else {
      alert("Please fill in all fields.")
    }
  }

  submitOrder() {
    const formData = new FormData();
    formData.append(
        "file",
        this.state.pictureAsFile,
        this.state.pictureAsFile.name
    );
    console.log(this.state.pictureAsFile.name)
    const requestOptions = {
      method: 'POST',
      body: formData,
      headers: {"Access-Control-Allow-Origin": "*"}
  };

  fetch('/customer/uploadphoto/', requestOptions)
      .then(res => res.json())
      .then(data => {
        this.setState({ photoCheck: data });
        
        let check = JSON.parse(this.state.photoCheck)
        console.log(check)
        if(check["found"]) {
          fetch('/customer/submitorder/', {
            // Adding method types
            method: "POST",
            // Adding body or contents to send
            body: JSON.stringify({
                items: this.state.order,
                price: this.state.price,
                name: check["name"],
                locationTag: this.state.locationTag
            }),
            // Adding headers to the request
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(function(res) {
          res.json();
          console.log(res);
        });
        //sessionStorage.setItem('uuid', JSON.stringify(staffProps));
        alert("Order submitted!")

      }
      else {
        alert("Face not recognized, please contact customer support.");
      }

      window.location.replace('/');
      });

      
  };

  render() {
    const seePopup = this.state.seePopup;
    console.log(seePopup);
    return (
      <div>
        <div className="menuCustomer">
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
          {this.state.seePopup ? this.ModalExample() : null}
        </Form>
      </div>            
      </div>
    );
  }

  renderCategory() {
    return(
    <Table dark>
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
                <td><Reactstrap.Button className="btn btn-danger" onClick={() => this.addItem(item)}> Add</Reactstrap.Button></td>
              </tr> :
                null)
              )
            )
          }
        </tbody>
    </Table>);
  }

  renderOrder() {
    return(
    <Table>
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
                <td><Reactstrap.Button onClick={() => this.removeItem(item)}>Remove</Reactstrap.Button></td>
              </tr>
              )
            )
          )
        }
      </tbody>
    </Table>);
  }


ModalExample() {
 
  return (
    <div>
      {/* <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
        Launch demo modal
      </button> */}
      <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Order Summary</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <Label> Total price: {this.state.price} €</Label>
            <br />
            <input type="file" name="image" onChange={this.uploadPicture}/>
            <br />
            <img src={this.state.picturePreview} alt="Preview" width="120" height="100"></img>
            <br />

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-dismiss="modal" onClick={this.validateInputs}>Submit Payment</button>
          </div>
        </div>
      </div>
      </div>  
    </div>

    
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