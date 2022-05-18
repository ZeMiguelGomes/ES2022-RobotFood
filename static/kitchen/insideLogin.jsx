var Router = ReactRouterDOM.Router;
var Route = ReactRouterDOM.Route;
var Link = ReactRouterDOM.Link;

var canLoggin = '';

const App = () => (
  <div>
    <h1> Kitchen staff</h1>
  </div>

)

const Home = () => <h1>Home</h1>
const Login1 = () => <h1>Login</h1>
const Register = () => <h1>Register</h1>

ReactDOM.render(<App />, document.getElementById('login'));

