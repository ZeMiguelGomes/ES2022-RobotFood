var Router = ReactRouterDOM.Router;
var Route = ReactRouterDOM.Route;
var Link = ReactRouterDOM.Link;

var canLoggin = '';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      validate: {
        emailState: '',
      },
      canLoggin: true,
    };
    this.handleChange = this.handleChange.bind(this);
    this.changeStateLogin = this.changeStateLogin.bind(this);
    this.submitForm = this.submitForm.bind(this);
  }

  changeStateLogin(){
    this.setState({canLoggin: false});
  }

  handleChange = (event) => {
    const { target } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const { name } = target;

    this.setState({
      [name]: value,
    });
  };

  validateEmail(e) {
    const emailRex =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const { validate } = this.state;

    if (emailRex.test(e.target.value)) {
      validate.emailState = 'has-success';
    } else {
      validate.emailState = 'has-danger';
    }

    this.setState({ validate });
  }

  submitForm = (e) => {
    e.preventDefault();
    console.log(`Email: ${this.state.email}`);
    console.log(`Pass: ${this.state.password}`);

    var that = this;

    fetch('/kitchen/login/', {
      // Adding method type
      method: "POST",
      // Adding body or contents to send
      body: JSON.stringify({
          username: this.state.email,
          password: this.state.password,
      }),
      // Adding headers to the request
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      }
  }).then(function(response){
    return response.json()
    .then(function(json){

      if(json != null){
        if(json['Attributes']['authToken'] != null){
          //Go to new screen
          canLoggin = 'True'
          var staffProps = {
            'email': json['Attributes']['staff_email'], 
            'name' : json['Attributes']['name'],
            'authToken' : json['Attributes']['authToken']
          }
          sessionStorage.setItem('email', JSON.stringify(staffProps));
          console.log(JSON.stringify(staffProps));
          window.location.replace('/kitchen/login/');

        }else{
          that.changeStateLogin();
          canLoggin = 'False'
        }
      }else{
        that.changeStateLogin();
        canLoggin = 'False'
      }
    
    });
  })
  };

  

  render() {
    const { email, password } = this.state;

    return (
      <div className="Login">
        <h2>Sign In</h2>
        <Reactstrap.Form className="form" onSubmit={(e) => this.submitForm(e) }>
          <Reactstrap.FormGroup>
            <Reactstrap.Label>Username</Reactstrap.Label>
            <Reactstrap.Input
              type="email"
              name="email"
              id="exampleEmail"
              placeholder="example@example.com"
              valid={ this.state.validate.emailState === 'has-success' }
              invalid={this.state.validate.emailState === 'has-danger'}
              value={email}
              onChange={(e) => {
                this.validateEmail(e);
                this.handleChange(e);
              }}
            />
            <Reactstrap.FormText>Your username is most likely your email.</Reactstrap.FormText>
          </Reactstrap.FormGroup>
          <Reactstrap.FormGroup>
            <Reactstrap.Label for="examplePassword">Password</Reactstrap.Label>
            <Reactstrap.Input
              type="password"
              name="password"
              id="examplePassword"
              placeholder="********"
              value={password}
              onChange={(e) => this.handleChange(e)}
            />
          </Reactstrap.FormGroup>
          <Reactstrap.Button >Submit</Reactstrap.Button>
          {this.state.canLoggin == false ?<Reactstrap.FormText> Oops something wrong happened!</Reactstrap.FormText>:null}

        </Reactstrap.Form>
      </div>
    );
  }
}


const Register = () => <h1>Register</h1>

ReactDOM.render(<Login/>, document.getElementById('login'))

const App = () => (
  <ReactRouterDOM.HashRouter>
    <ul>
      <li><Link to="/">Home</Link></li>
      <li><Link to="/login">Login1</Link></li>
      <li><Link to="/register">Register</Link></li>
    </ul>

    <Route path="/" exact component={Home} />
    <Route path="/login" component={Login1} />
    <Route path="/register" component={Register} />
  </ReactRouterDOM.HashRouter>
)

//const Home = () => <h1>Home</h1>
//const Login1 = () => <h1>Login</h1>
//const Register = () => <h1>Register</h1>

//ReactDOM.render(<App />, document.getElementById('login'));

