class MyPage extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            email: "",
            password: "",
            alertMessage: "",
        }
        this.textreference = React.createRef();
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.setAlertMessage = this.setAlertMessage.bind(this);
    }

    handleInputChange(event) {
        event.preventDefault();
        const target = event.target;
        this.setState({
            [target.name]: target.value
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
                email: this.state.email,
                password: this.state.password
            })
        };
        fetch('/kitchen/', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ postId: data.id }))
            .then(body => {
              print(body)
            })
            .catch(error => this.setAlertMessage(error.message));
    }

    setAlertMessage(message) {
        this.setState({ alertMessage: message });
    }

    render() {
        return (
            <div>
              <Alert message={this.state.alertMessage} />
              <form onSubmit={this.handleSubmit}>
                <label>
                  Email
                  <input
                    name="email"
                    type="text"
                    value={this.state.email}
                    onChange={this.handleInputChange}
                  />
                </label>
                <label>
                  Password
                  <input
                    name="password"
                    type="password"
                    value={this.state.password}
                    onChange={this.handleInputChange}
                  />
                </label>
                <button type="submit">Log in</button>
              </form>
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

ReactDOM.render(<MyPage/>, reacthere)