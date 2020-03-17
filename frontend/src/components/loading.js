import React from 'react';
import './loading.css'

export default (props) => {
    return (
        <div className="overlay">
            <div className="spinner-box">
                <div className="main-spinner spinner-border text-info align-middle" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            </div>
        </div>
    )
}