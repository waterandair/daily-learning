import Component from "react"

class ControlledComponents extends Component {
    constructor(props) {
        super(props);

        this.state = { value: "" }

    }

    handleChange(event) {
        this.setState({ value: event.target.value })
    }

    handleSubmit(event) {
        alert("a name was submitted: " + this.state.value);
        event.preventDefault()
    }

    render() {
        return (
            <div>
                <h1>受控组件: </h1>
                <form onSubmit={this.handleSubmit}>
                    <lable>Name:
                        <input type="text" value={this.state.value} onChange={this.handleChange} />
                    </lable>
                    <input type="submit" value="submit" />
                </form>
            </div>
        )
    }
}


export default ControlledComponents