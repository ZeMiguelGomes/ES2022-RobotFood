class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      canSeePage : false,
      items: [],
    }
    this.handleSeingPage = this.handleSeingPage.bind(this);
    
  }
  
  handleSeingPage(){
    this.setState({canSeePage : true})
  }

  verifyAuthToken(){
    const data = JSON.parse(sessionStorage.getItem('email'));
    if (data == null){
      window.location.replace('/kitchen/');
    }
    else{
      this.handleSeingPage();
    }
    
  }

  updateState() {
    fetch('/kitchen/getOrder/')
        .then(res => res.json())
        .then((data) => {
          this.setState({
            items: data
          })
          console.log(data);

        })
  }


  componentDidMount(){
    this.verifyAuthToken();
    this.updateState();
  }

  render(){
    const canSeePage = this.state.canSeePage;
    console.log(canSeePage);
    
    return(
      <div>
        {canSeePage ? 
        <div>
        <KitchenPage/> 
        <div className="insideLogin">
          <h1> Kitchen staff</h1>
          <div>
            <Reactstrap.Container style={{ marginTop: "20px" }}>
              <h2 class="text-left text-primary"> Orders List</h2>
              <Reactstrap.Table dark>
                    <thead>
                        <tr>
                          <th>Location Tag</th>
                          <th>Order Description</th>
                          <th>Status</th>
                          <th></th>
                        </tr>
                      </thead>
                      <tbody>
                      {!this.state.items || this.state.items.length <= 0 ? (
                        <tr>
                          <td colSpan="6" align="center">
                          <b>Ops, no orders to fill here yet</b>
                          </td>
                        </tr>):
                        (
                          this.state.items.map((item) => (
                            <tr colSpan="6" align="center" key={item.order_id.S}>
                              <td>{item.locationTag.N}</td>
                              <td>{item.items.L.map(item =>( item.S + '\n'
                              ))}</td>
                              <td>{item.status.S}</td>
                            </tr>)
                          )
                        )}
                      </tbody>
                </Reactstrap.Table>
            </Reactstrap.Container>
          </div>
        </div>
        </div>
        : null}
    </div>
    );
  }

}

function KitchenPage(){
  return(
      <div>
        <div className="loginButton">
        <Logout/>
        </div>
      </div>

  );
}


function Logout(){
  function logoutStaff(){
    const data = JSON.parse(sessionStorage.getItem('email'));
    fetch('/kitchen/login/', {
      // Adding method type
      method: "PUT",
      // Adding body or contents to send
      body: JSON.stringify({
          username: data['email'],
      }),
      // Adding headers to the request
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      }
  });
  
  sessionStorage.removeItem('email');
  window.location.replace('/kitchen/');
  }

  return(
    <div>
      <Reactstrap.Button onClick={logoutStaff} >Logout</Reactstrap.Button>
    </div>
  );
}




ReactDOM.render(<App />, document.getElementById('login'));

