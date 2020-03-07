import React from 'react';

import CertificationContent from './certificationContent';
import './scss-legacy/userProfile.scss';

class Certification extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        const dataSource = {};
        const logoUrl = '/wuhan2020-logo-white.png';
        return (
            <main>
                <div className="certification-page">
                    <header>
                        <a href='/'>
                            <img className="logo" alt="logo missing" src={logoUrl} />
                        </a>
                    </header>
                    <article>
                        <CertificationContent />
                    </article>
                </div>
            </main>
        )
    }

}


export default Certification;