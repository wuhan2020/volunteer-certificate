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
ReactDOM.render(
    <App/>, document.getElementById('root')
)