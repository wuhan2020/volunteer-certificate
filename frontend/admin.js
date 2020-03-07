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
      status: null,
      textAreaContent: '',
      org_name: '',
      org_website: '',
      name_horizontal_pos: 0,
      name_vertical_pos: 0,
      org_email_username: '',
      org_email_password: ''
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
  submitConfigurations() {
    const { host } = this.state;
    let api = `${host}api/updateOrgConfig`;
    let data = {
      name: this.state.org_name,
      website: this.state.org_website,
      name_horizontal_pos: this.state.name_horizontal_pos,
      name_vertical_pos: this.state.name_vertical_pos,
      email: {
        username: this.state.org_email_username,
        password: this.state.org_email_password
      }
    }
    this.postJsonData(api, data)
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
  submitVolunteerEmails() {
    const { host } = this.state;
    let api = `${host}api/addUserData`;
    let data = {
      email: this.state.textAreaContent.split('\n'),
      token: this.state.token
    }
    this.postJsonData(api, data)
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
    // headers.append('Content-Type', 'multipart/form-data');
    const formData = new FormData();
    formData.append('template', this.state.file);
    return  fetch(api, {
      method: 'POST',
      mode: 'cors',
      headers,
      body: formData
    });
  }
  postJsonData(api, data) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    let configurations = {
        method: 'POST',
        mode: 'cors',
        headers,
        body: JSON.stringify(data)
    };        
    return  fetch(api, configurations);
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

      <form onSubmit={
        (e) => {
          e.preventDefault();
          this.submitConfigurations();
        }}>
        <div className="form-row">
          <div className="form-group col-md-6">
            <label htmlFor="orgName">Organization Name</label>
            <input type="text" className="form-control" id="orgName"
                   name="org_name" value={ this.state.org_name }
                   onChange={this.handleChange}></input>
          </div>
          <div className="form-group col-md-6">
          <label htmlFor="orgWebsite">Organization Website</label>
          <input type="url" className="form-control" id="orgWebsite"
                 name="org_website" value={ this.state.org_website }
                 onChange={this.handleChange}></input>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group col-md-6">
          <label htmlFor="orgEmail">Organization Email</label>
            <input type="email" className="form-control" id="orgEmail"
                   name="org_email_username" value={ this.state.org_email_username }
                   onChange={this.handleChange}></input>
          </div>
          <div className="form-group col-md-6">
          <label htmlFor="orgEmailSMTPPass">SMTP password</label>
            <input type="password" className="form-control" id="orgEmailSMTPPass"
                   name="org_email_password" value={ this.state.org_email_password }
                   onChange={this.handleChange}></input>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group col-md-6">
            <label htmlFor="nameHorizontal">Volunteer name horizontal position</label>
            <input type="text" className="form-control" id="nameHorizontal"
                   name="name_horizontal_pos" value={ this.state.name_horizontal_pos }
                   onChange={this.handleChange}></input>
          </div>
          <div className="form-group col-md-6">
            <label htmlFor="nameVertical">Vertical position</label>
            <input type="text" className="form-control" id="nameVertical"
                   name="name_vertical_pos" value={ this.state.name_vertical_pos }
                   onChange={this.handleChange}></input>
          </div>
        </div>
        <button type="submit" className="btn btn-primary">
            Submit
        </button>        
      </form>
      <form onSubmit={(e) => {
        e.preventDefault();
        this.submitVolunteerEmails();
      }}>
        <div className="form-group">
          <label htmlFor="email-lists">volunteer email lists</label>
          <textarea className="form-control" rows="3"
              name="textAreaContent"
              value={ this.state.textAreaContent }
              onChange={this.handleChange}></textarea>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
    </div>
    )
  }
}

