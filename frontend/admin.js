import React from 'react'
export default class Admin extends React.Component {

  constructor(props){
    super(props);
    this.state = {
    }
  }

    render() {
    return (
    <div>
      Admin page
      <div class="input-group mb-3">
      <div class="input-group-prepend"><span class="input-group-text">
        Token</span></div>
      <input type="password" id="token" className="form-control" />
      </div>
    </div>
    )
  }
}

