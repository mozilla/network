import { Component } from "react";

/**
 * Renders mobile version of multipage navs (secondary navs)
 */
class MultipageNavMobile extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);

    this.state = {
      isOpen: false,
    };
  }

  toggle() {
    this.setState({
      isOpen: !this.state.isOpen,
    });
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  render() {
    let activeLinkLabel;
    let links = this.props.links.map((link, index) => {
      let className = `multipage-link${link.isActive ? ` active` : ``}`;

      if (link.isActive) {
        activeLinkLabel = (
          <div className={`active-link-label d-inline-block ${className}`}>
            {link.label}
          </div>
        );
      }

      return (
        <div key={`link-${index}`}>
          <a href={link.href} className={className}>
            {link.label}
          </a>
        </div>
      );
    });

    links.unshift(
      <div key="current-active-link">
        <button className="expander" onClick={this.toggle}>
          <div className="d-flex justify-content-between">
            <div>{activeLinkLabel}</div>
            <div className="d-inline-block align-self-center control" />
          </div>
        </button>
      </div>
    );

    return (
      <div
        className={`dropdown-nav${
          this.state.isOpen ? ` dropdown-nav-open` : ``
        }`}
      >
        {links}
      </div>
    );
  }
}

export default MultipageNavMobile;
