
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
        { items.map(item =>
            <div className="col col-sm-6 col-lg-4 col-xl-3 mb-4">
                <Card key={item.id} title={item.name} fields={[
                    {label: 'Descrição', value: item.description},
                    {label: 'Sorteado em:', value: item.held_in}
                ]} buttons={[]}/>
            </div>
        )}
        </div>
    );
}