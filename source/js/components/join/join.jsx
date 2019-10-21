import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import classNames from "classnames";
import CountrySelect from "../petition/country-select.jsx";
import { getText } from "../petition/locales";
import { getCurrentLanguage } from "../petition/locales";
import LanguageSelect from "./language-select.jsx";

export default class JoinUs extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  reset() {
    if (!this.state.apiSuccess) {
      this.email.value = "";
      this.privacy.checked = false;
    }
    this.setState(this.getInitialState());
  }

  getInitialState() {
    return {
      apiSubmitted: false,
      apiSuccess: false,
      apiFailed: false,
      userTriedSubmitting: false,
      lang: getCurrentLanguage()
    };
  }

  /**
   * Ensure that the parent component is informed
   * about this component being mounted (primarily
   * used in the context of automated testing)
   */
  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  componentDidUpdate(prevProps, prevState) {
    let navWrapper = document.querySelector("#nav-newsletter-form-wrapper");

    // when user has successfully signed up for newsletter from the newsletter section on the nav,
    // update the dismiss button so it reads "Back to menu" instead of "No thanks"
    if (
      navWrapper &&
      navWrapper.contains(ReactDOM.findDOMNode(this)) &&
      navWrapper.querySelector(".form-dismiss") &&
      this.state.apiSuccess
    ) {
      navWrapper.querySelector(".form-dismiss").textContent = "Back to menu";
    }
  }

  // state update function
  apiSubmissionSuccessful() {
    this.setState({
      apiSuccess: true
    });
  }

  // state update function
  apiSubmissionFailure(e) {
    if (e && e instanceof Error) {
      this.setState({
        apiFailed: true
      });
    }
  }

  // state check function
  apiIsDone() {
    return (
      this.state.apiSubmitted && (this.state.apiSuccess || this.state.apiFailed)
    );
  }

  /**
   * Performs very simple validation for emails.
   * @param {string} input the string that should be validated as an email address
   * @returns {boolean} true if the input is a legal-enough email address, else false
   */
  validatesAsEmail(input) {
    if (!input) {
      return {
        valid: false,
        errorMessage: `This is a required section.`
      };
    }

    let valid = input.match(/[^@]+@[^.@]+(\.[^.@]+)+$/) !== null;

    if (!valid) {
      return {
        valid: false,
        errorMessage: `Please enter a valid email address.`
      };
    }

    return {
      valid: true
    };
  }

  /**
   * Submit the user's data to the API server.
   */
  submitDataToApi() {
    this.setState({ apiSubmitted: true });

    return new Promise((resolve, reject) => {
      let payload = {
        email: this.email.value,
        /* Strip query params in source url for newsletter signups: https://github.com/mozilla/foundation.mozilla.org/issues/2994#issuecomment-516997473 */
        source: window.location.href.split(`?`)[0]
      };

      if (this.givenNames) {
        payload.givenNames = this.givenNames.value;
      }
      if (this.surname) {
        payload.surname = this.surname.value;
      }
      if (this.state.country) {
        payload.country = this.state.country;
      }
      if (this.state.lang) {
        payload.lang = this.state.lang;
      }

      let xhr = new XMLHttpRequest();

      xhr.onreadystatechange = () => {
        if (xhr.readyState !== XMLHttpRequest.DONE) {
          return;
        }

        if (xhr.status !== 201) {
          reject(new Error(xhr.responseText));
        }

        resolve();
      };

      xhr.open(`POST`, this.props.apiUrl, true);
      xhr.setRequestHeader(`Content-Type`, `application/json`);
      xhr.setRequestHeader(`X-Requested-With`, `XMLHttpRequest`);
      xhr.setRequestHeader(`X-CSRFToken`, this.props.csrfToken);
      xhr.timeout = 5000;
      xhr.ontimeout = () => reject(new Error(`xhr timed out`));

      xhr.send(JSON.stringify(payload));
    });
  }

  /**
   * Process the form data, to make sure there is a valid
   * email address, and the consent checkbox has been checked,
   * before proceding with a data post to the API server.
   */
  processFormData(event) {
    this.setState({ userTriedSubmitting: true });
    event.preventDefault();

    // validate data here. Do not continue unless we're cool.
    let email = this.email.value;
    let consent = this.privacy.checked;

    if (email && this.validatesAsEmail(email).valid && consent) {
      this.submitDataToApi()
        .then(() => {
          this.apiSubmissionSuccessful();
        })
        .catch(e => this.apiSubmissionFailure(e));
    }

    ReactGA.event({
      category: `signup`,
      action: `form submit tap`,
      label: `Signup submitted from ${
        this.props.formPosition ? this.props.formPosition : document.title
      }`
    });
  }

  /**
   * On focus, we want to do two things:
   * 1.Fire a GA event when users interact with the signup form
   * 2.Reveal localization fields for header and footer signup forms
   */
  onInputFocus() {
    ReactGA.event({
      category: `signup`,
      action: `form focus`,
      label: `Signup form input focused`
    });

    let emailFields = document.querySelectorAll(
      '.fields-wrapper .form-control[type="email"]'
    );

    emailFields.forEach(emailField => {
      let currentEmailField = event.target === emailField;
      if (currentEmailField) {
        let localizationFields = document.querySelector(
          `.join-us[data-form-position="${this.props.formPosition}"] .form-l10n`
        );
        localizationFields.classList.remove(`d-none`);
      }
    });
  }

  /**
   * Render the signup CTA.
   */
  render() {
    if (
      this.state.apiSuccess &&
      this.state.apiSubmitted &&
      this.props.formPosition == "flow"
    ) {
      this.props.handleSignUp(true);
    }

    let signupState = classNames({
      "signup-success": this.state.apiSuccess && this.state.apiSubmitted,
      "signup-fail": !this.state.apiFailed && this.state.apiSubmitted
    });

    let layoutClass =
      this.props.layout === `2-column` ? `col-12 col-md-6` : `col-12`;

    let flowFormClasses =
      this.props.formPosition == "flow" ? "col-md-11 m-auto" : null;

    return (
      <div className={`row ${signupState}`}>
        <div className={layoutClass}>{this.renderFormHeading()}</div>
        <div className={`${layoutClass} ${flowFormClasses}`}>
          {this.renderFormContent()}
        </div>
      </div>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderFlowHeading() {
    return (
      <React.Fragment>
        <h2 className="text-center">{this.props.flowHeading}</h2>
        <p className="text-center">{this.props.flowText}</p>
      </React.Fragment>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderSnippetHeading() {
    return (
      <React.Fragment>
        <h5 className="h5-heading">
          {!this.state.apiSuccess ? `${this.props.ctaHeader}` : `Thanks!`}
        </h5>
        {!this.state.apiSuccess ? (
          <p
            dangerouslySetInnerHTML={{
              __html: this.props.ctaDescription
            }}
          />
        ) : (
          <p
            dangerouslySetInnerHTML={{
              __html: this.props.thankYouMessage
            }}
          />
        )}
      </React.Fragment>
    );
  }

  /**
   * Render the CTA heading.
   */
  renderFormHeading() {
    return (
      <React.Fragment>
        {this.props.formPosition == "flow"
          ? this.renderFlowHeading()
          : this.renderSnippetHeading()}
      </React.Fragment>
    );
  }

  /**
   * Render the email field in signup CTA.
   */
  renderEmailField() {
    // During the first render, we bind the email field to this.email
    // using ref={el => (this.email = el)}
    // This means this.email is undefined until the second render.
    // To avoid TypeError we have do the following conditional assignment.
    let emailValidation = this.email
      ? this.validatesAsEmail(this.email.value)
      : false;

    let wrapperClasses = classNames({
      "has-danger":
        (!this.state.apiSuccess &&
          this.state.userTriedSubmitting &&
          !emailValidation.valid) ||
        this.state.signupFailed
    });

    let classes = classNames(`mb-2`, {
      "position-relative": wrapperClasses !== ``
    });

    let errorWrapperClasses = classNames("glyph-container", {
      "d-none": this.props.formPosition == "flow"
    });

    return (
      <div className={wrapperClasses}>
        <div className={classes}>
          {this.props.formPosition == "flow" && (
            <label className="font-weight-bold" for="userEmail">
              Email
            </label>
          )}
          <input
            name="userEmail"
            type="email"
            className="form-control"
            placeholder={getText(`Please enter your email`)}
            ref={el => (this.email = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
          {this.state.userTriedSubmitting && !emailValidation.valid && (
            <div className={errorWrapperClasses}>
              <span className="form-error-glyph" />
            </div>
          )}
        </div>
        {this.state.userTriedSubmitting && !emailValidation.valid && (
          <p className="body-small form-check form-control-feedback">
            {emailValidation.errorMessage}
          </p>
        )}
        {this.state.signupFailed && (
          <small className="form-check form-control-feedback">
            Something went wrong. Please check your email address and try again
          </small>
        )}
      </div>
    );
  }

  /**
   * Render localization fields
   */

  setCountry(country) {
    this.setState({ country });
  }

  setLang(lang) {
    this.setState({ lang });
  }

  renderLocalizationFields() {
    let header = this.props.formPosition === `header`;
    let footer = this.props.formPosition === `footer`;
    let classes = classNames(`form-l10n`, {
      "d-none": footer || header
    });

    return (
      <div className={classes}>
        <div className="mb-2">
          <CountrySelect
            label={getText(`Your country`)}
            className="w-100"
            handleCountryChange={e => this.setCountry(e)}
          />
        </div>
        <div>
          <LanguageSelect
            className="w-100"
            handleLangChange={e => this.setLang(e)}
            selectedLang={this.state.lang}
          />
        </div>
      </div>
    );
  }

  /**
   * Render fields asking for user name
   */
  renderNameFields() {
    return (
      <div>
        <div className="mb-2">
          <input
            type="text"
            className="form-control"
            placeholder="First name"
            ref={el => (this.givenNames = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
        </div>
        <div className="mb-2">
          <input
            type="text"
            className="form-control"
            placeholder="Last name"
            ref={el => (this.surname = el)}
            onFocus={evt => this.onInputFocus(evt)}
          />
        </div>
      </div>
    );
  }
  /**
   * Render the privacy field in signup CTA.
   */
  renderPrivacyField() {
    let classes = classNames(`my-3`, {
      "form-check": true,
      "has-danger":
        !this.state.apiSuccess &&
        this.state.userTriedSubmitting &&
        !this.privacy.checked
    });

    return (
      <div className={classes}>
        <div className="d-flex align-items-start">
          <div className="mb-0 form-check d-flex align-items-start">
            <label className="form-check-label d-flex align-items-start align-items-md-center">
              <input
                type="checkbox"
                className="form-check-input"
                id="PrivacyCheckbox"
                ref={el => (this.privacy = el)}
                required
              />
              <p className="d-inline-block body-small form-text mb-0">
                {getText(
                  `I'm okay with Mozilla handling my info as explained in this Privacy Notice`
                )}
              </p>
              {this.state.userTriedSubmitting &&
                !this.state.apiSubmitted &&
                !this.privacy.checked &&
                this.props.formPosition !== "flow" && (
                  <span class="form-error-glyph privacy-error d-flex" />
                )}
            </label>
          </div>
        </div>
        {this.state.userTriedSubmitting && !this.privacy.checked && (
          <p className="body-small form-check form-control-feedback mt-0 mb-3">
            Please check this box if you want to proceed.
          </p>
        )}
      </div>
    );
  }

  /**
   * Render the submit button in signup CTA.
   */
  renderSubmitButton() {
    let classnames = classNames("btn btn-primary", {
      "w-100": this.props.formPosition !== "flow",
      "flex-1": this.props.formPosition == "flow",
      "mr-3": this.props.formPosition == "flow"
    });
    return <button className={classnames}>{getText(`Sign up`)}</button>;
  }

  /**
   * Render the actual CTA form, with an email
   * field and a consent checkbox.
   */
  renderFormContent() {
    if (this.state.apiSuccess) return null;

    let formClass = `d-flex flex-column`;
    let fieldsWrapperClass = `w-100`;
    let buttonsWrapperClass = `w-100`;

    if (this.props.buttonPosition === `side`) {
      formClass = `${formClass} flex-md-row`;
      fieldsWrapperClass = ``;
      buttonsWrapperClass = `ml-md-3`;
    }

    if (this.props.formPosition === `flow`) {
      buttonsWrapperClass = `d-flex`;
    }

    return (
      <form
        noValidate
        onSubmit={evt => this.processFormData(evt)}
        className={formClass}
      >
        <div className={`fields-wrapper ${fieldsWrapperClass}`}>
          {/* the data attribute is passed as a String from Python, so we need this check structured this way */}
          {this.props.askName === "True" && this.renderNameFields()}
          {this.renderEmailField()}
          {this.props.formPosition !== "flow" &&
            this.renderLocalizationFields()}
          {this.renderPrivacyField()}
        </div>
        <div className={buttonsWrapperClass}>
          {this.renderSubmitButton()}
          {this.props.formPosition == "flow" && (
            <button
              class="btn btn-primary btn-dismiss flex-1"
              onClick={() => this.props.handleSignUp(false)}
              type="button"
            >
              No Thanks
            </button>
          )}
        </div>
      </form>
    );
  }
}

JoinUs.defaultProps = {
  ctaHeader: `Protect the internet as a global public resource`,
  ctaDescription: `Join our email list to take action and stay updated!`,
  thankYouMessage: `If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. <strong>Please check your inbox or your spam filter for an email from us.</strong>`,
  newsletter: `mozilla-foundation`,
  askName: false
};
