import React from 'react'
import ReactDOM from 'react-dom'
import Admin from './admin'
import UserProfile from './userProfile'
import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css'

const App = () => (
        <div>
            <UserProfile />
        </div>
    )
const AdminApp = () => (
        <div>
            <Admin />
        </div>
    )
if(window.location.href.search('admin.html') > 0) {
    ReactDOM.render(
        <AdminApp/>, document.getElementById('root')
    )
}
else { //  
    ReactDOM.render(
        <App />, document.getElementById('root')
    )
}
