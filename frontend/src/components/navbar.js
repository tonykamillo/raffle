import React from 'react';
import NavSearch from './nav-search.js'

export default (props) => {
    return (
        <nav className="navbar navbar-expand-lg fixed-top navbar-dark bg-dark mb-3">
            <a className="navbar-brand" href="/">Raffle</a>
            <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
                <ul className="navbar-nav">
                    <li className="nav-item active">
                        <a className="nav-link" href="#">Open Contests <span className="sr-only">(current)</span></a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="#">Helded</a>
                    </li>
                </ul>
            </div>
            <NavSearch fetchContests={props.fetchContests}></NavSearch>
        </nav>
    )
}
