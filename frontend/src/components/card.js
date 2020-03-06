
import React from 'react';
import Button from './button.js';
import './card.css';

const Card = ({title, fields, buttons}) => {
  return (

    <div className="card h-100">
        <div className="card-body">
            <h4 className="card-title">{title}</h4>
            { fields.map(item =>
            <p className="card-text" key={item.label}>
                <strong>{item.label}</strong>
                <span>{item.value || ' --------'}</span>
            </p>
            )}
        </div>
        <div className="buttons-place mb-4">
            <a href="#" className="action btn btn-primary">Go somewhere</a>
            { buttons.map(btnConfig =>
                <Button key={btnConfig} {...btnConfig} />
            )}
        </div>
    </div>

  );
}

export default Card;
