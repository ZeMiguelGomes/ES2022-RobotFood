var Router = ReactRouterDOM.Router;
var Route = ReactRouterDOM.Route;
var Link = ReactRouterDOM.Link;

var canLoggin = '';

const App = () => (
  <div>
    <h1> Kitchen staff</h1>
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
  </div>

)

const Home = () => <h1>Home</h1>
const Login1 = () => <h1>Login</h1>
const Register = () => <h1>Register</h1>

ReactDOM.render(<App />, document.getElementById('login'));

