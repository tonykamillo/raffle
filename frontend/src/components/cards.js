
import React from 'react';
import Card from './card.js';
import './cards.css';

export default ({cards}) => {
    let items = [...cards]
    items = items.concat([...cards])
    items = items.concat([...cards])
    items = items.concat([...cards])
    items = items.concat([...cards])

    return (
        <div className="cards row">
        { items.map((item, index) =>
            <div key={index} className="col-xs-12 col-sm-12 col-lg-4 mb-4">
                <Card title={item.name} fields={[
                    {label: 'Descrição', value: item.description},
                    {label: 'Sorteado em:', value: item.held_in}
                ]} buttons={[]}/>
            </div>
        )}
        </div>
    );
}