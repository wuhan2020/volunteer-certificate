import React from 'react'
import { API_URL } from './config-local';

export default class Admin extends React.Component {

  constructor(props) {
    super(props);
    let host = API_URL;        
    if (host[host.length - 1] != '/') {
        host = host + '/';
    }
    this.state = {
      host,
      token: "",
      file: null,
      alert_message: '',
      status: null
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleImageSelect = this.handleImageSelect.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  submitPictureAndParameters() {
    const { host } = this.state;
    let api = `${host}api/uploadImage`;
    this.postFormData(api)
        .then( res => res.json() )
        .then( (result) => {
            const { code, message } = result;
               this.setState({
                 alert_message: message,
                 status: code == 0 ? 'success' : 'fail'
               });
         })
         .catch( (error) => {
             console.error('Error:', error);
             this.setState({status: 'fail',
                            alert_message: 'network problem'});
         });
  }
  postFormData(api) {
    let headers = new Headers();
    headers.append('Token', this.state.token);
    headers.append('Content-Type', 'multipart/form-data');
    const formData = new FormData();
    formData.append('template', this.state.file);
    return  fetch(api, {
      method: 'POST',
      mode: 'cors',
      headers,
      body: formData
    });
  }
  handleChange(e) {
    let new_json = {}
    new_json[e.target.name] = e.target.value;
    this.setState( new_json );
  }
  handleImageSelect(e) {
    this.setState({file: e.target.files[0]});
  }
  handleSubmit(e) {
    e.preventDefault();
    this.submitPictureAndParameters();
  }
  render() {
    let AlertPart;
    if(this.state.status == 'success') {
      AlertPart = 
        (<div className="alert alert-success" role="alert">
          {this.state.alert_message}
        </div>);
    } else if(this.state.status == 'fail') {
      AlertPart = 
        (<div className="alert alert-danger" role="alert">
          {this.state.alert_message}
        </div>);
    } else {
      AlertPart = (<div />);
    }
    return (
    <div>
      Admin page
      <form onSubmit={this.handleSubmit}>
        {AlertPart}
        <div className="input-group mb-3">
        <div className="input-group-prepend"><span className="input-group-text">
          Token</span></div>
        <input type="password" id="token" className="form-control" name="token"
          value={ this.state.token } onChange={this.handleChange}/>
        </div>
        <div className="form-group">
          <label htmlFor="template">Template Image</label>
          <input type="file" className="form-control-file"
                id="template" accept=".jpg"
                onChange={this.handleImageSelect}/>
        </div>
        <div className="form-group">
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
    </div>
    )
  }
}

