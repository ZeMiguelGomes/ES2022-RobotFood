class MyPage extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            picturePreview: "",
            pictureAsFile: ""
        }
        this.textreference = React.createRef();
        this.uploadPicture = this.uploadPicture.bind(this);
        this.setImageAction = this.setImageAction.bind(this);
    }

    uploadPicture = (e) => {
      this.setState({
          picturePreview : URL.createObjectURL(e.target.files[0]),
          pictureAsFile : e.target.files[0]
      })
  };

    setImageAction = () => {
      const formData = new FormData();
      formData.append(
          "file",
          this.state.pictureAsFile,
          this.state.pictureAsFile.name
      );
      const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch('/customer/uploadphoto/', requestOptions)
        .then(res => res.json())
        .then(data => {
          this.setState({ postId: data.id });
          console.log(data)
        });
  };

    render() {
        return (
          <form onSubmit={this.setImageAction}>
            <input type="file" name="image" onChange={this.uploadPicture}/>
            <br />
            <img src={this.state.picturePreview} alt="Preview" width="120" height="100"></img>
            <br />
            <button type="submit" name="upload">
              Upload
            </button>
          </form>
        );
    }

}

ReactDOM.render(<MyPage/>, reacthere)