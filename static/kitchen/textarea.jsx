class MyPage extends React.Component {
    constructor(props) {
        super(props)
        this.state = { text : props.text }
        this.textreference = React.createRef();
    }

    render() {
        return (
            <div>
                <textarea rows="4" cols="50" defaultValue={this.state.text}
                onChange={this.changeText.bind(this)}
                ref={this.textreference}/>
                <p>{this.state.text}</p>
            </div>
        )
    }

    changeText() {
        this.setState({
            text : this.textreference.current.value
        })
    }
}

ReactDOM.render(<MyPage text="Put your text here"/>, reacthere)