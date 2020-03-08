import React from 'react';

import { API_URL } from './config-local';
import { formText } from './data-source';

import './scss-legacy/certificationContent.scss';

class CertificationContent extends React.Component {
    constructor(props) {
        super(props);
        let host = API_URL;
        
        if (host[host.length - 1] != '/') {
            host = host + '/';
        }
            
        this.state = {
            host,
            email: '',
            name: '',
            status: 'none',
            isShowImage: false,
            token: '',
            message: ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleResizing = this.handleResizing.bind(this);
        this.handleNameChange = this.handleNameChange.bind(this);
    }
    getUserInfo(token) {
        const { host } = this.state;
        let api = `${host}api/getUserInfo?token=${token}`;
        this.fetchCertificationApi(api, null, 'GET')
            .then( res => res.json() )
            .then( (result) => {
                const { code, data, message } = result;
                let email = '';
                if (code == 0) {
                    email = data.email;
                }
                   this.setState({
                     email,
                     message,
                     status: code == 0 ? 'none' : 'error'
                   });
             })
             .catch( (error) => {
                 console.error('Error:', error);
             });
    }
    getAlertType(status) {
        let type = ['error', 'none', 'warn'].filter( type => status.toLowerCase().includes(type))[0];
        return  type || 'successful';
    }
    getParameterByName(name) {
        const match = RegExp(`[?&]${name}=([^&]*)`).exec(window.location.search);
        return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
    }

    getToken() {
        return this.getParameterByName('token');
    }
    // return fetch promise
    fetchCertificationApi(api, data, method='POST') {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        let configurations = {
            method,
            mode: 'cors',
            headers
        };

        if (method == 'POST') {
            configurations['body'] = JSON.stringify(data);
        }
            
        return  fetch(api, configurations);
    };

    handleSubmit(event) {
        event.preventDefault();

        const { name, token, host } = this.state;
        const api = `${host}api/submitUserInfo`; 
        const payloadData = { name, token };

        this.fetchCertificationApi(api, payloadData)
            .then( res => res.json() )
            .then( (result) => {
                const { code, message } = result;
                this.setState({
                    status: code === 0 ? 'successful' : 'error',
                    message
                });
            })
            .catch( (error) => {
               console.error('Error:', error);
            });
    };

    handleResizing() {
        this.setState({ isShowImage: window.innerWidth > 1200 });
    }
    handleNameChange(e) {
        this.setState( {name: e.target.value});
    }
    componentDidMount() {
        this.handleResizing();
        window.addEventListener('resize', this.handleResizing);
        const token = this.getToken();
        this.setState( { token });
        this.getUserInfo(token);
    }

    componentDidUpdate() {
        window.addEventListener('resize', this.handleResizing);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.handleResizing);
    }

    render() {
        const alertType = this.getAlertType(this.state.status);
        return (
            <section>
                <div className="certification-content">
                <div className="certification-content-alerts-wrapper">
                  {
                    this.state.status == 'none' ? null : (
                        <div className={`certification-content-alerts row ${alertType}`}>
                            <span className="alert-msg">
                                {this.state.message}
                            </span>
                        </div>
                    )
                  }
                  </div>

                    <div className="certification-content-main row">
                        {
                            this.state.isShowImage &&
                            <aside className="column">
                                <figure>
                                    <img src="/images/certification/illustration.png" />
                                </figure>
                            </aside>
                        }
                        <form className="column" onSubmit={this.handleSubmit}>
                            <fieldset>
                                <legend>{formText.header}</legend>
                                <div className="form-row email">
                                    <label>{formText.emailLabel}</label>
                                    <input type="email" name="mail" value={ this.state.email } disabled />
                                </div>
                                <div className="form-row name">
                                    <label>{formText.nicknameLabel}
                                        <span className="description">{formText.nicknameDescription}</span>
                                    </label>
                                    <input type="text" name="name" value={this.state.name} onChange={this.handleNameChange} />
                                </div>
                                <div className="form-row action">
                                    <input type="submit" value={formText.action} />
                                </div>
                            </fieldset>
                        </form>
                    </div>
                </div>
            </section>
        )
    }
}

export default CertificationContent