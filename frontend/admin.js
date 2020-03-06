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
      <form>
      <div class="input-group mb-3">
      <div class="input-group-prepend"><span class="input-group-text">
        Token</span></div>
      <input type="password" id="token" className="form-control" />
      </div>
      <div class="form-group">
        <label for="template">Template Image</label>
        <input type="file" class="form-control-file"
               id="template" accept=".jpg"/>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">
          Submit
        </button>
      </div>
      </form>
    </div>
    )
  }
}

