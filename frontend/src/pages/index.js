import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NavBar from '../components/navbar.js';
import Cards from '../components/cards.js';
import Loading from '../components/loading.js'

const API = 'http://localhost:5000/';

export default (props) => {

    const [contests, setContests] = useState([]);
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        fetchContests()
    }, [])

    const fetchContests = async (params) => {
        setLoading(true)
        const response = await axios.get(API + 'contests/', {
            params
        })

        if (response.data.success)
            setContests(response.data.found)
        else
        {
            console.exception(response.data.message)
            throw response.data.message
        }
        setLoading(false)
    }

    return (
        <div className="container">
            <NavBar fetchContests={fetchContests}></NavBar>
            {loading &&
                <Loading></Loading>
            }
            <Cards cards={contests}></Cards>
        </div>
    )
}