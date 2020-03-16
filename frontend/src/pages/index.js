import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NavBar from '../components/navbar.js';
import Cards from '../components/cards.js';

const API = 'http://localhost:5000/';

export default (props) => {

    const [contests, setContests] = useState([]);

    useEffect(() => {
        fetchContests()
    }, [])

    const fetchContests = (params) => {
        axios.get(API + 'contests/', {
            params
        })
        .then(res => {
            return res.json()
        })
        .then(json => {
            if (json.success)
                setContests(json.found)
            else
                throw json.message

        })
        .catch(err => console.log(err))
    }

    return (
        <div className="container">
            <NavBar></NavBar>
            <Cards cards={contests}></Cards>
        </div>
    )
}