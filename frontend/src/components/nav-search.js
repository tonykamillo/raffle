import React from 'react';

export default class Search extends React.Component {

    constructor(props)
    {
        super(props);
        this.state = {terms: ''};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleClear = this.handleClear.bind(this);
        this.reloadContests = this.reloadContests.bind(this);
    }

    handleChange(event)
    { this.setState({terms: event.target.value}) }

    handleClear(event)
    {
        event.preventDefault()
        this.setState({terms: ''}, () => this.reloadContests());
    }

    handleSubmit(event)
    {
        event.preventDefault();
        this.reloadContests();
    }

    reloadContests()
    {
        this.props.fetchContests({
            search: this.state.terms
        })
    }

    render()
    {
        return (
            <form className="form-inline">
                <input onChange={this.handleChange} value={this.state.terms} className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                <button onClick={this.handleSubmit} className="btn btn-outline-success my-2 my-sm-0 mr-1" type="submit">Search</button>
                <button onClick={this.handleClear} className="btn btn-outline-secondary my-2 my-sm-0" type="submit">Clear</button>
            </form>
        )
    }
}
