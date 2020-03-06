import React from 'react';
import NavSearch from './nav-search.js'

export default (props) => {
    return (
        <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark mb-3">
            <a class="navbar-brand" href="/">Raffle</a>
            <button
                class="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Open Contests <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Helded</a>
                    </li>
                </ul>
            </div>
            <NavSearch></NavSearch>
        </nav>
    )
}
